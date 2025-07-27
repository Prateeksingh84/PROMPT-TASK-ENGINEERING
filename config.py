# config.py
import os

# c:\Users\user\my_project\config.py

GEMINI_API_KEY = "AIzaSyDJd59ys6zvkn5j6KoQbBRPNjKrPHunvy8"
# It's better practice to load API keys from environment variables
# For development, you can put it directly, but for production, use os.environ
# import os
# GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_DEFAULT_KEY_IF_NOT_SET")