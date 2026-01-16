#!/usr/bin/env python3

import requests
import io
import os
import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import speech_recognition as sr
import subprocess

# Configuration
SERVER_URL = "http://YOUR_SERVER_IP:5000"  # Your laptop/cloud server
BUTTON_CAPTURE = 17
BUTTON_VOICE = 27

class SamakshClient:
    def __init__(self):
        # Initialize camera
        self.camera = Picamera2()
        config = self.camera.create_still_configuration(main={"size": (1920, 1080)})
        self.camera.configure(config)
        self.camera.start()
        time.sleep(2)
        print("Camera ready")
        
        # Initialize GPIO buttons
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_CAPTURE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(BUTTON_VOICE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # Add button callbacks
        GPIO.add_event_detect(BUTTON_CAPTURE, GPIO.RISING, 
                            callback=self.handle_capture, bouncetime=300)
        GPIO.add_event_detect(BUTTON_VOICE, GPIO.RISING, 
                            callback=self.handle_voice, bouncetime=300)
        
        # Speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        print("SAMAKSH Client Ready!")
        print(f"Server: {SERVER_URL}")
        print("Press Capture button to read text")
        print("Press Voice button to ask questions")
    
    def handle_capture(self, channel):
        """Capture image and send to server for processing"""
        print("\n[Capture] Button pressed")
        self.play_beep()
        
        try:
            # Capture image
            print("Capturing image...")
            image_stream = io.BytesIO()
            self.camera.capture_file(image_stream, format='jpeg')
            image_stream.seek(0)
            
            # Send to server
            print("Sending to server...")
            files = {'image': ('capture.jpg', image_stream, 'image/jpeg')}
            data = {'action': 'read_text'}
            
            response = requests.post(
                f"{SERVER_URL}/process",
                files=files,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Download and play audio response
                if 'audio_url' in result:
                    self.play_audio(result['audio_url'])
                
                # Print text for debugging
                if 'text' in result:
                    print(f"Extracted text: {result['text'][:100]}...")
            else:
                print(f"Server error: {response.status_code}")
                self.speak_error("Server error occurred")
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            self.speak_error("Cannot connect to server")
        except Exception as e:
            print(f"Error: {e}")
            self.speak_error("An error occurred")
    
    def handle_voice(self, channel):
        """Capture voice question and send to server"""
        print("\n[Voice] Button pressed")
        self.play_beep()
        
        try:
            print("Listening...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Processing speech...")
            question = self.recognizer.recognize_google(audio, language='en-IN')
            print(f"Question: {question}")
            
            # Send question to server
            response = requests.post(
                f"{SERVER_URL}/query",
                json={'question': question},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'audio_url' in result:
                    self.play_audio(result['audio_url'])
            else:
                self.speak_error("Could not process question")
                
        except sr.WaitTimeoutError:
            print("No speech detected")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except Exception as e:
            print(f"Error: {e}")
            self.speak_error("Voice error occurred")
    
    def play_audio(self, audio_url):
        """Download and play audio from server"""
        try:
            audio_response = requests.get(f"{SERVER_URL}{audio_url}", timeout=10)
            if audio_response.status_code == 200:
                # Save temporarily
                with open('/tmp/response.mp3', 'wb') as f:
                    f.write(audio_response.content)
                
                # Play using mpg123
                subprocess.run(['mpg123', '-q', '/tmp/response.mp3'])
                os.remove('/tmp/response.mp3')
        except Exception as e:
            print(f"Audio playback error: {e}")
    
    def speak_error(self, message):
        """Simple error beep"""
        print(f"Error: {message}")
        # Could add offline TTS here if needed
    
    def play_beep(self):
        """Confirmation beep"""
        # Simple beep using speaker-test or similar
        pass
    
    def cleanup(self):
        GPIO.cleanup()
        self.camera.stop()
        print("Cleaned up")

if __name__ == "__main__":
    import signal
    import sys
    
    client = SamakshClient()
    
    def signal_handler(sig, frame):
        client.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Keep running
    print("\nReady. Press Ctrl+C to exit.")
    while True:
        time.sleep(0.1)
