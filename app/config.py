import os
from dotenv import load_dotenv

load_dotenv()

GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

SEARCH_KEYWORD = os.getenv("SEARCH_KEYWORD", "Singing Bowls")
DAILY_SEND_LIMIT = int(os.getenv("DAILY_SEND_LIMIT", 100))
PRESENTATION_PATH = os.getenv("PRESENTATION_PATH", "assets/demo_presentation.pdf")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DRY_RUN = os.getenv("DRY_RUN", "true").lower() in ("true", "1", "yes")

# Ensure required config for sending unless it's just tests
def validate_config():
    if not os.path.exists(PRESENTATION_PATH):
        raise FileNotFoundError(f"Presentation file not found at {PRESENTATION_PATH}")
    if not DRY_RUN:
        if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
            raise ValueError("Gmail credentials missing in .env for real send")
