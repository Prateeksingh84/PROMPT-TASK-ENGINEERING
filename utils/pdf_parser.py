import PyPDF2
import requests
import os

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

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or "" 
        return text
    except PyPDF2.errors.PdfReadError as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while extracting text from {pdf_path}: {e}")
        return None

if __name__ == '__main__':
    # Example Usage:
    pdf_links = [
        "[https://ncert.nic.in/textbook/pdf/hesc106.pdf](https://ncert.nic.in/textbook/pdf/hesc106.pdf)",
        "[https://ncert.nic.in/textbook/pdf/hesc107.pdf](https://ncert.nic.in/textbook/pdf/hesc107.pdf)",
        "[https://ncert.nic.in/textbook/pdf/hesc108.pdf](https://ncert.nic.in/textbook/pdf/hesc108.pdf)",
        "[https://ncert.nic.in/textbook/pdf/hesc113.pdf](https://ncert.nic.in/textbook/pdf/hesc113.pdf)"
    ]
    download_dir = "../data/downloaded_pdfs/"
    os.makedirs(download_dir, exist_ok=True)

    for url in pdf_links:
        file_name = url.split('/')[-1]
        output_file_path = os.path.join(download_dir, file_name)
        if download_pdf(url, output_file_path):
            print(f"Extracting text from {file_name}...")
            extracted_text = extract_text_from_pdf(output_file_path)
            if extracted_text:
                output_txt_path = os.path.join(download_dir, file_name.replace(".pdf", ".txt"))
                with open(output_txt_path, "w", encoding="utf-8") as f:
                    f.write(extracted_text)
                print(f"Text extracted and saved to {output_txt_path}")
            else:
                print(f"Could not extract text from {file_name}")

    print("\nRemember: PyPDF2 is basic. For complex layouts, consider other parsing methods or APIs.")