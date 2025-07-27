# c:\Users\user\my_project\utils\__init__.py

# --- Imports from pdf_parser.py ---
# Based on your provided pdf_parser.py, it ONLY defines:
#   - download_pdf
#   - extract_text_from_pdf
# If you add more functions to pdf_parser.py later (e.g., parse_pdf_to_json),
# you MUST update this import statement accordingly.
from .pdf_parser import (
    download_pdf,
    extract_text_from_pdf
)

# --- Imports from ai_interface.py ---
# These functions MUST be defined in c:\Users\user\my_project\utils\ai_interface.py
# If any of these are missing from ai_interface.py, you will get an ImportError.
from .ai_interface import (
    initialize_gemini,
    call_gemini_api,
    extract_content_with_ai,
    generate_study_planner_with_ai,
    # Make sure 'itr' is actually a function or variable you want to expose.
    # If it's internal to ai_interface, don't import it here.
    itr
)

# --- Imports from excel_generator.py ---
# This function MUST be defined in c:\Users\user\my_project\utils\excel_generator.py
from .excel_generator import generate_excel_from_json

# --- Imports from knowledge_graph.py ---
# This function MUST be defined in c:\Users\user\my_project\utils\knowledge_graph.py
from .knowledge_graph import generate_text_based_knowledge_graph

# --- Note on dotenv.load_dotenv() ---
# Do NOT put dotenv.load_dotenv() or similar environment loading here.
# Environment variables should be loaded once at the absolute entry point of your application
# (e.g., in your main.py or app.py file) before any modules that rely on them are imported.
# This prevents issues with environment variables not being set when a module is loaded.