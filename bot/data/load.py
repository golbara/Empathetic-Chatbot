from datasets import load_dataset
import os
# Download the dataset
    # Get the current directory of this script
current_directory = os.path.dirname(os.path.abspath(__file__))
df_processed = load_dataset("keenGol/chatbot", split="train")
df_processed.save_to_disk(current_directory)  # Save locally
