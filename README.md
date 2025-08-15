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

🏗️ Folder Structure

A common folder structure for a small to medium-sized project is as follows:

```
project/
├── .github/          # GitHub-specific files (e.g., issue templates, workflows)
├── .vscode/          # VS Code editor settings and extensions
├── notebooks/        # Jupyter notebooks for exploration and analysis
├── data/             # All data files, separated into raw, processed, and external
│   ├── raw/
│   ├── processed/
│   └── external/
├── src/              # Source code for the project
│   ├── __init__.py
│   ├── main.py       # Main entry point of the application
│   ├── config.py     # Configuration settings
│   ├── utils.py      # Utility functions
│   └── models/       # Machine learning models or data models
├── tests/            # Unit and integration tests
│   ├── __init__.py
│   └── test_main.py
├── docs/             # Documentation for the project
├── .gitignore        # Files and folders to be ignored by Git
├── requirements.txt  # Project dependencies
├── README.md         # Project description and instructions
└── setup.py          # Script for packaging and distributing the project
```
---

## 🛠️ Technologies Used

* **Python 3.10+**
* `os`, `sys`, `json`, `datetime` (Standard Python libraries for system interactions, data handling, and timestamps)
* `PyPDF2` for PDF parsing
* **Custom AI interface** (integrating OpenAI/Gemini via prompts)
* **Base Python modules** for file I/O operations
* **Excel handling** with `openpyxl` or similar (implemented within `utils/excel_generator.py`)
* **Knowledge graph generation logic** from structured JSON (implemented within `utils/knowledge_graph.py`)

---

## 🔁 Workflow Steps

1.  **Accept Chapter Input:** The system prompts the user to provide a chapter name and either a PDF URL or a local file path.
2.  **PDF Handling:** Downloads the PDF if a URL is provided, or loads it from the local path.
3.  **Text Extraction:** Extracts the raw textual content from the loaded PDF using `PyPDF2`.
4.  **AI Content Structuring:** Leverages the AI (via `extraction_prompt.txt`) to process the raw text and extract structured content (e.g., headings, definitions, examples).
5.  **Study Planner Generation:** Uses the AI (via `planner_prompt.txt`) to generate a comprehensive study planner based on the extracted content.
6.  **Output Generation:** Saves the processed outputs into designated folders:
    * Structured content in **JSON format** (`data/extracted_json/`).
    * Summarized data in an **Excel file** (`data/output_excel/`).
    * Textual representation for a **knowledge graph** (`data/output_kg/`).
    * The generated **Markdown planner** (`data/output_planner/`).
7.  **Documentation Creation:** Compiles full documentation, including a history of prompts used and a summary of the workflow, in the `data/documentation/` folder.

---

📦 How to Run

1️⃣ Install Requirements
pip install google-generativeai chromadb sentence-transformers PyPDF2 openpyxl

### 2️⃣ Set Your Gemini API Key
set GEMINI_API_KEY=your_google_generative_ai_key

### 3️⃣ Run the Workflow
python main.py

---


## 🧾 Example Output
Step 1: Scraping content from the web 
Successfully scraped and read the original chapter text.

Step 2: Initializing ChromaDB for versioning 
Original chapter version stored in ChromaDB.

Step 3: AI writing and review cycle 
AI draft 1 created and stored.
AI Reviewer Feedback:
The rewritten text flows better but loses some original context in paragraph 2. Consider restoring the metaphors. ---

Step 4: Human-in-the-Loop review 
Please provide your edits or 'approve':

---

📄 Sample Prompts
Extraction Prompt:

(Contents of prompts/extraction_prompt.txt)

Planner Prompt:

(Contents of prompts/planner_prompt.txt)


---

📌 Example Chapters Included
Chapter 6: Combustion and Flame

Chapter 7: Conservation of Plants and Animals

Chapter 8: Cell Structure and Functions

Chapter 13: Sound

---

✅ Advantages
Fully automated academic content structuring

Reusable across subjects and grade levels

Easily extendable with more prompt types

Promotes efficient self-study and documentation

---

⚠️ Notes
Requires valid API access to LLMs (OpenAI, Gemini, etc.).

Make sure GEMINI_API_KEY is set as an environment variable.

