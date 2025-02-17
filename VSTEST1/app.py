from flask import Flask, render_template, request, jsonify, send_file, Response
from flask_cors import CORS
import os
import tempfile
import base64
import pyaudio
import json
import threading
import queue
import time

# Import after verifying model loads correctly
from voice_to_sign import *
from sign_translator import SignTranslator

app = Flask(__name__)
CORS(app)

# Initialize translator
translator = SignTranslator()

# Optimized audio settings
CHUNK_SIZE = 4096  # Smaller chunk size for faster processing
SAMPLE_RATE = 16000
audio_queue = queue.Queue(maxsize=10)  # Limit queue size to prevent lag
is_recording = False
current_model = None  # Will store the currently selected model
current_recognizer = None

@app.route('/select_language', methods=['POST'])
def select_language():
    global current_model, current_recognizer
    try:
        language = request.json.get('language', '')
        if not language:
            return jsonify({'error': 'No language specified'}), 400
            
        model_paths = {
            'isl': VOSK_MODEL_PATH_ISL,
            'asl': VOSK_MODEL_PATH_ASL,
            'hindi': VOSK_MODEL_PATH_HINDI,
            'telugu': VOSK_MODEL_PATH_TELUGU,
            'gujarati': VOSK_MODEL_PATH_GUJARATI
        }
        
        if language in model_paths:
            current_model = Model(str(model_paths[language]))
            current_recognizer = KaldiRecognizer(current_model, SAMPLE_RATE)
            print(f"{language.upper()} model selected")
            return jsonify({'status': f'{language.upper()} selected'})
            
        return jsonify({'error': 'Invalid language selection'}), 400
        
    except Exception as e:
        print(f"Error selecting language: {str(e)}")
        return jsonify({'error': str(e)}), 500

def process_audio_stream():
    global is_recording, current_recognizer
    
    if not current_recognizer:
        yield f"data: {json.dumps({'error': 'Please select a language first'})}\n\n"
        return
        
    buffer = []
    last_send_time = time.time()
    
    try:
        while is_recording:
            try:
                try:
                    audio_data = audio_queue.get(timeout=0.1)
                except queue.Empty:
                    continue
                    
                if current_recognizer.AcceptWaveform(audio_data):
                    result = json.loads(current_recognizer.Result())
                    if result.get('text'):
                        # Process complete phrases
                        text = result['text'].strip()
                        if text:
                            yield f"data: {json.dumps({'text': text})}\n\n"
                            buffer = []  # Clear buffer after sending
                else:
                    # Handle partial results
                    partial = json.loads(current_recognizer.PartialResult())
                    if partial.get('partial'):
                        current_time = time.time()
                        # Only send partial results every 300ms
                        if current_time - last_send_time > 0.3:
                            yield f"data: {json.dumps({'partial': partial['partial']})}\n\n"
                            last_send_time = current_time
                            
            except Exception as e:
                print(f"Error processing audio chunk: {e}")
                continue
                
    except Exception as e:
        print(f"Error in audio stream processing: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_stream', methods=['GET'])
def start_stream():
    global is_recording
    is_recording = True
    
    def generate():
        try:
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=SAMPLE_RATE,
                              input=True,
                              frames_per_buffer=CHUNK_SIZE)
            
            while is_recording:
                data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                # Use try_put to prevent blocking on full queue
                try:
                    audio_queue.put(data, timeout=0.1)
                except queue.Full:
                    # Skip frame if queue is full
                    continue
                    
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
        except Exception as e:
            print(f"Error in audio stream: {e}")
    
    threading.Thread(target=generate, daemon=True).start()
    return Response(process_audio_stream(), 
                   mimetype='text/event-stream')

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    global is_recording
    is_recording = False
    return jsonify({'status': 'stopped'})

@app.route('/translate_text', methods=['POST'])
def translate_text():
    try:
        text = request.json.get('text', '')
        language = request.json.get('language', 'asl')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
            
        # Get translation with context
        translation = translator.translate(text, language)
        
        # Convert to video paths
        video_paths = text_to_sign(translation['signs'], language)
        
        return jsonify({
            'video_paths': video_paths,
            'expressions': translation['expressions'],
            'context': translation.get('context', {})  # Include grammar context
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    try:
        original = request.json.get('original', '')
        correction = request.json.get('correction', '')
        
        if not original or not correction:
            return jsonify({'error': 'Missing feedback data'}), 400
            
        translator.learn_from_feedback(original, correction)
        return jsonify({'status': 'Feedback recorded successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/media/<path:filename>')
def serve_media(filename):
    return send_file(os.path.join(VIDEOS_PATH, filename))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 