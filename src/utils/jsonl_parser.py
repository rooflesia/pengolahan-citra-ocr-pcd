import json

def parse_jsonl(jsonl_file):
    """Membaca file JSONL dan mengembalikan daftar anotasi."""
    data = []
    with open(jsonl_file, 'r') as file:
        for line in file:
            data.append(json.loads(line.strip()))
    return data

def process_annotations(jsonl_file, image_dir, output_dir):
    """Memproses anotasi untuk bounding box dan menyimpan hasil."""
    annotations = parse_jsonl(jsonl_file)
    
    for annotation in annotations:
        image_path = f"{image_dir}/{annotation['image']}"
        print(f"Memproses gambar: {image_path}")
        # Tambahkan logika preprocessing atau OCR di sini
    
if __name__ == "__main__":
    jsonl_file = "../data/raw/annotations/_annotations.train.jsonl"
    image_dir = "../data/raw/images"
    output_dir = "../data/processed/train"
    
    process_annotations(jsonl_file, image_dir, output_dir)
