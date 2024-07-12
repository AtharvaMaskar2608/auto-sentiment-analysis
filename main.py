# Importing libraries
import pandas as pd
from sqlalchemy import create_engine


# Importing utils
from utils import *
from dotenv import load_dotenv

load_dotenv()

CALL_RECORDINGS_EXCEL_PATH = "data/call-recordings.csv"
CSV_FILE_PATH = "/home/choice/Desktop/sentiment-analysis/output/audio_analysis.csv"


MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOSTNAME = os.getenv("MYSQL_HOSTNAME")
MYSQL_DATABASE_NAME = os.getenv("MYSQL_DATABASE_NAME")

# MYSQL_URL = f"mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE_NAME}"
# engine = create_engine(MYSQL_URL)

def main():
    # 1. Read the excel file using pandas. 
    call_recordings_df = pd.read_csv(CALL_RECORDINGS_EXCEL_PATH)

    # 2. Convert the call recordings csv to dict
    call_recordings = call_recordings_df.to_dict('records')

    master_data = []

    # 3. Iterating through the audio files, and performing operations
    for i, call_recording in enumerate(call_recordings):
         # 3.1 Get transcripts and agent Name
        transcripts = generate_transcripts(call_recording['Audio Urls'])
        audio_url = call_recording["Audio Urls"]
        agent_name = call_recording['Caller Name']
        # 3.2 Pre-process transcripts
        audio_transcripts = ""
        try:
            for transcript in transcripts:
                audio_transcripts += f"Speaker {transcript.speaker}: {transcript.text}\n"

            audio_transcripts = preprocess_speaker_transcript(audio_transcripts, agent_name)

            # 3.2 Generate summary for the transcript
            summary = generate_sumary(transcript=audio_transcripts, agentName=agent_name)
            print(f"## Generated Summary!")

            # 3.3 Check if the agent greeted
            didGreet = check_greeting(transcript=audio_transcripts, summary=summary)
            print(f"## Checked Greeting!")


            # 3.4 Mark empathy score
            empathy_score = check_empathy(transcript=audio_transcripts, summary=summary)
            print("## Marked Empathy score!")

            # 3.5 Mark Closure score
            closure_score = check_closure(transcript=audio_transcripts, summary=summary)
            print(f"## Marked Closure")

            # 3.6 Check for query type
            query = get_query_type(transcript=audio_transcripts)
            print(f"## Fetched Query Type")

            # 3.7 Create the data object
            data = {
                "Audio Urls": audio_url,
                "Sr. No.": call_recording['Sr. No.'], 
                "Caller Name": call_recording['Caller Name'],
                "Date": call_recording['Date'], 
                "Ticket ID": call_recording['Ticket ID'], 
                "Client ID": call_recording["Client ID"],
                "Expected Type of Query": call_recording['Type of Query'], 
                "Predicted Type of Query": query, 
                "Expected Greetings": call_recording['Greetings'], 
                "Predicted Greetings": didGreet,
                "Expected Empathy Score": call_recording['Empathy talking'], 
                "Predicted Empathy Score": empathy_score, 
                "Expected Closure": call_recording['further assistance/Closure'], 
                "Predicted Closure": closure_score, 
                "Expected Total": int(call_recording['Greetings']) + int(call_recording['Empathy talking']) + int(call_recording['further assistance/Closure']),
                "Total": int(didGreet) + int(empathy_score) + int(closure_score), 
                "Original Remark": call_recording['Remark'], 
                "Transcript": audio_transcripts, 
                "Summary": summary
            }
        
            # 3.7 Append the data to the master data list
            master_data.append(data)
            print(f"Processed {i+1}/{len(call_recordings)} files")

            if i % 10 == 0:
                master_df = pd.DataFrame(master_data)  
                # 4.2 Saving the master dataframe to csv format
                master_df.to_csv(CSV_FILE_PATH, index=False)
                print("Dataframe saved to sheets")  
                print(f"step: {i}")
        except Exception as e:
            print("Error but passing: ", e)
            print(audio_url)
            pass
    # 4. Save it to a local database and in csv files.

    # 4.1 convert the list of dict to pandas dataframe
    master_df = pd.DataFrame(master_data)         

    # 4.2 Saving the master dataframe to csv format
    master_df.to_csv(CSV_FILE_PATH, index=False)
    print("Dataframe saved to sheets")

if __name__ == "__main__":
    main()