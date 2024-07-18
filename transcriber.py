import openai

#It converts Audio unto text
class Transcriber:
    def __init__(self):
        pass

    #It always stores and reads from audio.mp3    
    #It uses whisper model on the cloud.
    def transcribe(self, audio):
        audio.save("audio.mp3")
        audio_file= open("audio.mp3", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript.text