import os
import layoutparser as lp
import cv2
import json

def detect_layout_on_images(image_dir, output_dir):
    # Load custom Detectron2 model from local files
    model = lp.Detectron2LayoutModel(
        config_path="models/layout/config.yml",
        model_path="models/layout/model_final.pth",
        extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
        label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
    )

    # Make sure output folder exists
    os.makedirs(output_dir, exist_ok=True)

    # Loop through all images in the image_dir
    for img_file in os.listdir(image_dir):
        if img_file.lower().endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(image_dir, img_file)
            image = cv2.imread(img_path)

            layout = model.detect(image)

            # Save layout as JSON for later use
            layout_data = [b.to_dict() for b in layout]
            json_file = os.path.join(output_dir, img_file.rsplit(".", 1)[0] + ".json")
            with open(json_file, "w") as f:
                json.dump(layout_data, f, indent=4)

            print(f"[✓] Layout extracted for {img_file}")

# Example usage
if __name__ == "__main__":
    detect_layout_on_images("data/images", "data/extracted/layouts")
