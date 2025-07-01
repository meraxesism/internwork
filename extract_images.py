import os
import json
from PIL import Image
import layoutparser as lp

def extract_figure_blocks(image_dir, layout_dir, output_dir, json_output_path):
    os.makedirs(output_dir, exist_ok=True)
    image_files = sorted(os.listdir(image_dir))
    extracted_data = []

    for img_file in image_files:
        if not img_file.endswith(".png"):
            continue

        page_number = int(os.path.splitext(img_file)[0].split('_')[-1])
        image_path = os.path.join(image_dir, img_file)
        layout_path = os.path.join(layout_dir, f"page_{page_number}.json")

        if not os.path.exists(layout_path):
            print(f"Layout not found for page {page_number}")
            continue

        with open(layout_path, "r", encoding='utf-8') as f:
            layout_json = json.load(f)

        img = Image.open(image_path)

        for block in layout_json.get("blocks", []):
            if block["type"] == "Figure":
                x1, y1, x2, y2 = map(int, block["bbox"])
                cropped_img = img.crop((x1, y1, x2, y2))

                fig_name = f"figure_p{page_number}_{x1}_{y1}.png"
                fig_path = os.path.join(output_dir, fig_name)
                cropped_img.save(fig_path)

                extracted_data.append({
                    "page": page_number,
                    "bbox": [x1, y1, x2, y2],
                    "image_file": fig_name
                })

    with open(json_output_path, "w", encoding='utf-8') as jf:
        json.dump(extracted_data, jf, indent=2)

    print(f"[✓] Extracted {len(extracted_data)} figure images.")

# Example usage:
if __name__ == "__main__":
    extract_figure_blocks(
        image_dir="data/images/",
        layout_dir="data/extracted/layouts/",
        output_dir="data/images_extracted/",
        json_output_path="data/extracted/images.json"
    )
