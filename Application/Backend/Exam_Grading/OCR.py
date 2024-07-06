import sys
from google.cloud import vision

def detect_text(input_path, output_path):
    """Detects text in the file and saves it to the output path."""
    client = vision.ImageAnnotatorClient()

    with open(input_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image) # Use document_text_detection instead of text_detection
    document = response.full_text_annotation

    recognized_text = document.text
    # The document.text attribute from the document_text_detection response will return the entire extracted text.

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(recognized_text)
    print(f"Recognized text saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python OCR.py <input_image_path> <output_text_path>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    output_text_path = sys.argv[2]
    detect_text(input_image_path, output_text_path)
