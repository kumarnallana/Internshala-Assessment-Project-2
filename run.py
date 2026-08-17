import sys
sys.modules["google._upb._message"] = None

import uvicorn
from app.logging.activity_logger import init_logs
from app.config import validate_config

if __name__ == "__main__":
    init_logs()
    try:
        validate_config()
    except Exception as e:
        print(f"Configuration Error: {e}")
        # Not exiting immediately to allow UI to show, but in a real app might exit.
        
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
