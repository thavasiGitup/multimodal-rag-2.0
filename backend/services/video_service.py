from moviepy import VideoFileClip
from openai import OpenAI
from backend.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_audio(video_path):
    video = VideoFileClip(video_path)
    audio_path = video_path + ".mp3"
    video.audio.write_audiofile(audio_path)
    return audio_path


def transcribe_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text
