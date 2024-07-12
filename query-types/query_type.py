from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def generate_summary(transcript: str) -> str:
    """
    Description:
        - This function takes the transcript and generates summary useful for query function.

    parameters:
        - transcript (str): Call transcript

    returns:
        - summary (str): Summary that is useful for query type.
    """

    system_prompt = """You are a professional transcript analyzer for a finance platform. For a given call transcript between the customer support agent and the client/customer you have to generate a brief to the point summary the covers the following points: 
    
    - What was the customer's query?
    - What was the actual reason/cause behind the problem (according to the agent) 
    - how did the agent solve the problem.
    """
    user_prompt = f"Give a summary for the given transcript: {transcript}"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return completion.choices[0].message.content


def get_main_query(summary: str) -> str:
    """
    Description:
        - This function takes the transcript and summary and returns which query type it belongs to.

    parameters:
        - summary: Special summary generated for query type.

    returns:
        - main_query_type: Main query type. 
    """

    main_query_description = None

    with open("/home/choice/Desktop/sentiment-analysis/query-types/main_query_2.json", 'r') as jsonFile:
        main_query_description = json.load(jsonFile)

    system_prompt = f"You are a professional transcript analyzer for a finance platform, for a given transcript summary between the platform agent and the customer categorize the problem in the query type from the given list: {main_query_description}. Just return the name of the query and nothing else."        

    user_prompt = f"For the given transcript summary return the matching query name that matches the description: {summary}"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return completion.choices[0].message.content
    