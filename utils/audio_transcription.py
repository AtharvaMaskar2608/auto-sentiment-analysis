from typing import List, Dict
import os

# Importing Assembly AI libraries 
import assemblyai as aai

from dotenv import load_dotenv

load_dotenv()

def generate_transcripts(audio_file_path: str) -> List[Dict[str, str]]:
    """
    Description:
        - This function uses the assembly AI API to take an audio file and transcribe it. 

    parameters:
        - audio_file_path (str): path of the audio file 
    
    returns:
        - transcripts (arr): Array of dictionary of transcripts
    """

    try:
        aai.settings.api_key = os.getenv("ASSEMBLY_AI_API_KEY")

        config = aai.TranscriptionConfig(language_code='hi', speaker_labels=True, speakers_expected=2, punctuate=True)

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(
            audio_file_path,
            config=config
        )

        return transcript.utterances

    except Exception as e:
        print(audio_file_path)
        print("Problem transcribing audio: ", e)
        pass