import tempfile
import os
from app.services.pipeline import PipelineService
from app.classification.mock_classifier import MockClassifier
from app.outreach.mock_sender import MockSender
from app.logging import activity_logger

def test_end_to_end_happy_path_and_idempotency():
    """
    Tests the entire happy-path workflow and formal idempotency.
    mock search -> extract -> validate -> deduplicate -> mock Gemini -> audience selection -> mock Gmail -> log -> report
    """
    # Setup temporary files for isolation
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, newline='') as b_file, \
         tempfile.NamedTemporaryFile(mode='w+', delete=False, newline='') as sl_file, \
         tempfile.NamedTemporaryFile(mode='w+', delete=False, newline='') as be_file, \
         tempfile.NamedTemporaryFile(mode='w+', delete=False, newline='') as ie_file:
         
        activity_logger.BUYERS_FILE = b_file.name
        activity_logger.SENT_LOG_FILE = sl_file.name
        activity_logger.BUSINESS_EMAILS_FILE = be_file.name
        activity_logger.INDIVIDUAL_EMAILS_FILE = ie_file.name
        
        activity_logger.init_logs()

        pipeline = PipelineService(keyword="Singing Bowls")
        
        # 1. Discovery & Extraction & Validation
        total, valid = pipeline.run_discovery()
        assert total > 0
        assert valid > 0
        
        # 2. Classification
        classifier = MockClassifier()
        b_count, i_count = pipeline.run_classification(classifier)
        
        assert b_count > 0 or i_count > 0
        
        # Gather emails to send to
        import csv
        emails = []
        with open(b_file.name, 'r') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                if row.get("email"):
                    emails.append(row["email"])
                    
        # 3. Outreach RUN 1
        sender = MockSender()
        s1, f1, succ1, fail1, skip1 = sender.send_campaign(emails, "Test Subject", "Test Body")
        
        assert s1 > 0
        assert len(skip1) == 0
        
        # 4. Outreach RUN 2 (Idempotency check)
        s2, f2, succ2, fail2, skip2 = sender.send_campaign(emails, "Test Subject", "Test Body")
        
        assert s2 == 0
        assert len(skip2) == len(emails) # All skipped as duplicate
        
        # Cleanup
        os.remove(b_file.name)
        os.remove(sl_file.name)
        os.remove(be_file.name)
        os.remove(ie_file.name)
