import os
from dotenv import load_dotenv
import requests

# Text to voice and we get the voice from Elvenlabs
class TTS():
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('ELEVENLABS_API_KEY')
    
    def process(self, text):
        CHUNK_SIZE = 1024
        url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.key
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v1",
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.55
            }
        }

        file_name = "response.mp3"

        try:
            # Request POST with stream=True
            response = requests.post(url, json=data, headers=headers, stream=True)
            response.raise_for_status()  #error against not succesfull answer
            
            #Itsaves the file on the static folder to it can be readed by flask
            with open("static/" + file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
            
            return file_name
        
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud POST: {e}")
            return None
