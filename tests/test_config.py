import os
import pytest
from app.config import validate_config

def test_validate_config_missing_presentation():
    # If the file doesn't exist, it should raise FileNotFoundError
    import app.config as config
    old_path = config.PRESENTATION_PATH
    config.PRESENTATION_PATH = "nonexistent.pdf"
    
    with pytest.raises(FileNotFoundError):
        validate_config()
        
    config.PRESENTATION_PATH = old_path # Restore
