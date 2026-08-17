import os
import tempfile
from app.outreach.mock_sender import MockSender
from app.logging import activity_logger

def test_formal_idempotency_duplicate_prevention():
    """
    Formal test for Idempotency/Duplicate Prevention as requested.
    Run #1: john@example.com -> sent
    Run #2: john@example.com -> skipped_duplicate
    """
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, newline='') as f:
        temp_log = f.name
        
    activity_logger.SENT_LOG_FILE = temp_log
    activity_logger.init_logs()
    
    sender = MockSender()
    email = "john@example.com"
    
    # Run 1
    s1, f1, succ1, fail1, skip1 = sender.send_campaign([email], "Pitch", "Body")
    assert s1 == 1
    assert email in succ1
    assert email not in skip1
    
    log1 = activity_logger.get_sent_log()
    assert len(log1) == 1
    assert log1[0]["email"] == email
    assert log1[0]["status"] == "sent"
    
    # Run 2
    s2, f2, succ2, fail2, skip2 = sender.send_campaign([email], "Pitch", "Body")
    assert s2 == 0
    assert email not in succ2
    assert email in skip2
    
    log2 = activity_logger.get_sent_log()
    assert len(log2) == 2
    assert log2[1]["email"] == email
    assert log2[1]["status"] == "skipped_duplicate"

    os.remove(temp_log)
