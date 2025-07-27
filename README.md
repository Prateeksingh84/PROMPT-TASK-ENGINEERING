# 🧠 Prompt-Task-Engineering – AI-Powered Study Workflow Automation

## 📌 Overview

Prompt-Task-Engineering is a Python-based automation framework designed to streamline the creation of structured educational content from raw PDF chapters using Large Language Models (LLMs). The system performs text extraction, AI-driven content structuring, Excel generation, knowledge graph creation, and automated study planner generation—all in a single workflow.

## 🚀 Key Features

- 🔽 PDF download or local usage
- 📄 Text extraction using PyPDF2
- 🤖 AI-powered content extraction via custom prompts
- 📊 Auto-generated Excel sheets
- 🌐 Knowledge graph generation from structured text
- 📝 Markdown-based study planners
- 📚 Complete documentation with used prompts and workflow summary

## 🏗️ Folder Structure
project/
├── main.py # Core workflow script
├── prompts/
│ ├── extraction_prompt.txt # Prompt for AI-based content extraction
│ └── planner_prompt.txt # Prompt for AI-based planner creation
├── utils/
│ ├── pdf_parser.py
│ ├── ai_interface.py
│ ├── excel_generator.py
│ └── knowledge_graph.py
├── data/
│ ├── downloaded_pdfs/
│ ├── extracted_json/
│ ├── output_excel/
│ ├── output_kg/
│ ├── output_planner/
│ └── documentation/


## 🛠️ Technologies Used

- **Python 3.10+**
- `os`, `sys`, `json`, `datetime`
- `PyPDF2` for PDF parsing
- Custom AI interface (OpenAI/Gemini via prompts)
- Base Python modules for I/O
- Excel handling with `openpyxl` or similar (in utils)
- Knowledge graph generation logic from structured JSON

## 🔁 Workflow Steps

1. Accept chapter name and PDF URL or local path
2. Download or load the PDF
3. Extract raw text from the PDF
4. Use AI to:
   - Extract structured content (headings, definitions, examples, etc.)
   - Generate a study planner
5. Save outputs in:
   - JSON format
   - Excel file
   - Knowledge graph text
   - Markdown planner
6. Generate full documentation including prompt history

## 📦 How to Run

```bash
python main.py



