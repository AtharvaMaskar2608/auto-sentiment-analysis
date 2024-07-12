import pandas as pd
from query_type import *


csv_file_path = "/home/choice/Desktop/sentiment-analysis/query-types/sentiment_analysis.csv"


df = pd.read_csv(csv_file_path)

df['V2 Predictions'] = None


for index, row in df.iterrows():
    # 1. Take the transcript
    transcript = row['Transcript']

    # 2. Generate a summary
    summary = generate_summary(transcript=transcript)
    print(f"Summary generated for {index}: {summary}")

    # 3. Get query type
    query_type = get_main_query(summary=summary)
    print(f"Query type generated for {index}: {query_type}")

    # Update in dataframe
    df.at[index, 'V2 Predictions'] = query_type

    df.to_csv("final_update.csv", index=False)