import os
from pdf2image import convert_from_path

def convert_pdf_to_images(pdf_path, output_folder, dpi=300):
    """
    Converts a PDF into high-resolution images and saves them page-wise.
    Skips if images already exist.
    """
    os.makedirs(output_folder, exist_ok=True)

    print(f"📄 Converting PDF: {pdf_path}")
    pages = convert_from_path(pdf_path, dpi=dpi)

    for i, page in enumerate(pages):
        filename = f"page_{i+1:03}.png"
        filepath = os.path.join(output_folder, filename)
        page.save(filepath, "PNG")
        print(f"✅ Saved: {filepath}")

    print(f"🎯 Conversion complete. Total pages: {len(pages)}")

if __name__ == "__main__":
    # Change this to match your file
    input_pdf = "data/pdfs/manual.pdf"
    output_dir = "data/images/"

    if not os.path.isfile(input_pdf):
        print("❌ PDF not found. Please place it in 'data/pdfs/' and try again.")
    else:
        convert_pdf_to_images(input_pdf, output_dir)
