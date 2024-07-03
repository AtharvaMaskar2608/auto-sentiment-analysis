# Importing Libraries 
import pandas as pd 

# Importing utils 
from download_audio_files import fetch_audio_files

# GLOBAL VARIABLES 
CALL_RECORDING_PATH = "/home/choice/Desktop/sentiment-analysis/data/call-recordings.csv"

# 1. Access the recordings file
call_recordings_df = pd.read_csv(CALL_RECORDING_PATH) 

# 2. Convert the dataframe to an array of objects
call_recordings = call_recordings_df.to_dict('records')

# 3. Saving audio files from urls
for i, recording in enumerate(call_recordings):
    fetch_audio_files(recording['Audio Urls'])

    print(f"Downloaded: {i+1}/{len(call_recordings)} files\n")


