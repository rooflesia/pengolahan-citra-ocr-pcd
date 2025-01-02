import json
import pandas as pd

def process_files(json_file_path, csv_file_path, output_json_path):
    # Load JSON
    with open(json_file_path, "r") as f:
        json_data = [json.loads(line) for line in f.readlines()]

    # Load CSV
    csv_data = pd.read_csv(csv_file_path)

    # Extract unique hash functions
    def extract_hash_from_json_url(url):
        return url.split("/")[-2]

    def extract_hash_from_csv_filename(filename):
        return filename.split(".rf.")[-1].split(".")[0]

    # Create a dictionary from CSV for quick lookup
    csv_dict = {
        extract_hash_from_csv_filename(row["filename"]): {
            "width": row["width"],
            "height": row["height"],
            "xmin": row["xmin"],
            "ymin": row["ymin"],
            "xmax": row["xmax"],
            "ymax": row["ymax"],
        }
        for _, row in csv_data.iterrows()
    }

    # Combine JSON and CSV data with filtered keys
    filtered_combined_data = []
    for entry in json_data:
        for msg in entry["messages"]:
            if "content" in msg and isinstance(msg["content"], list):
                url = msg["content"][0]["image_url"]["url"]
                unique_hash = extract_hash_from_json_url(url)

                if unique_hash in csv_dict:
                    filtered_entry = {
                        "url": url,
                        "width": csv_dict[unique_hash]["width"],
                        "height": csv_dict[unique_hash]["height"],
                        "xmin": csv_dict[unique_hash]["xmin"],
                        "ymin": csv_dict[unique_hash]["ymin"],
                        "xmax": csv_dict[unique_hash]["xmax"],
                        "ymax": csv_dict[unique_hash]["ymax"],
                    }
                    filtered_combined_data.append(filtered_entry)

    # Save filtered combined data to JSON
    with open(output_json_path, "w") as f:
        json.dump(filtered_combined_data, f, indent=4)

    print(f"Filtered combined JSON saved to {output_json_path}")

# Process each dataset
datasets = [
    ("_annotations.test.jsonl", "test.csv", "test.json"),
    ("_annotations.train.jsonl", "train.csv", "train.json"),
    ("_annotations.valid.jsonl", "valid.csv", "valid.json"),
]

for json_file, csv_file, output_file in datasets:
    process_files(json_file, csv_file, output_file)