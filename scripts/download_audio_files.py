import requests
import os
AUDIO_BASE_FOLDER_PATH = "/home/choice/Desktop/sentiment-analysis/data/call_recording/"
def fetch_audio_files(audio_file_url: str) -> True:
    """
    Description:
        - This function takes the audio file url, fetches the audio file and saves it in the data directoy

    Parameters:
        - audio_file_url (str): Url of the audio file

    returns:
        - result (bool): Returns true if the audio was saved successfully else returns false. 
    """

    # 1. fetch audio name 
    audio_id = audio_file_url.split('/')[-1]

    # 2. Performing fetch request 
    url = audio_file_url

    # Ensure the folder exists; create if it doesn't
    os.makedirs(AUDIO_BASE_FOLDER_PATH, exist_ok=True)

    file_name = f"{AUDIO_BASE_FOLDER_PATH}{audio_id}.mp3" 

    try:
        response = requests.get(url)

        if response.status_code == 200:
            file_path = os.path.join(AUDIO_BASE_FOLDER_PATH, file_name)
            with open(file_path, 'wb') as audioFile:
                audioFile.write(response.content)
            return True
        else:
            print("Failed to download file. Status Code: ", response.status_code)                
    except Exception as e:
        print("Error fetching audio file from source: ", e)