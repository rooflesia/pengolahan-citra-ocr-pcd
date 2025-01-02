from PIL import Image, ImageFilter
import os
import json

def apply_gaussian_blur(image_path, output_path):
    """
    Menghapus noise menggunakan Gaussian Blur.
    """
    try:
        image = Image.open(image_path).convert("L")  # Ubah ke grayscale
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=1))  # Terapkan Gaussian Blur
        blurred_image.save(output_path)
        print(f"Gaussian Blur diterapkan: {output_path}")
    except Exception as e:
        print(f"Error memproses {image_path}: {e}")

def process_images_with_noise_reduction(json_file, input_dir, output_dir):
    """
    Memproses semua gambar dalam dataset JSON dengan Gaussian Blur.
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(json_file, "r") as file:
        annotations = json.load(file)

        for idx, annotation in enumerate(annotations):
            image_name = f"image_{idx}.jpg"
            input_path = os.path.join(input_dir, image_name)
            output_path = os.path.join(output_dir, image_name)

            if os.path.exists(input_path):
                apply_gaussian_blur(input_path, output_path)
            else:
                print(f"Gambar tidak ditemukan: {input_path}")

if __name__ == "__main__":
    json_file = "./data/raw/annotations/train.json"  # File JSON dataset
    input_dir = "./data/raw/images"  # Folder gambar input
    output_dir = "./data/processed/train"  # Folder output untuk gambar yang telah diproses
    process_images_with_noise_reduction(json_file, input_dir, output_dir)