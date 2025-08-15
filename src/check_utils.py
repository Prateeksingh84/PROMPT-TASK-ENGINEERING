import os

utils_path = os.path.join(os.path.dirname(__file__), "utils")
expected = [
    "__init__.py",
    "ai_interface.py",
    "pdf_parser.py",
    "excel_generator.py",
    "knowledge_graph.py"
]

for f in expected:
    file_path = os.path.join(utils_path, f)
    if not os.path.isfile(file_path):
        print(f" MISSING: {f}")
    else:
        print(f" FOUND: {f}")
