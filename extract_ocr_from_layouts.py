# engine/extract_ocr_from_layouts.py

import os
import json
import cv2
from paddleocr import PaddleOCR
import layoutparser as lp
from tqdm import tqdm

# Paths
image_dir = "data/images"
layout_dir = "data/extracted/layouts"
ocr_output_dir = "data/extracted/ocr"
os.makedirs(ocr_output_dir, exist_ok=True)

# Load PaddleOCR
ocr_model = PaddleOCR(use_angle_cls=True, lang='en')  # Use GPU if available

def load_layout(json_path):
    with open(json_path, 'r') as f:
        blocks = json.load(f)
    return [
        lp.TextBlock(
            lp.Rectangle(b['x_1'], b['y_1'], b['x_2'], b['y_2']),
            type=b.get('type', 'Text'),
            score=b.get('score', None)
        )
        for b in blocks
    ]


def run_ocr_on_layout_blocks(image_path, layout_blocks):
    image = cv2.imread(image_path)
    ocr_results = []

    for i, block in enumerate(layout_blocks):
        x1, y1, x2, y2 = map(int, block.block.coordinates)
        cropped = image[y1:y2, x1:x2]
        result = ocr_model.predict(cropped)


        text = "\n".join([line[1][0] for line in result[0]]) if result and result[0] else ""

        ocr_results.append({
            "block_index": i,
            "type": block.type,
            "bbox": [x1, y1, x2, y2],
            "text": text.strip()
        })

    return ocr_results

def process_all():
    for img_name in tqdm(sorted(os.listdir(image_dir))):
        if not img_name.lower().endswith((".png", ".jpg")):
            continue

        page_id = os.path.splitext(img_name)[0]
        img_path = os.path.join(image_dir, img_name)
        layout_path = os.path.join(layout_dir, f"{page_id}.json")
        ocr_output_path = os.path.join(ocr_output_dir, f"{page_id}.json")

        if not os.path.exists(layout_path):
            print(f"❌ Layout not found for {page_id}")
            continue

        layout_blocks = load_layout(layout_path)
        ocr_results = run_ocr_on_layout_blocks(img_path, layout_blocks)

        with open(ocr_output_path, "w", encoding="utf-8") as f:
            json.dump(ocr_results, f, indent=2, ensure_ascii=False)

        print(f"[✓] OCR saved for {page_id}")

if __name__ == "__main__":
    process_all()
