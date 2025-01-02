from PIL import Image, ImageFilter
import os

def apply_gaussian_blur(image_path, output_path):
    """
    Menghapus noise menggunakan Gaussian Blur.
    """
    image = Image.open(image_path).convert("L")  # Ubah ke grayscale
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=1))  # Terapkan Gaussian Blur
    blurred_image.save(output_path)
    print(f"Gaussian Blur diterapkan: {output_path}")

if __name__ == "__main__":
    input_dir = "./data/raw/images"  # Folder input
    output_dir = "./data/processed/train"  # Folder output
    os.makedirs(output_dir, exist_ok=True)
    
    for image_file in os.listdir(input_dir):
        if image_file.endswith(".jpg") or image_file.endswith(".png"):
            input_path = os.path.join(input_dir, image_file)
            output_path = os.path.join(output_dir, image_file)
            apply_gaussian_blur(input_path, output_path)
