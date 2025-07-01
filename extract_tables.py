import os
import json
import cv2
import pandas as pd
from paddleocr import PaddleOCR
from tqdm import tqdm

def extract_tables(image_dir, layout_dir, output_dir):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    os.makedirs(output_dir, exist_ok=True)

    for filename in tqdm(os.listdir(image_dir), desc="Extracting Tables"):
        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        image_path = os.path.join(image_dir, filename)
        layout_path = os.path.join(layout_dir, f"{os.path.splitext(filename)[0]}.json")

        if not os.path.exists(layout_path):
            continue

        image = cv2.imread(image_path)
        with open(layout_path, "r") as f:
            blocks = json.load(f)

        tables = []
        for block in blocks:
            if block["type"] != "Table":
                continue

            x1, y1, x2, y2 = block["coordinates"]
            cropped = image[y1:y2, x1:x2]

            result = ocr.ocr(cropped, cls=True)
            text_lines = [line[1][0] for line in result[0]]
            tables.append({
                "bbox": block["coordinates"],
                "rows": text_lines
            })

        output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
        with open(output_path, "w") as f:
            json.dump(tables, f, indent=2)

if __name__ == "__main__":
    image_dir = "data/images"
    layout_dir = "data/extracted/layouts"
    output_dir = "data/extracted/tables"
    extract_tables(image_dir, layout_dir, output_dir)
