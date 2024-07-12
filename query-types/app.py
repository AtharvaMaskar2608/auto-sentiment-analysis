from query_type import *

transcript = ""

with open("transcript.txt", 'r') as file:
    transcript = file.read()

summary = generate_summary(transcript=transcript)
print(summary)

query_type = get_main_query(summary=summary)
print(query_type)