import os
import pytest
from app.config import validate_config

def test_validate_config_missing_presentation():
    # If the file doesn't exist, it should raise FileNotFoundError
    old_path = os.getenv("PRESENTATION_PATH", "assets/demo_presentation.pdf")
    os.environ["PRESENTATION_PATH"] = "nonexistent.pdf"
    
    with pytest.raises(FileNotFoundError):
        validate_config()
        
    os.environ["PRESENTATION_PATH"] = old_path # Restore
