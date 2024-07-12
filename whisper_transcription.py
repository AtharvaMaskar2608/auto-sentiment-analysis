from openai import OpenAI
import os 
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

from openai import OpenAI
client = OpenAI()

audio_file= open("/home/choice/Desktop/sentiment-analysis/data/call_recording/f287abd1-7150-45cb-985f-abadedcb7ccb.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)

audio_file= open("/home/choice/Desktop/sentiment-analysis/data/call_recording/f287abd1-7150-45cb-985f-abadedcb7ccb.mp3", "rb")
translation = client.audio.translations.create(
  model="whisper-1", 
  file=audio_file, 
)
print(translation.text)