import json
import requests
import os

def download_images_with_custom_names(jsonl_file, output_dir):
    """
    Mendownload gambar dari URL di file JSONL dan menyimpannya secara lokal dengan nama sesuai bagian unik dari URL.
    """
    os.makedirs(output_dir, exist_ok=True)  # Pastikan folder output ada
    
    with open(jsonl_file, 'r') as file:
        for line in file:
            annotation = json.loads(line.strip())  # Baca tiap baris JSONL
            for message in annotation.get("messages", []):
                if "content" in message and isinstance(message["content"], list):
                    for item in message["content"]:
                        if item.get("type") == "image_url":
                            image_url = item["image_url"]["url"]
                            
                            # Ekstrak bagian unik dari URL (setelah domain)
                            unique_name = "/".join(image_url.split("/")[-2:]).replace("/", "_")
                            image_name = f"{unique_name}.jpg"
                            output_path = os.path.join(output_dir, image_name)
                            
                            # Download gambar
                            print(f"Mendownload {image_url} sebagai {output_path}")
                            response = requests.get(image_url)
                            if response.status_code == 200:
                                with open(output_path, 'wb') as img_file:
                                    img_file.write(response.content)
                            else:
                                print(f"Gagal mendownload {image_url}, status: {response.status_code}")

if __name__ == "__main__":
    # Path ke file JSONL dan direktori output
    jsonl_file = "./data/raw/annotations/_annotations.train.jsonl"
    output_dir = "./data/raw/images"
    download_images_with_custom_names(jsonl_file, output_dir)
