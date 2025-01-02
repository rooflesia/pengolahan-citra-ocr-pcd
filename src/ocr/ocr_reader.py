import easyocr
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import os


def debug_image(image_path):
    """
    Menampilkan gambar yang akan diproses untuk OCR.
    """
    img = Image.open(image_path)
    plt.imshow(img, cmap='gray')
    plt.title("Input Image for OCR")
    plt.axis('off')
    plt.show()


def enhance_contrast(image_path, output_path):
    """
    Meningkatkan kontras gambar untuk membuat teks lebih jelas.
    """
    img = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2) 
    img.save(output_path)
    return output_path


def read_text_from_image(image_path):
    """
    Membaca teks dari gambar menggunakan EasyOCR.
    """
    reader = easyocr.Reader(['en', 'id'], gpu=True)  # Gunakan model bahasa Inggris dan Indonesia
    results = reader.readtext(image_path, detail=1, decoder='greedy')

    # Debugging hasil OCR
    if results:
        for (bbox, text, prob) in results:
            print(f"Bounding Box: {bbox}, Teks: '{text}', Confidence: {prob}")
        return " ".join([res[1] for res in results])  # Gabungkan semua teks yang terdeteksi
    else:
        print("Tidak ada teks yang terdeteksi.")
        return ""


def process_ocr(input_dir, output_dir):
    """
    Memproses semua gambar di folder ROI dan menyimpan hasil OCR ke file.
    """
    os.makedirs(output_dir, exist_ok=True)  # Pastikan folder output ada
    ocr_results = {}

    for image_file in os.listdir(input_dir):
        if image_file.endswith(".jpg") or image_file.endswith(".png"):
            image_path = os.path.join(input_dir, image_file)
            
            # Debug gambar awal
            print(f"\nMemproses gambar: {image_file}")
            debug_image(image_path)

            # Langkah tambahan: Tingkatkan kontras
            enhanced_path = enhance_contrast(image_path, f"{output_dir}/enhanced_{image_file}")

            # OCR
            plate_text = read_text_from_image(enhanced_path)
            print(f"Hasil OCR untuk {image_file}: {plate_text}")

            # Simpan hasil OCR
            ocr_results[image_file] = plate_text

    # Simpan semua hasil ke file JSON
    output_json_path = os.path.join(output_dir, "ocr_results.json")
    with open(output_json_path, 'w') as file:
        import json
        json.dump(ocr_results, file, indent=4)

    print(f"Hasil OCR disimpan di: {output_json_path}")


if __name__ == "__main__":
    input_dir = "./data/processed/train/roi"  # Folder gambar ROI
    output_dir = "./data/output/ocr_debug"   # Folder untuk hasil debugging dan OCR
    process_ocr(input_dir, output_dir)
