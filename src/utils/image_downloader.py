import json
import requests
import os

def download_images_from_json(json_file, output_dir):
    """
    Mendownload gambar dari URL di file JSON dan menyimpannya secara lokal.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Baca file JSON
    with open(json_file, 'r') as file:
        annotations = json.load(file)

        for idx, annotation in enumerate(annotations):
            image_url = annotation["url"]
            image_name = f"image_{idx}.jpg"
            output_path = os.path.join(output_dir, image_name)

            print(f"Mendownload {image_url} sebagai {output_path}")
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(output_path, 'wb') as img_file:
                    img_file.write(response.content)
            else:
                print(f"Gagal mendownload {image_url}, status: {response.status_code}")

if __name__ == "__main__":
    json_file = "./data/raw/annotations/train.json"
    output_dir = "./data/raw/images"
    download_images_from_json(json_file, output_dir)