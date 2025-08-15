import google.generativeai as genai
import json
from config import GEMINI_API_KEY 
import time
from dotenv import load_dotenv
import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(CURRENT_DIR, '..', 'prompts')

load_dotenv()
def initialize_gemini():
    """Initializes the Google Gemini API."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    if GEMINI_API_KEY:
        print(f"DEBUG: Initializing Gemini with key (first 5 chars): {GEMINI_API_KEY[:5]}...")
    else:
        print("DEBUG: GEMINI_API_KEY is NOT set. This is a critical error.")
        raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it before running.")

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-pro")
        return model
    except Exception as e:
        print(f"Error initializing Gemini: {e}")
        raise

def call_gemini_api(model, prompt_text, max_retries=3, delay=10): 
    """Calls the Gemini API with retry logic."""
    print(f"DEBUG: Calling Gemini API for prompt (first 200 chars): {prompt_text[:200]}...") 

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt_text)

            print(f"DEBUG: Attempt {attempt+1} - Raw API Response Object: {response}")
            if response.prompt_feedback:
                print(f"DEBUG: Prompt Feedback (Safety or Blocked Reason): {response.prompt_feedback}")

            if response.parts:
                print(f"DEBUG: API returned content on attempt {attempt+1}.")
                return response.text
            else:
                print(f"DEBUG: Attempt {attempt+1}: Gemini API response has no text content in .parts. Response: {response}")
                if response.prompt_feedback and response.prompt_feedback.block_reason:
                    print(f"DEBUG: Blocking reason: {response.prompt_feedback.block_reason.name}")
                    if response.prompt_feedback.block_reason.name == 'OTHER': 
                        print("DEBUG: Block reason is 'OTHER', may indicate an API error or unsupported content.")

                if attempt < max_retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2 
        except Exception as e:
            print(f"DEBUG: Attempt {attempt+1}: EXCEPTION during Gemini API call: {e}")
            if "blocked" in str(e).lower(): 
                print("DEBUG: This exception message suggests a potential content policy violation.")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2 
    raise Exception("Failed to get a valid response from Gemini API after multiple retries. Review debug output above for clues.")


def extract_content_with_ai(chapter_text):
    """
    Uses AI to extract structured content from chapter text.
    Returns JSON object.
    """
    model = initialize_gemini()
    prompt_file_path = os.path.join(PROMPTS_DIR, "extraction_prompt.txt")
    try:
        with open(prompt_file_path, "r", encoding="utf-8") as f:
            base_prompt = f.read()
    except FileNotFoundError:
        print(f"Error: Prompt file not found at {prompt_file_path}")
        return None

    full_prompt = f"{base_prompt}\n\n[INSERT THE CLASS 8 NCERT SCIENCE CHAPTER TEXT HERE]\n{chapter_text}"

    print("Sending extraction request to AI...")
    ai_response_text = call_gemini_api(model, full_prompt)

    try:
        json_start = ai_response_text.find('{')
        json_end = ai_response_text.rfind('}') + 1
        if json_start != -1 and json_end != -1 and json_end > json_start:
            json_string = ai_response_text[json_start:json_end]
            return json.loads(json_string)
        else:
            print("Could not find a valid JSON object in AI response.")
            print("AI Raw Response:", ai_response_text)
            return None
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        print("AI Raw Response:", ai_response_text)
        return None

def generate_study_planner_with_ai(extracted_json_content):
    """
    Uses AI to generate a study planner based on extracted content.
    Returns string (Markdown/text).
    """
    model = initialize_gemini()
    prompt_file_path = os.path.join(PROMPTS_DIR, "planner_prompt.txt")
    try:
        with open(prompt_file_path, "r", encoding="utf-8") as f:
            base_prompt = f.read()
    except FileNotFoundError:
        print(f"Error: Prompt file not found at {prompt_file_path}")
        return None

    json_str_for_ai = json.dumps(extracted_json_content, indent=2)

    full_prompt = f"{base_prompt}\n\n[INSERT THE EXTRACTED JSON CONTENT OF THE CLASS 8 NCERT SCIENCE CHAPTER HERE]\n{json_str_for_ai}"

    print("Sending study planner request to AI...")
    ai_response_text = call_gemini_api(model, full_prompt)
    return ai_response_text

def itr():
    return "This is itr"

if __name__ == '__main__':
    print("Testing AI interface...")
    dummy_chapter_text = "This is a dummy chapter about cells. It discusses the structure of a plant cell, including the cell wall and nucleus. An activity involves observing onion peel cells under a microscope."

    print("\n--- Testing Content Extraction ---")
    extracted_data = extract_content_with_ai(dummy_chapter_text)
    if extracted_data:
        print("Extracted Data (first 200 chars):", json.dumps(extracted_data, indent=2)[:200])
    else:
        print("Content extraction failed.")

    print("\n--- Testing Study Planner Generation ---")
    if extracted_data:
        study_planner = generate_study_planner_with_ai(extracted_data)
        if study_planner:
            print("Generated Study Planner (first 200 chars):\n", study_planner[:200])
        else:
            print("Study planner generation failed.")
    else:
        print("Skipping study planner test due to failed extraction.")