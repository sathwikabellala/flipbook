# pdf_converter.py
import pdf2image
import os

def convert_pdf_to_flipbook(pdf_input, output_dir):
    if isinstance(pdf_input, str):  # Check if input is a file path
        with open(pdf_input, 'rb') as file:
            return convert_pdf_to_flipbook(file, output_dir)  # Recursively call with file object

    try:
        images = pdf2image.convert_from_bytes(pdf_input.read(), output_folder=output_dir, poppler_path='poppler-24.02.0/Library/bin')

    except Exception as e:
        return [f'Error: {e}']

    flipbook_pages = []
    for i, image in enumerate(images):
        try:
            image_path = os.path.join(output_dir, f'page_{i}.jpg')
            image.save(image_path, 'JPEG')
            flipbook_pages.append(image_path)  # Append image path to the list
        except Exception as e:
            flipbook_pages.append(f'Error saving page {i}: {e}')

    return flipbook_pages  # Return the list of image paths
