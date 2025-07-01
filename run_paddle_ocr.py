import os
import cv2
import json
from paddleocr import PaddleOCR
from tqdm import tqdm

def run_ocr_on_detected_text(image_dir, layout_dir, output_dir):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    os.makedirs(output_dir, exist_ok=True)

    for filename in tqdm(os.listdir(image_dir), desc="Running OCR"):
        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        image_path = os.path.join(image_dir, filename)
        layout_path = os.path.join(layout_dir, f"{os.path.splitext(filename)[0]}.json")

        if not os.path.exists(layout_path):
            continue

        image = cv2.imread(image_path)
        with open(layout_path, "r") as f:
            layout_blocks = json.load(f)

        results = []
        for block in layout_blocks:
            if block["type"] not in ["Text", "Title"]:
                continue

            x1, y1, x2, y2 = block["coordinates"]
            cropped = image[y1:y2, x1:x2]

            ocr_result = ocr.ocr(cropped, cls=True)
            for line in ocr_result[0]:
                text = line[1][0]
                score = float(line[1][1])
                results.append({
                    "text": text,
                    "score": score,
                    "bbox": block["coordinates"]
                })

        output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    image_dir = "data/images"
    layout_dir = "data/extracted/layouts"
    output_dir = "data/extracted/ocr"
    run_ocr_on_detected_text(image_dir, layout_dir, output_dir)
