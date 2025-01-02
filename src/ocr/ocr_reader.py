import easyocr
import os
import json
import re

def validate_plate_number(plate_text):
    """
    Validasi format plat nomor Indonesia.
    Format umum: B 1234 XYZ
    """
    pattern = r'^[A-Z]{1,2}\s\d{1,4}\s[A-Z]{1,3}$'
    if re.match(pattern, plate_text):
        return True
    return False


def read_text_from_image(image_path):
    """
    Membaca teks dari gambar ROI menggunakan EasyOCR.
    """
    reader = easyocr.Reader(['en', 'id'], gpu=True)  # Gunakan GPU jika tersedia
    results = reader.readtext(image_path, detail=1)

    # Gabungkan semua hasil OCR menjadi string
    if results:
        text = " ".join([res[1] for res in results])
        print(f"Teks yang terdeteksi: {text}")

        # Membagi teks menjadi tiga bagian
        parts = text.split()
        if len(parts) == 3:
            part1, part2, part3 = parts[0], parts[1], parts[2]

            # Aturan untuk array pertama
            if part1 == '0':
                part1 = 'D'
            elif part1 == '6':
                part1 = 'G'
            elif part1 == '4':
                part1 = 'A'

            # Aturan untuk array kedua
            if not part3.isdigit():
                part3 = ''.join(['0' if char.isalpha() else char for char in part3])

            # Gabungkan kembali bagian-bagian yang telah diubah
            modified_text = f"{part1} {part2} {part3}"
            print(f"Teks yang telah dimodifikasi: {modified_text}")
            return modified_text
        else:
            print("Teks tidak sesuai format yang diharapkan (3 bagian).")
            print(f"Teks yang terdeteksi: {text}")
            return text
        
    else:
        print(f"Tidak ada teks yang terdeteksi pada {image_path}")
        return ""


def process_ocr(input_dir, output_file):
    """
    Melakukan OCR pada semua gambar di folder ROI.
    """
    ocr_results = {}
    for image_file in os.listdir(input_dir):
        if image_file.endswith(".bmp") or image_file.endswith(".png"):
            image_path = os.path.join(input_dir, image_file)
            print(f"Memproses OCR pada: {image_file}")
            text = read_text_from_image(image_path)

            # Validasi hasil OCR
            is_valid = validate_plate_number(text)
            ocr_results[image_file] = {
                "text": text,
                "is_valid": is_valid
            }

    # Simpan hasil OCR ke file JSON
    with open(output_file, 'w') as file:
        json.dump(ocr_results, file, indent=4)
    print(f"Hasil OCR disimpan di: {output_file}")


if __name__ == "__main__":
    input_dir = "./data/train/roi"  # Folder ROI hasil deteksi
    output_file = "./data/output/ocr_results_new.json"  # File hasil OCR
    process_ocr(input_dir, output_file)
