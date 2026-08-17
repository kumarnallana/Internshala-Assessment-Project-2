import os
import tempfile
import pytest
from email.message import EmailMessage
from app.outreach.attachment_handler import attach_file

def test_attach_file_success():
    msg = EmailMessage()
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("dummy content")
        temp_name = f.name
        
    attach_file(msg, temp_name)
    assert len(msg.get_payload()) > 0
    os.remove(temp_name)

def test_attach_file_not_found():
    msg = EmailMessage()
    with pytest.raises(FileNotFoundError):
        attach_file(msg, "nonexistent.pdf")
