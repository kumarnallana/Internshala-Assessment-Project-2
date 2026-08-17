import os
import tempfile
import csv
from unittest import mock
from app.outreach.mock_sender import MockSender
from app.logging import activity_logger
from app.models.buyer import BuyerRecord

def test_mock_sender_success_and_skip():
    # Setup temp file for logging
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, newline='') as f:
        temp_log = f.name
        
    activity_logger.SENT_LOG_FILE = temp_log
    activity_logger.init_logs()
    
    sender = MockSender()
    
    # First run
    emails = ["test1@example.com", "test2@example.com"]
    s_count, f_count, succ, fail, skip = sender.send_campaign(emails, "Subj", "Body")
    
    assert s_count == 2
    assert len(skip) == 0
    
    # Check log
    log = activity_logger.get_sent_log()
    assert len(log) == 2
    assert log[0]["email"] == "test1@example.com"
    assert log[0]["status"] == "sent"
    
    # Second run with same emails + one new
    emails_run2 = ["test1@example.com", "test2@example.com", "test3@example.com"]
    s_count2, f_count2, succ2, fail2, skip2 = sender.send_campaign(emails_run2, "Subj", "Body")
    
    assert s_count2 == 1 # Only test3
    assert len(skip2) == 2 # test1, test2 skipped
    
    # Check log again
    log2 = activity_logger.get_sent_log()
    assert len(log2) == 5 # 2 from run1 + 1 new + 2 skipped
    
    # cleanup
    os.remove(temp_log)
