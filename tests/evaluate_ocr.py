import json

def evaluate_ocr(ocr_results_file, ground_truth_file):
    """
    Evaluasi hasil OCR dengan membandingkan ground truth.
    """
    with open(ocr_results_file, 'r') as ocr_file, open(ground_truth_file, 'r') as gt_file:
        ocr_results = json.load(ocr_file)
        ground_truth = json.load(gt_file)

    correct = 0
    total = len(ground_truth)

    for image_name, gt_text in ground_truth.items():
        ocr_text = ocr_results.get(image_name, {}).get("text", "")
        if ocr_text == gt_text:
            correct += 1

    accuracy = correct / total * 100
    print(f"Akurasi OCR: {accuracy:.2f}%")
    return accuracy


if __name__ == "__main__":
    ocr_results_file = "./data/output/ocr_results.json"
    ground_truth_file = "./data/raw/annotations/ground_truth.json"
    evaluate_ocr(ocr_results_file, ground_truth_file)
