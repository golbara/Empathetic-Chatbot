import requests
import json
import os
# Download the dataset
def download_dataset(url, output_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'w') as file:
            file.write(response.text)
        print(f"Dataset downloaded successfully to {output_path}")
    else:
        print(f"Failed to download dataset. Status code: {response.status_code}")

# Calculate the mean for a specified field
def calculate_mean(data, field_name):
    values = [entry.get(field_name, 0) for entry in data]
    return sum(values) / len(values) if values else 0

# Main execution
if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Replace with the actual URL of your dataset
    dataset_url = "https://huggingface.co/datasets/keenGol/processed_semantic-search-channels/resolve/main/feedback_dataset.json"
    dataset_path = f"{current_directory}/data/feedback_dataset_server.json"

    # Step 1: Download the dataset
    download_dataset(dataset_url, dataset_path)

    # Step 2: Load the dataset
    with open(dataset_path, "r") as f:
        feedback_data = json.load(f)

    # Step 3: Calculate metrics
    mean_mrr = calculate_mean(feedback_data, "MRR")
    mean_precision = calculate_mean(feedback_data, "precision")

    # Step 4: Output the results
    print(f"Mean MRR: {mean_mrr:.4f}")
    print(f"Mean Precision: {mean_precision:.4f}")
