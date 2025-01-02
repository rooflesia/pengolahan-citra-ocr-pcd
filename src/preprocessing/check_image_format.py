from PIL import Image
import os

def check_image_format(image_path):
    """
    Memeriksa format gambar, mode warna, dan memastikan 8-bit grayscale.
    """
    try:
        img = Image.open(image_path)
        print(f"File: {image_path}")
        print(f"Format: {img.format}, Mode: {img.mode}, Size: {img.size}")
        if img.format == "BMP" and img.mode == "L":
            print("Gambar sudah dalam format BMP 8-bit grayscale.")
            return True
        else:
            print("Gambar TIDAK dalam format BMP 8-bit grayscale.")
            return False
    except Exception as e:
        print(f"Error membuka gambar {image_path}: {e}")
        return False

if __name__ == "__main__":
    input_dir = "./data/processed/bmp_grayscale"
    for image_file in os.listdir(input_dir):
        if image_file.endswith((".bmp", ".jpg", ".png")):
            image_path = os.path.join(input_dir, image_file)
            check_image_format(image_path)
