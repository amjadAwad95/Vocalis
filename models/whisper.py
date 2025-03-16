import whisper
import os
from module.model import Model

model = whisper.load_model("large")
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg"


class Whisper(Model):
    def __init__(self, audio_path):
        self.audio_path = audio_path

    async def run(self):
        result = model.transcribe(self.audio_path)

        transcription = result["text"]

        return transcription
