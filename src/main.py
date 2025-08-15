import os
print("DEBUG: GEMINI_API_KEY at main:", os.getenv("GEMINI_API_KEY"))
import sys
import json
from datetime import datetime

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ---- Your Module Imports ----
from utils.pdf_parser import download_pdf, extract_text_from_pdf
from utils.ai_interface import extract_content_with_ai, generate_study_planner_with_ai, itr
from utils.excel_generator import generate_excel_from_json
from utils.knowledge_graph import generate_text_based_knowledge_graph

# Main Workflow FunctioN
def run_workflow(chapter_name, pdf_source):
    print(f"\n--- Starting Workflow for {chapter_name} ---")

   
    base_data_dir = "data"
    folders = [
        "downloaded_pdfs", "extracted_json", "output_excel",
        "output_kg", "output_planner", "documentation"
    ]
    paths = {name: os.path.join(base_data_dir, name) for name in folders}
    for path in paths.values():
        os.makedirs(path, exist_ok=True)

    if pdf_source.startswith("http://") or pdf_source.startswith("https://"):
        pdf_filename = pdf_source.split('/')[-1]
        pdf_path = os.path.join(paths["downloaded_pdfs"], pdf_filename)

        if not os.path.exists(pdf_path):
            print(f"Downloading {pdf_filename} from URL...")
            if not download_pdf(pdf_source, pdf_path):
                print(f"Failed to download {pdf_filename}. Exiting.")
                return
        else:
            print(f"PDF already exists locally: {pdf_path}. Skipping download.")
    elif os.path.exists(pdf_source):
        pdf_path = pdf_source
        pdf_filename = os.path.basename(pdf_source)
        print(f"Using local PDF file: {pdf_path}")
    else:
        print(f"Invalid PDF source: {pdf_source}")
        return

    print(f"Extracting text from {pdf_filename}...")
    chapter_text = extract_text_from_pdf(pdf_path)
    if not chapter_text:
        print(f"Could not extract text from {pdf_filename}. Exiting.")
        return

    raw_text_path = os.path.join(paths["downloaded_pdfs"], pdf_filename.replace(".pdf", "_extracted.txt"))
    with open(raw_text_path, "w", encoding="utf-8") as f:
        f.write(chapter_text)
    print(f"Raw extracted text saved to {raw_text_path}")

    print("Calling AI for structured content extraction...")
    extracted_data = extract_content_with_ai(chapter_text)
    if not extracted_data:
        print("AI extraction failed. Exiting.")
        return

    json_path = os.path.join(paths["extracted_json"], f"{chapter_name}_chapter-extract.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=2)
    print(f"Structured JSON saved to {json_path}")

    excel_path = os.path.join(paths["output_excel"], f"{chapter_name}_science-sample-output.xlsx")
    if generate_excel_from_json(extracted_data, excel_path):
        print(f"Excel file saved to {excel_path}")
    else:
        print("Excel generation failed.")

    kg_text = generate_text_based_knowledge_graph(extracted_data)
    kg_path = os.path.join(paths["output_kg"], f"{chapter_name}_knowledge-graph.txt")
    with open(kg_path, "w", encoding="utf-8") as f:
        f.write(kg_text)
    print(f"Knowledge graph saved to {kg_path}")

    planner_text = generate_study_planner_with_ai(extracted_data)
    if planner_text:
        planner_path = os.path.join(paths["output_planner"], f"{chapter_name}_study_planner.md")
        with open(planner_path, "w", encoding="utf-8") as f:
            f.write(planner_text)
        print(f"Study planner saved to {planner_path}")
    else:
        print("Study planner generation failed.")

    doc_path = os.path.join(paths["documentation"], f"{chapter_name}_documentation.md")
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(f"# Documentation for {chapter_name}\n\n")
        f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Prompts Used\n")
        try:
            with open("prompts/extraction_prompt.txt", "r", encoding="utf-8") as f1:
                f.write("### Extraction Prompt:\n```markdown\n" + f1.read() + "\n```\n")
            with open("prompts/planner_prompt.txt", "r", encoding="utf-8") as f2:
                f.write("### Planner Prompt:\n```markdown\n" + f2.read() + "\n```\n")
        except FileNotFoundError:
            f.write("*Prompt files not found.*\n")

        f.write("## Workflow\n")
        f.write("1. Download or use local PDF.\n")
        f.write("2. Extract text using PyPDF2.\n")
        f.write("3. Use AI for JSON structuring.\n")
        f.write("4. Create Excel & knowledge graph.\n")
        f.write("5. Generate planner & documentation.\n")

    print(f"Documentation saved to {doc_path}")
    print(f"--- Workflow Complete for {chapter_name} ---\n")


if __name__ == '__main__':
    chapters_to_process = {
        "Chapter_06_Combustion_and_Flame": "https://ncert.nic.in/textbook/pdf/hesc106.pdf",
        "Chapter_07_Conservation_of_Plants_and_Animals": "https://ncert.nic.in/textbook/pdf/hesc107.pdf",
        "Chapter_08_Cell_Structure_and_Functions": "https://ncert.nic.in/textbook/pdf/hesc108.pdf",
        "Chapter_13_Sound": "https://ncert.nic.in/textbook/pdf/hesc113.pdf",
    }

    for chapter, source in chapters_to_process.items():
        run_workflow(chapter, source)
        print("=" * 80)