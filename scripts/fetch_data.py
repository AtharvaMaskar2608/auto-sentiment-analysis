# Importing Libraries 
import pandas as pd 

# GLOBAL VARIABLES 
CALL_RECORDING_PATH = "/home/choice/Desktop/sentiment-analysis/data/call-recordings.csv"

# 1. Access the recordings file
call_recordings_df = pd.read_csv(CALL_RECORDING_PATH) 

# 2. Convert the dataframe to an array of objects
call_recordings = call_recordings_df.to_dict('records')

print(call_recordings)

