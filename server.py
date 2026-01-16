#!/usr/bin/env python3

from flask import Flask, request, jsonify, send_file
from PIL import Image
import io
import os
import hashlib
import base64
from openai import OpenAI
import google.generativeai as genai
from elevenlabs import ElevenLabs
from gtts import gTTS

app = Flask(__name__)

# Configuration
OPENAI_API_KEY = "sk-proj-your-key"
GEMINI_API_KEY = "your-gemini-key"
ELEVENLABS_API_KEY = "your-eleven-key"

# Initialize clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

# Storage
AUDIO_DIR = "audio_cache"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Session state (in production, use Redis or database)
current_context = {
    'last_text': None,
    'last_image': None,
    'language': 'en'
}

def detect_language(text):
    """Simple language detection"""
    import re
    if re.search(r'[\u0900-\u097F]', text):
        return 'hi'
    return 'en'

def extract_text_gemini(image_bytes):
    """Extract text using Gemini Vision"""
    try:
        # Convert to base64
        image_b64 = base64.b64encode(image_bytes).decode()
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content([
            "Extract all text from this image. If there's no text, say 'NO_TEXT_FOUND'. Return only the extracted text, nothing else.",
            {"mime_type": "image/jpeg", "data": image_b64}
        ])
        
        text = response.text.strip()
        
        if "NO_TEXT_FOUND" in text:
            return None, None
        
        language = detect_language(text)
        return text, language
        
    except Exception as e:
        print(f"Gemini error: {e}")
        return None, None

def extract_text_gpt(image_bytes):
    """Extract text using GPT-4 Vision"""
    try:
        image_b64 = base64.b64encode(image_bytes).decode()
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract all visible text from this image. If no text is found, respond with only 'NO_TEXT_FOUND'. Return only the extracted text."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        text = response.choices[0].message.content.strip()
        
        if "NO_TEXT_FOUND" in text:
            return None, None
        
        language = detect_language(text)
        return text, language
        
    except Exception as e:
        print(f"GPT error: {e}")
        return None, None

def describe_scene_gpt(image_bytes):
    """Describe scene using GPT-4 Vision"""
    try:
        image_b64 = base64.b64encode(image_bytes).decode()
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe this scene for a visually impaired person. Focus on: objects, their locations (left/right/center), people if any, and spatial layout. Be concise and clear."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Scene description error: {e}")
        return "Could not analyze scene"

def generate_tts_elevenlabs(text, language):
    """Generate speech using ElevenLabs"""
    try:
        # Create hash for caching
        text_hash = hashlib.md5(f"{text}_{language}".encode()).hexdigest()
        audio_path = f"{AUDIO_DIR}/{text_hash}.mp3"
        
        # Check cache
        if os.path.exists(audio_path):
            print("Using cached audio")
            return audio_path
        
        # Generate
        voice_id = "pNInz6obpgDQGcFmaJgB" if language == 'en' else "EXAVITQu4vr4xnSDxMaL"
        
        audio = eleven_client.generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v2"
        )
        
        # Save
        with open(audio_path, 'wb') as f:
            for chunk in audio:
                f.write(chunk)
        
        return audio_path
        
    except Exception as e:
        print(f"ElevenLabs error: {e}, falling back to gTTS")
        return generate_tts_gtts(text, language)

def generate_tts_gtts(text, language):
    """Fallback TTS using gTTS"""
    text_hash = hashlib.md5(f"{text}_{language}_gtts".encode()).hexdigest()
    audio_path = f"{AUDIO_DIR}/{text_hash}.mp3"
    
    if not os.path.exists(audio_path):
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(audio_path)
    
    return audio_path

def answer_question(question, context_text):
    """Answer question using context"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are SAMAKSH, an AI assistant for visually impaired users. The user just read this text: '{context_text}'. Answer their question based on this context. Be concise and helpful."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=150
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Question answering error: {e}")
        return "Sorry, I couldn't process that question."

@app.route('/process', methods=['POST'])
def process_image():
    """Main endpoint for image processing"""
    try:
        # Get image
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        image_bytes = image_file.read()
        
        # Store for context
        current_context['last_image'] = image_bytes
        
        # Extract text (try Gemini first, fallback to GPT)
        print("Extracting text with Gemini...")
        text, language = extract_text_gemini(image_bytes)
        
        if not text:
            print("No text with Gemini, trying GPT...")
            text, language = extract_text_gpt(image_bytes)
        
        # If no text found, offer scene description
        if not text:
            print("No text found, describing scene...")
            description = describe_scene_gpt(image_bytes)
            language = 'en'
            
            response_text = f"No text found. Here's what I see: {description}"
            audio_path = generate_tts_elevenlabs(response_text, language)
            
            return jsonify({
                'text': None,
                'description': description,
                'language': language,
                'audio_url': f'/audio/{os.path.basename(audio_path)}'
            })
        
        # Text found - store and convert to speech
        current_context['last_text'] = text
        current_context['language'] = language
        
        print(f"Text extracted ({language}): {text[:100]}...")
        
        # Generate audio
        audio_path = generate_tts_elevenlabs(text, language)
        
        return jsonify({
            'text': text,
            'language': language,
            'audio_url': f'/audio/{os.path.basename(audio_path)}'
        })
        
    except Exception as e:
        print(f"Process error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/query', methods=['POST'])
def handle_query():
    """Handle voice questions"""
    try:
        data = request.json
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        # Check for scene description request
        scene_keywords = ['describe', 'scene', 'see', 'what is', 'क्या है', 'room', 'around']
        if any(kw in question.lower() for kw in scene_keywords):
            if current_context['last_image']:
                description = describe_scene_gpt(current_context['last_image'])
                language = current_context.get('language', 'en')
                audio_path = generate_tts_elevenlabs(description, language)
                
                return jsonify({
                    'answer': description,
                    'audio_url': f'/audio/{os.path.basename(audio_path)}'
                })
        
        # Answer from context
        if current_context['last_text']:
            answer = answer_question(question, current_context['last_text'])
            language = current_context.get('language', 'en')
            audio_path = generate_tts_elevenlabs(answer, language)
            
            return jsonify({
                'answer': answer,
                'audio_url': f'/audio/{os.path.basename(audio_path)}'
            })
        else:
            response = "Please capture an image first"
            audio_path = generate_tts_gtts(response, 'en')
            return jsonify({
                'answer': response,
                'audio_url': f'/audio/{os.path.basename(audio_path)}'
            })
        
    except Exception as e:
        print(f"Query error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve cached audio files"""
    return send_file(f"{AUDIO_DIR}/{filename}", mimetype='audio/mpeg')

@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("SAMAKSH Server starting...")
    print(f"Audio cache: {AUDIO_DIR}")
    app.run(host='0.0.0.0', port=5000, debug=True)
