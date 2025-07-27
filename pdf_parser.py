import PyPDF2
import requests
import os
import re
import pytesseract
import pdfplumber
from PIL import Image
from pdf2image import convert_from_path # Removed PdfInfo import

# You might need to set the path to the Tesseract executable if it's not in your system's PATH.
# Example for Windows:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Example for Linux/macOS (often not needed if installed via package manager):
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract' # Adjust as per your installation


def download_pdf(url, output_path):
    """Downloads a PDF from a given URL."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)
        print(f"Downloaded: {output_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False

def extract_text_from_pdf(pdf_path, use_ocr_fallback=False):
    """
    Extracts text from a PDF file using pdfplumber, with an optional OCR fallback using pytesseract.
    
    Args:
        pdf_path (str): The path to the PDF file.
        use_ocr_fallback (bool): If True, attempts OCR if pdfplumber extracts no text.
                                 Set to True if you suspect scanned PDFs.
    """
    text = ""
    pdf_plumber_extracted_text = ""
    
    # --- Attempt text extraction with pdfplumber first ---
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                pdf_plumber_extracted_text += page.extract_text() or ""
        
        if pdf_plumber_extracted_text.strip(): # Check if pdfplumber found any significant text
            text = pdf_plumber_extracted_text
            print(f"Text extracted using pdfplumber from {os.path.basename(pdf_path)}")
            return text
        elif not pdf_plumber_extracted_text.strip() and use_ocr_fallback:
            print(f"pdfplumber found no text in {os.path.basename(pdf_path)}. Attempting OCR...")
        elif not pdf_plumber_extracted_text.strip() and not use_ocr_fallback:
            print(f"pdfplumber found no text in {os.path.basename(pdf_path)}. OCR fallback is disabled.")
            return None # No text found, and OCR not requested.
            
    except pdfplumber.exceptions.PDFSyntaxError as e: # Catch specific pdfplumber errors
        print(f"PDFSyntaxError with pdfplumber for {pdf_path}: {e}")
        if not use_ocr_fallback:
            print("OCR fallback is disabled. Skipping text extraction for this file.")
            return None
        print("Attempting OCR fallback due to PDFSyntaxError...")
    except Exception as e: # Catch any other general errors from pdfplumber
        print(f"An unexpected error occurred with pdfplumber while extracting text from {pdf_path}: {e}")
        if not use_ocr_fallback:
            print("OCR fallback is disabled. Skipping text extraction for this file.")
            return None
        print("Attempting OCR fallback due to unexpected error...")

    # --- Fallback to OCR if pdfplumber failed or found no text and OCR fallback is enabled ---
    if use_ocr_fallback and not text.strip(): # Only proceed if pdfplumber didn't yield text or errored
        try:
            # Convert PDF pages to images
            print(f"Converting pages of {os.path.basename(pdf_path)} to images for OCR...")
            # You might need to specify poppler_path if Poppler is not in your system's PATH
            # For example (Windows): poppler_path=r'C:\Program Files\poppler-XXX\bin'
            images = convert_from_path(pdf_path) 

            for i, image in enumerate(images):
                print(f"Performing OCR on page {i+1} of {os.path.basename(pdf_path)}...")
                # Use pytesseract to extract text from each image
                page_text = pytesseract.image_to_string(image)
                text += page_text + "\n" # Add a newline between pages

            if text.strip():
                print(f"Text extracted using OCR from {os.path.basename(pdf_path)}")
                return text
            else:
                print(f"OCR also found no text in {os.path.basename(pdf_path)}")
                return None

        except pytesseract.TesseractNotFoundError:
            print(f"Tesseract is not installed or not in your PATH for {pdf_path}.")
            print("Please install Tesseract OCR engine (e.g., `sudo apt-get install tesseract-ocr`)")
            print("and ensure it's accessible or set `pytesseract.pytesseract.tesseract_cmd`.")
            return None
        except Exception as e: # Catch any errors from pdf2image or other issues during OCR
            print(f"An unexpected error occurred during OCR for {pdf_path}: {e}")
            print("This might be due to Poppler not being installed or not in your system's PATH.")
            print("If on Windows, you might need to specify poppler_path in convert_from_path.")
            return None
            
    return text if text.strip() else None


if __name__ == '__main__':
    # Example Usage:
    pdf_links = [
        "[https://ncert.nic.in/textbook/pdf/hesc106.pdf](https://ncert.nic.in/textbook/pdf/hesc106.pdf)",
        "[https://ncert.nic.in/textbook/pdf/hesc107.pdf](https://ncert.nic.in/textbook/pdf/hesc107.pdf)",
        "[https://ncert.nic.in/textbook/pdf/hesc108.pdf](https://ncert.nic.in/textbook/pdf/hesc108.pdf)",
        "[https://ncert.nic.in/textbook/pdf/hesc113.pdf](https://ncert.nic.in/textbook/pdf/hesc113.pdf)"
        # Add a link to a known scanned PDF here if you want to test OCR more explicitly
        # Example (replace with an actual public scanned PDF URL):
        # "[https://www.africau.edu/images/default/sample.pdf](https://www.africau.edu/images/default/sample.pdf)"
    ]
    download_dir = "../data/downloaded_pdfs/"
    os.makedirs(download_dir, exist_ok=True)

    for url_string in pdf_links:
        # Extract the actual URL from the Markdown link format
        match = re.search(r'\((https?://[^\s]+)\)', url_string)
        if match:
            url = match.group(1)
        else:
            print(f"Could not parse URL from: {url_string}. Skipping.")
            continue

        file_name = url.split('/')[-1]
        output_file_path = os.path.join(download_dir, file_name)
        if download_pdf(url, output_file_path):
            print(f"\nProcessing: {file_name}")
            # Set use_ocr_fallback=True if you want it to try OCR if pdfplumber finds no text
            extracted_text = extract_text_from_pdf(output_file_path, use_ocr_fallback=True)
            if extracted_text:
                output_txt_path = os.path.join(download_dir, file_name.replace(".pdf", ".txt"))
                with open(output_txt_path, "w", encoding="utf-8") as f:
                    f.write(extracted_text)
                print(f"Text extracted and saved to {output_txt_path}")
            else:
                print(f"Could not extract text from {file_name} even with OCR fallback.")

    print("\n--- Processing Complete ---")
    print("Remember: pdfplumber is good for native PDF text and tables. pytesseract (OCR) is for scanned/image-based PDFs.")
    print("Ensure Tesseract OCR engine and Poppler are installed on your system for full functionality.")