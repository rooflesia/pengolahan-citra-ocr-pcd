from PIL import Image
import json
import os

def crop_roi(image_path, xmin, ymin, xmax, ymax, output_path):
    """
    Memotong area ROI (Region of Interest) berdasarkan koordinat bounding box.
    """
    try:
        # Buka gambar dan crop ROI
        image = Image.open(image_path)
        roi = image.crop((xmin, ymin, xmax, ymax))
        roi.save(output_path)
        print(f"ROI disimpan di: {output_path}")
    except Exception as e:
        print(f"Error memproses {image_path}: {e}")

def process_images_from_json(json_file, input_dir, output_dir):
    """
    Membaca file JSON dan memotong ROI berdasarkan koordinat bounding box untuk setiap gambar.
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(json_file, "r") as file:
        annotations = json.load(file)

        for idx, annotation in enumerate(annotations):
            # Ambil informasi bounding box dan URL gambar
            xmin, ymin, xmax, ymax = annotation["xmin"], annotation["ymin"], annotation["xmax"], annotation["ymax"]
            image_url = annotation["url"]

            # Nama file gambar dan path input/output
            image_name = f"preprocessed_image_{idx}.bmp"
            image_path = os.path.join(input_dir, image_name)
            output_path = os.path.join(output_dir, f"roi_{image_name}")

            # Periksa keberadaan gambar, lalu proses
            if os.path.exists(image_path):
                crop_roi(image_path, xmin, ymin, xmax, ymax, output_path)
            else:
                print(f"Gambar tidak ditemukan: {image_path}")

if __name__ == "__main__":
    json_file = "./data/raw/annotations/train.json"  # File JSON dataset
    # input_dir = "./data/raw/images"  # Folder gambar asli
    input_dir = "./data/processed/manual_preprocessed_new"  # Folder gambar asli
    output_dir = "./data/train/roi"  # Output folder ROI
    process_images_from_json(json_file, input_dir, output_dir)