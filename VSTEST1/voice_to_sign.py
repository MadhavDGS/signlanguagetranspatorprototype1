import os

# Paths with raw string to handle Windows paths
PROJECT_PATH = r"E:\till the uppercase work 12.44\till the uppercase work 12.44\VSTEST1"
ALPHABET_IMAGES_PATH = os.path.join(PROJECT_PATH, "alphabetimages")
VIDEOS_PATH = os.path.join(PROJECT_PATH, "mp4videos")

# Model paths for both ISL and ASL
VOSK_MODEL_PATH_ISL = r"E:\till the uppercase work 12.44\till the uppercase work 12.44\VSTEST1\vosk-model-en-in-0.5"
VOSK_MODEL_PATH_ASL = r"E:\till the uppercase work 12.44\till the uppercase work 12.44\VSTEST1\vosk-model-small-en-us-0.15"

# Add new model paths
VOSK_MODEL_PATH_HINDI = r"E:\till the uppercase work 12.44\till the uppercase work 12.44\VSTEST1\vosk-model-small-hi-0.22"
VOSK_MODEL_PATH_TELUGU = r"E:\till the uppercase work 12.44\till the uppercase work 12.44\VSTEST1\vosk-model-small-te-0.42"
VOSK_MODEL_PATH_GUJARATI = r"E:\till the uppercase work 12.44\till the uppercase work 12.44\VSTEST1\vosk-model-small-gu-0.42"

# Add new path for Indian alphabets
INDIAN_ALPHABET_IMAGES_PATH = os.path.join(PROJECT_PATH, "indianalphabetsandnumbers")

# Add model verification
print(f"Checking ISL model path: {VOSK_MODEL_PATH_ISL}")
print(f"ISL model path exists: {os.path.exists(VOSK_MODEL_PATH_ISL)}")
if os.path.exists(VOSK_MODEL_PATH_ISL):
    print("ISL model directory contents:")
    for item in os.listdir(VOSK_MODEL_PATH_ISL):
        print(f"  - {item}")

print(f"\nChecking ASL model path: {VOSK_MODEL_PATH_ASL}")
print(f"ASL model path exists: {os.path.exists(VOSK_MODEL_PATH_ASL)}")
if os.path.exists(VOSK_MODEL_PATH_ASL):
    print("ASL model directory contents:")
    for item in os.listdir(VOSK_MODEL_PATH_ASL):
        print(f"  - {item}")

import speech_recognition as sr
import cv2
import time
import pyaudio
from vosk import Model, KaldiRecognizer

# Load both models
try:
    print("\nLoading ISL model...")
    model_isl = Model(str(VOSK_MODEL_PATH_ISL))
    print("ISL model loaded successfully")
    
    print("\nLoading ASL model...")
    model_asl = Model(str(VOSK_MODEL_PATH_ASL))
    print("ASL model loaded successfully")
    
    # Initialize default recognizers
    recognizer_isl = KaldiRecognizer(model_isl, 16000)
    recognizer_asl = KaldiRecognizer(model_asl, 16000)
    
    print("\nBoth models and recognizers initialized successfully")
except Exception as e:
    print(f"\nError loading models: {str(e)}")
    print(f"ISL model path: {VOSK_MODEL_PATH_ISL}")
    print(f"ASL model path: {VOSK_MODEL_PATH_ASL}")
    raise

# Word-to-video mapping
video_dict = {
    "everything": "everything.mp4",
    "weekend": "weekend.mp4",
    "humid": "humid.mp4",
    "many": "many.mp4",
    "heavy rain": "heavy rain.mp4",
    "everyone": "everyone.mp4",
    "breezy": "breezy.mp4",
    "degrees": "degrees.mp4",
    "anyone": "anyone.mp4",
    "her": "her.mp4",
    "scattered rain": "scattered rain.mp4",
    "any": "any.mp4",
    "every monday": "every monday.mp4",
    "february": "february.mp4",
    "dust storm": "dust storm.mp4",
    "yourself": "yourself.mp4",
    "thunder": "thunder.mp4",
    "april": "april.mp4",
    "each": "each.mp4",
    "all": "all.mp4",
    "cold": "cold.mp4",
    "else": "else.mp4",
    "sunday": "sunday.mp4",
    "every thursday": "every thursday.mp4",
    "myself": "myself.mp4",
    "me": "me.mp4",
    "every two weeks": "every two weeks.mp4",
    "their": "their.mp4",
    "herself": "herself.mp4",
    "black ice": "black ice.mp4",
    "ourselves": "ourselves.mp4",
    "every friday": "every friday.mp4",
    "cloudy": "cloudy.mp4",
    "our": "our.mp4",
    "temperature": "temperature.mp4",
    "day": "day.mp4",
    "smog": "smog.mp4",
    "snow": "snow.mp4",
    "himself": "himself.mp4",
    "brisk": "brisk.mp4",
    "nothing": "nothing.mp4",
    "he": "he.mp4",
    "every tuesday": "every tuesday.mp4",
    "dusk": "dusk.mp4",
    "we": "we.mp4",
    "i": "i.mp4",
    "early": "early.mp4",
    "tuesday": "tuesday.mp4",
    "ice": "ice.mp4",
    "time": "time.mp4",
    "morning": "morning.mp4",
    "wintering": "wintering.mp4",
    "slippery walking": "slippery walking.mp4",
    "lightning": "lightning.mp4",
    "weather": "weather.mp4",
    "us": "us.mp4",
    "hail": "hail.mp4",
    "hot": "hot.mp4",
    "today": "today.mp4",
    "afternoon": "afternoon.mp4",
    "dry": "dry.mp4",
    "my": "my.mp4",
    "july": "july.mp4",
    "thursday": "thursday.mp4",
    "every two years": "every two years.mp4",
    "evening": "evening.mp4",
    "either": "either.mp4",
    "sunset": "sunset.mp4",
    "sunrise": "sunrise.mp4",
    "few": "few.mp4",
    "it": "it.mp4",
    "sun": "sun.mp4",
    "them": "them.mp4",
    "sleep": "sleep.mp4",
    "pouring rain": "pouring rain.mp4",
    "someone": "someone.mp4",
    "windy": "windy.mp4",
    "every two months": "every two months.mp4",
    "scattered snow": "scattered snow.mp4",
    "spring": "spring.mp4",
    "hour": "hour.mp4",
    "some": "some.mp4",
    "monthly": "monthly.mp4",
    "january": "january.mp4",
    "which": "which.mp4",
    "blizzard": "blizzard.mp4",
    "him": "him.mp4",
    "wednesday": "wednesday.mp4",
    "everyday": "everyday.mp4",
    "morning dew": "morning dew.mp4",
    "dawn": "dawn.mp4",
    "what": "what.mp4",
    "night": "night.mp4",
    "anything": "anything.mp4",
    "next week": "next week.mp4",
    "rainbow": "rainbow.mp4",
    "every week": "every week.mp4",
    "soon": "soon.mp4",
    "late night": "late night.mp4",
    "every wednesday": "every wednesday.mp4",
    "none": "none.mp4",
    "late": "late.mp4",
    "friday": "friday.mp4",
    "annually": "annually.mp4",
    "somebody": "somebody.mp4",
    "cool": "cool.mp4",
    "itself": "itself.mp4",
    "midnight": "midnight.mp4",
    "march": "march.mp4",
    "who": "who.mp4",
    "slippery": "slippery.mp4",
    "monday": "monday.mp4",
    "noon": "noon.mp4",
    "something": "something.mp4",
    "clear skies": "clear skies.mp4",
    "november": "november.mp4",
    "december": "december.mp4",
    "second": "second.mp4",
    "heat wave": "heat wave.mp4"
}

# ASL Video Dictionary
asl_video_dict = {
    # Weather Signs
    "weather": "weather.mp4",
    "hot": "hot.mp4",
    # ... rest of asl_video_dict entries ...
}

# ISL Video Dictionary (map to existing videos but with ISL context)
isl_video_dict = {
    # Common words
    "namaste": "hello.mp4",
    "dhanyavaad": "thank_you.mp4",
    
    # Weather related
    "mausam": "weather.mp4",
    "garmi": "hot.mp4",
    "thand": "cold.mp4",
    "barish": "rain.mp4",
    "badal": "cloudy.mp4",
    "dhoop": "sunny.mp4",
    "barf": "snow.mp4",
    "aandhi": "storm.mp4",
    
    # Time related
    "subah": "morning.mp4",
    "dopahar": "afternoon.mp4",
    "shaam": "evening.mp4",
    "raat": "night.mp4",
    "aaj": "today.mp4",
    "kal": "tomorrow.mp4",
    
    # Days
    "somvaar": "monday.mp4",
    "mangalvaar": "tuesday.mp4",
    "budhvaar": "wednesday.mp4",
    "guruvaar": "thursday.mp4",
    "shukravaar": "friday.mp4",
    "shanivaar": "saturday.mp4",
    "ravivaar": "sunday.mp4",
    
    # Months
    "january": "january.mp4",
    "february": "february.mp4",
    "march": "march.mp4",
    "april": "april.mp4",
    
    # Pronouns
    "main": "i.mp4",
    "mera": "my.mp4",
    "hum": "we.mp4",
    "hamara": "our.mp4",
    "tum": "you.mp4",
    "aap": "you.mp4",
    "vah": "he.mp4",
    "uska": "his.mp4",
    "unka": "their.mp4",
    
    # Common verbs
    "karna": "do.mp4",
    "jana": "go.mp4",
    "aana": "come.mp4",
    "dekhna": "see.mp4",
    "sunna": "hear.mp4",
    "bolna": "speak.mp4",
    "samajhna": "understand.mp4",
    
    # Numbers
    "ek": "one.mp4",
    "do": "two.mp4",
    "teen": "three.mp4",
    "char": "four.mp4",
    "paanch": "five.mp4",
    
    # Questions
    "kya": "what.mp4",
    "kahan": "where.mp4",
    "kab": "when.mp4",
    "kaun": "who.mp4",
    "kaise": "how.mp4",
    
    # Emotions
    "khushi": "happy.mp4",
    "dukh": "sad.mp4",
    "gussa": "angry.mp4",
    "pyaar": "love.mp4",
    
    # Family
    "maa": "mother.mp4",
    "pita": "father.mp4",
    "bhai": "brother.mp4",
    "behen": "sister.mp4",
    "parivar": "family.mp4"
}

# Language Mapping Dictionary
language_map = {
    # Weather
    "weather": ["mausam", "weather"],
    "hot": ["garmi", "hot"],
    # ... rest of language_map entries ...
}

def get_video_path(word, language='asl'):
    """Get video path based on language selection"""
    video_dict = isl_video_dict if language == 'isl' else asl_video_dict
    
    # First try exact match
    if word in video_dict:
        return os.path.join(VIDEOS_PATH, video_dict[word])
    
    # Try case-insensitive match
    word_lower = word.lower()
    for key, value in video_dict.items():
        if key.lower() == word_lower:
            return os.path.join(VIDEOS_PATH, value)
    
    # If no video found, spell it out
    return None

# Alphabet-to-image mapping
alphabet_dict = {chr(i): f"{chr(i)}_test.jpg" for i in range(65, 91)}
alphabet_dict.update({"nothing": "nothing_test.jpg", "space": "space_test.jpg"})

def resize_frame(frame, width=800):  # Add this new function
    """Resize frame while maintaining aspect ratio"""
    height = int(width * frame.shape[0] / frame.shape[1])
    return cv2.resize(frame, (width, height))

def play_video(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return
            
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = int(1000/fps)  # Calculate delay between frames
        
        # Create window without controls
        cv2.namedWindow("Sign Language", cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.setWindowProperty("Sign Language", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
            
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Resize frame to larger size    
            frame = resize_frame(frame, width=800)
            
            # Display frame without controls
            cv2.imshow("Sign Language", frame)
            
            # Use calculated delay for smooth playback
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyWindow("Sign Language")
    except Exception as e:
        print(f"Error playing video: {str(e)}")
        cv2.destroyAllWindows()

def recognize_speech(language='asl'):
    """Enhanced speech recognition with language support"""
    # Select appropriate model based on language
    if language == 'telugu':
        recognizer = KaldiRecognizer(Model(str(VOSK_MODEL_PATH_TELUGU)), 16000)
    elif language == 'hindi':
        recognizer = KaldiRecognizer(Model(str(VOSK_MODEL_PATH_HINDI)), 16000)
    elif language == 'gujarati':
        recognizer = KaldiRecognizer(Model(str(VOSK_MODEL_PATH_GUJARATI)), 16000)
    elif language == 'isl':
        recognizer = recognizer_isl
    else:
        recognizer = recognizer_asl
    
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, 
                     channels=1, 
                     rate=16000, 
                     input=True, 
                     frames_per_buffer=8192)
    stream.start_stream()
    print(f"Listening... (Language: {language.upper()})")
    
    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.FinalResult()
                if result:
                    text = result.strip()
                    if '"text" : ""' in text:  # Skip empty results
                        continue
                    word = text.split('"text" : "')[1].split('"')[0]
                    if word:  # Only return if we got actual text
                        print(f"Recognized ({language}): {word}")
                        return word.lower()
    except Exception as e:
        print(f"Error in speech recognition: {str(e)}")
    finally:
        stream.stop_stream()
        stream.close()
        mic.terminate()
        
    return "nothing"

def process_audio_file(file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            print("Processing audio file...")
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            # Record the entire audio file
            audio_data = recognizer.record(source)
            print("Recognizing speech...")
            # Use Google's speech recognition
            text = recognizer.recognize_google(audio_data)
            print("Recognized:", text)
            return text.lower()
    except sr.UnknownValueError:
        print("Speech recognition could not understand the audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from speech recognition service; {e}")
        return ""
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return ""

# Update alphabet dictionaries to use correct paths
# ASL alphabet continues to use the original alphabet images
asl_alphabet_dict = {chr(i): f"{chr(i)}_test.jpg" for i in range(65, 91)}
asl_alphabet_dict.update({
    "nothing": "nothing_test.jpg", 
    "space": "space_test.jpg"
})
# Add numbers separately to avoid dictionary comprehension error
for i in range(10):
    asl_alphabet_dict[str(i)] = f"{i}_test.jpg"

# Indian alphabet dictionary for ISL and regional languages - both upper and lowercase map to same files
indian_alphabet_dict = {}
# Add uppercase letters
for i in range(65, 91):
    indian_alphabet_dict[chr(i)] = f"{chr(i)}.jpg"
# Add lowercase letters (mapping to same uppercase files)
for i in range(97, 123):
    indian_alphabet_dict[chr(i)] = f"{chr(i).upper()}.jpg"
# Add numbers
for i in range(10):
    indian_alphabet_dict[str(i)] = f"{i}.jpg"

def text_to_sign(text, language='asl'):
    """Convert text to sign language videos with language-specific alphabet support"""
    words = text.split()
    video_paths = []
    current_chunk = []
    
    # Select appropriate alphabet dictionary and image path based on language
    if language == 'asl':
        alphabet_path = ALPHABET_IMAGES_PATH
        alphabet_dict_to_use = asl_alphabet_dict
    else:
        alphabet_path = INDIAN_ALPHABET_IMAGES_PATH
        alphabet_dict_to_use = indian_alphabet_dict
        
    # Select appropriate video dictionary based on language
    if language == 'hindi':
        video_dict_to_use = hindi_video_dict
    elif language == 'telugu':
        video_dict_to_use = telugu_video_dict
    elif language == 'gujarati':
        video_dict_to_use = gujarati_video_dict
    elif language == 'isl':
        video_dict_to_use = isl_video_dict
    else:  # default to ASL
        video_dict_to_use = video_dict
    
    for word in words:
        # First check if we have a video for the complete word
        video_path = None
        word_lower = word.lower()
        
        if word in video_dict_to_use:
            video_path = os.path.join(VIDEOS_PATH, video_dict_to_use[word])
            
        if video_path and os.path.exists(video_path):
            if current_chunk:
                video_paths.extend(current_chunk)
                current_chunk = []
            video_paths.append(video_path)
        else:
            # Spell out using appropriate alphabet
            for char in word:
                if language == 'asl':
                    img_file = alphabet_dict_to_use.get(char.upper(), "nothing_test.jpg")
                    img_path = os.path.join(alphabet_path, img_file)
                else:
                    # For non-ASL, use indian_alphabet_dict for letters/numbers
                    if char.isalnum():  # If it's a letter or number
                        img_file = alphabet_dict_to_use.get(char, "0.jpg")
                        img_path = os.path.join(alphabet_path, img_file)
                    else:  # For special characters or unknown chars
                        img_path = os.path.join(ALPHABET_IMAGES_PATH, "nothing_test.jpg")
                current_chunk.append(img_path)
            
            # Only add space_test.jpg after complete words, not between letters
            if word != words[-1]:  # Don't add space after the last word
                current_chunk.append(os.path.join(ALPHABET_IMAGES_PATH, "space_test.jpg"))
    
    # Add any remaining spelled words
    if current_chunk:
        video_paths.extend(current_chunk)
    
    return video_paths

# Add Natural Language Processing with spaCy
import spacy
try:
    nlp = spacy.load('en_core_web_sm')  # Free, offline model
except:
    os.system('python -m spacy download en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

def enhance_speech_recognition(text):
    """Use NLP to improve recognition accuracy"""
    doc = nlp(text)
    
    # Context understanding
    is_question = any(token.tag_ == "WP" for token in doc)
    is_command = doc[0].tag_ == "VB"
    
    # Named entity recognition
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Basic grammar correction
    corrected_text = text
    if doc[0].tag_ == "VBG" and len(doc) > 1:  # Fix common "ing" errors
        corrected_text = "I am " + text
        
    return {
        'text': corrected_text,
        'is_question': is_question,
        'is_command': is_command,
        'entities': entities
    }

def optimize_sign_sequence(text):
    """Use NLP to optimize sign language sequence"""
    doc = nlp(text)
    optimized_sequence = []
    
    for token in doc:
        # Handle tenses
        if token.pos_ == "VERB":
            tense = token.morph.get("Tense", ["present"])[0]
            if tense == "past":
                optimized_sequence.append("PAST")
            elif tense == "future":
                optimized_sequence.append("FUTURE")
                
        # Handle pronouns
        if token.pos_ == "PRON":
            if token.text.lower() in ["i", "me", "my"]:
                optimized_sequence.append("SELF")
                
        # Add the word itself
        optimized_sequence.append(token.text.upper())
        
    return optimized_sequence

def recognize_speech_realtime(language='asl'):
    """Enhanced real-time speech recognition with language support"""
    # Select appropriate model based on language
    if language == 'telugu':
        recognizer = KaldiRecognizer(Model(str(VOSK_MODEL_PATH_TELUGU)), 16000)
    elif language == 'hindi':
        recognizer = KaldiRecognizer(Model(str(VOSK_MODEL_PATH_HINDI)), 16000)
    elif language == 'gujarati':
        recognizer = KaldiRecognizer(Model(str(VOSK_MODEL_PATH_GUJARATI)), 16000)
    elif language == 'isl':
        recognizer = recognizer_isl
    else:
        recognizer = recognizer_asl
    
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, 
                     channels=1, 
                     rate=16000, 
                     input=True, 
                     frames_per_buffer=512)
    stream.start_stream()
    print(f"Listening... (Language: {language.upper()}) (Press 'q' to quit)")
    
    try:
        while True:
            data = stream.read(512, exception_on_overflow=False)
            
            if recognizer.AcceptWaveform(data):
                result = recognizer.FinalResult()
            else:
                result = recognizer.PartialResult()
            
            if result:
                text = result.strip()
                if '"text" : ""' in text or '"partial" : ""' in text:
                    continue
                    
                if '"text"' in text:
                    words = text.split('"text" : "')[1].split('"')[0].lower()
                elif '"partial"' in text:
                    words = text.split('"partial" : "')[1].split('"')[0].lower()
                else:
                    continue
                    
                if words:
                    # Enhance recognition with NLP
                    enhanced = enhance_speech_recognition(words)
                    # Optimize sign sequence
                    sign_sequence = optimize_sign_sequence(enhanced['text'])
                    
                    print(f"Recognized ({language}): {words}")
                    print("Enhanced:", enhanced)
                    print("Sign Sequence:", sign_sequence)
                    
                    # Display signs
                    for word in sign_sequence:
                        if language == 'telugu':
                            video_dict_to_use = telugu_video_dict
                        elif language == 'hindi':
                            video_dict_to_use = hindi_video_dict
                        elif language == 'gujarati':
                            video_dict_to_use = gujarati_video_dict
                        else:
                            video_dict_to_use = video_dict
                            
                        if word in video_dict_to_use:
                            video_path = get_video_path(word, language)
                            play_video(video_path)
                        else:
                            # Spell out word
                            for char in word:
                                if char.isalnum():
                                    if language in ['telugu', 'hindi', 'gujarati']:
                                        img_path = os.path.join(INDIAN_ALPHABET_IMAGES_PATH, 
                                                              indian_alphabet_dict.get(char, "0.jpg"))
                                    else:
                                        img_path = os.path.join(ALPHABET_IMAGES_PATH, 
                                                              alphabet_dict.get(char.upper(), "nothing_test.jpg"))
                                    img = cv2.imread(img_path)
                                    if img is not None:
                                        cv2.imshow("Sign Language", img)
                                        cv2.waitKey(400)  # Show each letter for 400ms
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        print(f"Error in speech recognition: {str(e)}")
    finally:
        stream.stop_stream()
        stream.close()
        mic.terminate()
        cv2.destroyAllWindows()

def scan_video_directory():
    """Scan the mp4videos directory and create a dictionary of all available videos"""
    video_files = {}
    uppercase_videos = []  # New list to track uppercase videos
    try:
        for file in os.listdir(VIDEOS_PATH):
            if file.endswith('.mp4') or file.endswith('.MP4'):
                # Store uppercase videos in a separate list
                if file[:-4].isupper():
                    uppercase_videos.append(file)
                # Remove .mp4 extension and create both lowercase and original case keys
                key_lower = file[:-4].lower()
                key_original = file[:-4]
                video_files[key_lower] = file  # Add lowercase key
                video_files[key_original] = file  # Add original case key
                
        print(f"\nFound {len(video_files)} total video files")
        print(f"\nUPPERCASE VIDEOS ({len(uppercase_videos)}):")
        for video in sorted(uppercase_videos):
            print(f"  {video}")
            
    except Exception as e:
        print(f"Error scanning video directory: {e}")
    return video_files

# Update the video dictionary with all available videos
available_videos = scan_video_directory()
video_dict.update(available_videos)

# Add new categories to organize videos
video_categories = {
    "weather": [
        "weather", "hot", "cold", "rain", "heavy rain", "lightning", 
        "cloudy", "sunny", "snow", "hail", "thunder", "smog", "humid",
        "windy", "breezy", "dust storm", "black ice", "clear skies",
        "scattered rain", "scattered snow", "pouring rain", "heat wave",
        "blizzard", "morning dew", "rainbow", "dry", "brisk", "slippery"
    ],
    "time": [
        "today", "morning", "afternoon", "evening", "night", "late",
        "early", "time", "day", "hour", "minute", "dawn", "dusk",
        "noon", "midnight", "late night", "sunrise", "sunset"
    ],
    "days": [
        "monday", "tuesday", "wednesday", "thursday", "friday", "sunday",
        "weekend", "every monday", "every tuesday", "every wednesday",
        "every thursday", "every friday", "every week", "next week"
    ],
    "months": [
        "january", "february", "march", "april", "july", "november",
        "december"
    ],
    "seasons": [
        "spring", "summer", "wintering"
    ],
    "pronouns": [
        "i", "me", "we", "us", "it", "he", "him", "they", "them",
        "myself", "yourself", "himself", "herself", "ourselves", "itself",
        "her", "their", "our", "my"
    ]
}

def get_category_words(category):
    """Get all words in a specific category"""
    return video_categories.get(category, [])

def list_available_categories():
    """Print all available categories and their words"""
    print("\nAvailable categories:")
    for category, words in video_categories.items():
        print(f"\n{category.upper()}:")
        available_words = [word for word in words if word in video_dict]
        print(", ".join(available_words))

# Add expanded dictionaries for regional languages
hindi_video_dict = {
    # Existing mappings...
    
    # Weather
    "मौसम": "weather.mp4",
    "गरमी": "hot.mp4",
    "ठंड": "cold.mp4",
    "बारिश": "rain.mp4",
    "भारी बारिश": "heavy rain.mp4",
    "बिजली": "lightning.mp4",
    "बादल": "cloudy.mp4",
    "धूप": "sunny.mp4",
    "बर्फ": "snow.mp4",
    "ओला": "hail.mp4",
    "गरज": "thunder.mp4",
    "धुंध": "smog.mp4",
    "नमी": "humid.mp4",
    "हवादार": "windy.mp4",
    "हल्की हवा": "breezy.mp4",
    "धूल भरी आंधी": "dust storm.mp4",
    "काली बर्फ": "black ice.mp4",
    "साफ आसमान": "clear skies.mp4",
    "छिटपुट बारिश": "scattered rain.mp4",
    "छिटपुट बर्फबारी": "scattered snow.mp4",
    "मूसलाधार बारिश": "pouring rain.mp4",
    "गर्मी की लहर": "heat wave.mp4",
    "बर्फानी तूफान": "blizzard.mp4",
    "सुबह की ओस": "morning dew.mp4",
    "इंद्रधनुष": "rainbow.mp4",
    "सूखा": "dry.mp4",
    "तेज": "brisk.mp4",
    "फिसलन": "slippery.mp4",

    # Time
    "आज": "today.mp4",
    "सुबह": "morning.mp4",
    "दोपहर": "afternoon.mp4",
    "शाम": "evening.mp4",
    "रात": "night.mp4",
    "देर": "late.mp4",
    "जल्दी": "early.mp4",
    "समय": "time.mp4",
    "दिन": "day.mp4",
    "घंटा": "hour.mp4",
    "मिनट": "minute.mp4",
    "भोर": "dawn.mp4",
    "संध्या": "dusk.mp4",
    "दोपहर": "noon.mp4",
    "मध्यरात्रि": "midnight.mp4",
    "देर रात": "late night.mp4",
    "सूर्योदय": "sunrise.mp4",
    "सूर्यास्त": "sunset.mp4",

    # Days and Time Periods
    "सोमवार": "monday.mp4",
    "मंगलवार": "tuesday.mp4",
    "बुधवार": "wednesday.mp4",
    "गुरुवार": "thursday.mp4",
    "शुक्रवार": "friday.mp4",
    "रविवार": "sunday.mp4",
    "सप्ताहांत": "weekend.mp4",
    "हर सोमवार": "every monday.mp4",
    "हर मंगलवार": "every tuesday.mp4",
    "हर बुधवार": "every wednesday.mp4",
    "हर गुरुवार": "every thursday.mp4",
    "हर शुक्रवार": "every friday.mp4",
    "हर सप्ताह": "every week.mp4",
    "अगला सप्ताह": "next week.mp4",

    # Months
    "जनवरी": "january.mp4",
    "फरवरी": "february.mp4",
    "मार्च": "march.mp4",
    "अप्रैल": "april.mp4",
    "जुलाई": "july.mp4",
    "नवंबर": "november.mp4",
    "दिसंबर": "december.mp4",

    # Seasons
    "वसंत": "spring.mp4",
    "गर्मी": "summer.mp4",
    "सर्दी": "wintering.mp4",

    # Pronouns and Common Words
    "मैं": "i.mp4",
    "मुझे": "me.mp4",
    "हम": "we.mp4",
    "हमें": "us.mp4",
    "यह": "it.mp4",
    "वह": "he.mp4",
    "उसको": "him.mp4",
    "वे": "they.mp4",
    "उन्हें": "them.mp4",
    "स्वयं": "myself.mp4",
    "खुद": "yourself.mp4",
    "अपने आप": "himself.mp4",
    "खुद": "herself.mp4",
    "हम सब": "ourselves.mp4",
    "स्वयं": "itself.mp4",
    "उसकी": "her.mp4",
    "उनका": "their.mp4",
    "हमारा": "our.mp4",
    "मेरा": "my.mp4"
}

telugu_video_dict = {
    # Weather
    "వాతావరణం": "weather.mp4",
    "వేడి": "hot.mp4",
    "చల్లని": "cold.mp4",
    "వర్షం": "rain.mp4",
    "భారీ వర్షం": "heavy rain.mp4",
    "మెరుపు": "lightning.mp4",
    "మేఘాలు": "cloudy.mp4",
    "ఎండ": "sunny.mp4",
    "మంచు": "snow.mp4",
    "వడగళ్ళు": "hail.mp4",
    "ఉరుము": "thunder.mp4",
    "పొగమంచు": "smog.mp4",
    "తేమ": "humid.mp4",
    "గాలి": "windy.mp4",
    "చల్లని గాలి": "breezy.mp4",
    "దుమారం": "dust storm.mp4",
    "నల్ల మంచు": "black ice.mp4",
    "నిర్మల ఆకాశం": "clear skies.mp4",
    "చెదురుమదురు వర్షం": "scattered rain.mp4",
    "చెదురుమదురు మంచు": "scattered snow.mp4",
    "కుండపోత వర్షం": "pouring rain.mp4",
    "వేడి గాలులు": "heat wave.mp4",
    "మంచు తుఫాను": "blizzard.mp4",
    "మంచు బిందువులు": "morning dew.mp4",
    "ఇంద్రధనుస్సు": "rainbow.mp4",
    "పొడి": "dry.mp4",
    "చురుకైన": "brisk.mp4",
    "జారుడు": "slippery.mp4",

    # Time
    "ఈరోజు": "today.mp4",
    "ఉదయం": "morning.mp4",
    "మధ్యాహ్నం": "afternoon.mp4",
    "సాయంత్రం": "evening.mp4",
    "రాత్రి": "night.mp4",
    "ఆలస్యం": "late.mp4",
    "ముందుగా": "early.mp4",
    "సమయం": "time.mp4",
    "రోజు": "day.mp4",
    "గంట": "hour.mp4",
    "నిమిషం": "minute.mp4",
    "తెల్లవారు": "dawn.mp4",
    "సంధ్య": "dusk.mp4",
    "మధ్యాహ్నం": "noon.mp4",
    "అర్ధరాత్రి": "midnight.mp4",
    "రాత్రి పొద్దు": "late night.mp4",
    "సూర్యోదయం": "sunrise.mp4",
    "సూర్యాస్తమయం": "sunset.mp4",

    # Days
    "సోమవారం": "monday.mp4",
    "మంగళవారం": "tuesday.mp4",
    "బుధవారం": "wednesday.mp4",
    "గురువారం": "thursday.mp4",
    "శుక్రవారం": "friday.mp4",
    "ఆదివారం": "sunday.mp4",
    "వారాంతం": "weekend.mp4",
    "ప్రతి సోమవారం": "every monday.mp4",
    "ప్రతి మంగళవారం": "every tuesday.mp4",
    "ప్రతి బుధవారం": "every wednesday.mp4",
    "ప్రతి గురువారం": "every thursday.mp4",
    "ప్రతి శుక్రవారం": "every friday.mp4",
    "ప్రతి వారం": "every week.mp4",
    "వచ్చే వారం": "next week.mp4"
}

gujarati_video_dict = {
    # Weather
    "હવામાન": "weather.mp4",
    "ગરમ": "hot.mp4",
    "ઠંડું": "cold.mp4",
    "વરસાદ": "rain.mp4",
    "ભારે વરસાદ": "heavy rain.mp4",
    "વીજળી": "lightning.mp4",
    "વાદળછાયું": "cloudy.mp4",
    "તડકો": "sunny.mp4",
    "બરફ": "snow.mp4",
    "કરા": "hail.mp4",
    "ગડગડાટ": "thunder.mp4",
    "ધુમ્મસ": "smog.mp4",
    "ભેજવાળું": "humid.mp4",
    "પવન": "windy.mp4",
    "મંદ પવન": "breezy.mp4",
    "ધૂળની આંધી": "dust storm.mp4",
    "કાળો બરફ": "black ice.mp4",
    "ચોખ્ખું આકાશ": "clear skies.mp4",
    "છૂટોછવાયો વરસાદ": "scattered rain.mp4",
    "છૂટોછવાયો બરફ": "scattered snow.mp4",
    "ધોધમાર વરસાદ": "pouring rain.mp4",
    "ગરમીનું મોજું": "heat wave.mp4",
    "બરફનું તોફાન": "blizzard.mp4",
    "ઝાકળ": "morning dew.mp4",
    "મેઘધનુષ": "rainbow.mp4",
    "સૂકું": "dry.mp4",
    "ઝડપી": "brisk.mp4",
    "લપસણું": "slippery.mp4",

    # Time
    "આજે": "today.mp4",
    "સવાર": "morning.mp4",
    "બપોર": "afternoon.mp4",
    "સાંજ": "evening.mp4",
    "રાત": "night.mp4",
    "મોડું": "late.mp4",
    "વહેલું": "early.mp4",
    "સમય": "time.mp4",
    "દિવસ": "day.mp4",
    "કલાક": "hour.mp4",
    "મિનિટ": "minute.mp4",
    "પરોઢ": "dawn.mp4",
    "સંધ્યા": "dusk.mp4",
    "બપોર": "noon.mp4",
    "મધરાત": "midnight.mp4",
    "મોડી રાત": "late night.mp4",
    "સૂર્યોદય": "sunrise.mp4",
    "સૂર્યાસ્ત": "sunset.mp4",

    # Days
    "સોમવાર": "monday.mp4",
    "મંગળવાર": "tuesday.mp4",
    "બુધવાર": "wednesday.mp4",
    "ગుરુવાર": "thursday.mp4",
    "શુક્રવાર": "friday.mp4",
    "રવિવાર": "sunday.mp4",
    "સપ્તાહાંત": "weekend.mp4",
    "દર સોમવારે": "every monday.mp4",
    "દર મંગળવારે": "every tuesday.mp4",
    "દર બુધવારે": "every wednesday.mp4",
    "દર ગుરુવારે": "every thursday.mp4",
    "દર શુક્રવારે": "every friday.mp4",
    "દર અઠવાડિયે": "every week.mp4",
    "આવતા અઠવાડિયે": "next week.mp4"
}

if __name__ == "__main__":
    while True:  # Keep running until user chooses to quit
        print("\nSelect an option:")
        print("1: Real-time audio to sign")
        print("2: Audio file to sign")
        print("3: Text to sign")
        print("4: Quit")
        choice = input("Enter choice: ")
        
        if choice == "1":
            recognize_speech_realtime()
        elif choice == "2":
            file_path = input("Enter audio file path: ")
            text = process_audio_file(file_path)
            print(f"Recognized text: {text}")
            text_to_sign(text)
        elif choice == "3":
            text = input("Enter text: ")
            text_to_sign(text)
        elif choice == "4":
            print("Thank you for using the Sign Language Translator!")
            break  # Exit the program
        else:
            print("Invalid choice. Please try again.")
