from PIL import Image
import os

def convert_to_bmp_grayscale(input_path, output_path):
    """
    Mengonversi gambar ke BMP 8-bit grayscale.
    """
    try:
        img = Image.open(input_path)
        img = img.convert("L")  # Ubah ke grayscale (mode 'L')
        img.save(output_path, format="BMP")
        print(f"Berhasil mengonversi {input_path} ke {output_path}")
    except Exception as e:
        print(f"Error mengonversi gambar {input_path}: {e}")

if __name__ == "__main__":
    input_dir = "./data/raw/images"
    output_dir = "./data/processed/bmp_grayscale"
    os.makedirs(output_dir, exist_ok=True)

    for image_file in os.listdir(input_dir):
        if image_file.endswith((".jpg", ".png")):
            input_path = os.path.join(input_dir, image_file)
            output_path = os.path.join(output_dir, os.path.splitext(image_file)[0] + ".bmp")
            convert_to_bmp_grayscale(input_path, output_path)
