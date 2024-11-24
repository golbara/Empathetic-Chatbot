import pandas as pd
import json
import os
def load_dataset(filename="saved_data.csv"):
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Path to the Streamlit script in the current directory
    path = os.path.join(current_directory, filename)
    # path = "/Users/golbarg/Documents/bachelor proj/Empathetic-Chatbot/bot/saved_data.csv"
    # Read the CSV file into a DataFrame
    df = pd.read_csv(path)
    
    # Deserialize JSON-encoded fields
    if "selected_messages" in df.columns:
        df["selected_messages"] = df["selected_messages"].apply(json.loads)
    if "sorted_indices" in df.columns:
        df["sorted_indices"] = df["sorted_indices"].apply(json.loads)
    print(df.head(5))
    return df
load_dataset()