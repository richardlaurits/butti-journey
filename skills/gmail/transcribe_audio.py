#!/usr/bin/env python3
"""
Transcribe audio files using Google Cloud Speech-to-Text API
Usage: python3 transcribe_audio.py <audio_file_path>
"""

import sys
import os
from google.cloud import speech_v1
from google.oauth2 import service_account
import json

def get_credentials():
    """Load Google Cloud credentials from gmail_credentials.json"""
    creds_file = os.path.join(os.path.dirname(__file__), 'gmail_credentials.json')
    
    # Check if we have a service account key (for Speech-to-Text)
    # For now, we'll use the OAuth token from Gmail
    if not os.path.exists(creds_file):
        print("❌ Missing credentials file!")
        return None
    
    # For Speech-to-Text, we actually need to use the OAuth token that's already authorized
    # The google-cloud-speech library will use GOOGLE_APPLICATION_CREDENTIALS or Application Default Credentials
    return True

def transcribe_audio(audio_file_path):
    """Transcribe an audio file using Google Cloud Speech-to-Text"""
    
    if not os.path.exists(audio_file_path):
        print(f"❌ Audio file not found: {audio_file_path}")
        return None
    
    try:
        # Initialize Speech-to-Text client
        client = speech_v1.SpeechClient()
        
        # Read audio file
        with open(audio_file_path, 'rb') as audio_file:
            content = audio_file.read()
        
        # Detect file format from extension
        file_ext = os.path.splitext(audio_file_path)[1].lower()
        encoding_map = {
            '.ogg': speech_v1.RecognitionConfig.AudioEncoding.OGG_OPUS,
            '.wav': speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            '.mp3': speech_v1.RecognitionConfig.AudioEncoding.MP3,
            '.m4a': speech_v1.RecognitionConfig.AudioEncoding.MP3,
        }
        
        encoding = encoding_map.get(file_ext, speech_v1.RecognitionConfig.AudioEncoding.OGG_OPUS)
        
        audio = speech_v1.RecognitionAudio(content=content)
        
        config = speech_v1.RecognitionConfig(
            encoding=encoding,
            language_code="sv-SE",  # Swedish
            enable_automatic_punctuation=True,
        )
        
        # Transcribe
        response = client.recognize(config=config, audio=audio)
        
        # Extract transcription
        transcription = ""
        for result in response.results:
            for alternative in result.alternatives:
                transcription += alternative.transcript + " "
        
        return transcription.strip() if transcription else None
        
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe_audio.py <audio_file_path>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    result = transcribe_audio(audio_file)
    
    if result:
        print(result)
    else:
        print("❌ No transcription available")
