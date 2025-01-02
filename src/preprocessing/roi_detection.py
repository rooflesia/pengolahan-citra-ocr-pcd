from PIL import Image
import json
import os

def parse_location_tag(location_string):
    """
    Mengonversi string lokasi seperti <loc0176><loc0022><loc0738><loc0844>
    menjadi bounding box (x_min, y_min, x_max, y_max).
    """
    # Pisahkan string menjadi elemen bounding box
    loc_tags = location_string.strip().split("><")
    cleaned_tags = []

    for tag in loc_tags:
        # Bersihkan elemen dan pastikan hanya angka yang diambil
        cleaned_tag = tag.replace("<loc", "").replace(">", "").strip()
        # Ambil hanya bagian numerik sebelum karakter non-numerik
        numeric_part = ''.join(filter(str.isdigit, cleaned_tag))
        if numeric_part:
            cleaned_tags.append(numeric_part)

    # Pastikan jumlah elemen adalah 4
    if len(cleaned_tags) == 4:
        try:
            # Konversi elemen menjadi integer
            x_min, y_min, x_max, y_max = map(int, cleaned_tags)
            return x_min, y_min, x_max, y_max
        except ValueError as e:
            raise ValueError(f"Error mengonversi elemen menjadi integer: {cleaned_tags}. Error: {e}")
    else:
        raise ValueError(f"Format lokasi tidak valid: {location_string}. Harus memiliki 4 elemen valid.")

def crop_roi_from_location(image_path, location_string, output_path):
    """
    Memotong area plat nomor (ROI) berdasarkan string lokasi.
    """
    try:
        # Parse lokasi menjadi bounding box
        x_min, y_min, x_max, y_max = parse_location_tag(location_string)

        # Crop gambar
        image = Image.open(image_path)
        roi = image.crop((x_min, y_min, x_max, y_max))
        roi.save(output_path)
        print(f"ROI disimpan di: {output_path}")
    except Exception as e:
        print(f"Error memproses {image_path}: {e}")

def process_images_with_locations(jsonl_file, input_dir, output_dir):
    """
    Membaca file JSONL dan memotong ROI berdasarkan string lokasi untuk setiap gambar.
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(jsonl_file, "r") as file:
        for line in file:
            annotation = json.loads(line.strip())

            # Cari lokasi string di JSON
            for message in annotation.get("messages", []):
                if message["role"] == "assistant" and "content" in message:
                    location_string = message["content"]  # Ambil string lokasi
                    break
            else:
                print("String lokasi tidak ditemukan di JSON.")
                continue

            # Cari URL gambar
            for message in annotation.get("messages", []):
                if "content" in message and isinstance(message["content"], list):
                    for item in message["content"]:
                        if item.get("type") == "image_url":
                            image_url = item["image_url"]["url"]
                            image_name = "/".join(image_url.split("/")[-2:]).replace("/", "_") + ".jpg"
                            image_path = os.path.join(input_dir, image_name)

                            # Proses gambar jika ditemukan
                            if os.path.exists(image_path):
                                output_path = os.path.join(output_dir, f"roi_{image_name}")
                                crop_roi_from_location(image_path, location_string, output_path)
                            else:
                                print(f"Gambar tidak ditemukan: {image_name}")

if __name__ == "__main__":
    jsonl_file = "./data/raw/annotations/_annotations.train.jsonl"  # File JSONL
    input_dir = "./data/raw/images"  # Folder gambar asli
    output_dir = "./data/processed/train/roi"  # Output folder ROI
    process_images_with_locations(jsonl_file, input_dir, output_dir)
