import whisper
import os

model = whisper.load_model("large")
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg"


async def extract_text_from_audio(audio_path: str) -> str:
    # Transcribe the audio file
    result = model.transcribe(audio_path)

    # Get the transcription
    transcription = result["text"]

    # Return the transcription
    return transcription
