from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def preprocess_speaker_transcript(transcript: str, agentName: str) -> str:
    """
    Description:
        - This function takes the script which is in the format of Speaker A & Speaker B and replaces them with actual names of the speaker. 

    parameters:
        - transcript (str): Call transcript
        - agentName (str): Name of the agent

    returns:   
        - processed_transcript (str): Processed trancript will be in the following format, AgentName & Customer  
    """

    system_prompt = f"You are a transcript which is in the following format: <Speaker A>: <Text> <Speaker B>: <Text>. From the transcript you have to identify who the agent is. Name of the company agent is: {agentName}. Understand the context and do not assume anything from any speaker, purely work on the transcript. Return `Speaker A` if you think speaker A is the agent, or return `Speaker B` if you think the speaker B is the agent. Strictly reply in `Speaker A` or `Speaker B` only always without any explanation or additional text."

    user_prompt = f"For the given transcript: {transcript}, return `Speaker A` if you think Speaker A is the agent and Speaker B is the customer. Return `Speaker B` if you think speaker B is the agent and the Speaker A is the customer."

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    if completion.choices[0].message.content == "Speaker A":
        processed_transcripts = pre_process_text(transcript=transcript, agentName=agentName, agentTag="Speaker A", customerTag="Speaker B")
    elif completion.choices[0].message.content == "Speaker B":
        processed_transcripts = pre_process_text(transcript=transcript, agentName=agentName, agentTag="Speaker B", customerTag="Speaker A")

    return processed_transcripts         

def pre_process_text(transcript: str, agentName: str, agentTag: str, customerTag: str)  -> str:
    """
    Description:
        - This function returns the processed transcripts with names. 
    
    parameters:
        - transcript (str): Call transcript
        - agentName (str): Name of the agent
        - agentTag (str): What to replace the agent name with Speaker A or B
        - customerTag (str): What to replace customer with
    returns:
        - processed_transcript (str): Processed transcripts. 
    """

    # 1. Replacing agentTag with agentName

    processed_transcripts = transcript.replace(agentTag, f"Agent {agentName}: ")


    # 2. Replacing customer Tag with Customer
    processed_transcripts = processed_transcripts.replace(customerTag, "Customer")

    return processed_transcripts
