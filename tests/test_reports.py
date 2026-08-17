import tempfile
import csv
from app.reports.report_generator import generate_summary_report, generate_csv_report
from app.logging import activity_logger

def test_report_generation():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, newline='') as b_file, \
         tempfile.NamedTemporaryFile(mode='w+', delete=False, newline='') as sl_file, \
         tempfile.NamedTemporaryFile(mode='w+', delete=False, newline='') as be_file, \
         tempfile.NamedTemporaryFile(mode='w+', delete=False, newline='') as ie_file:
         
        activity_logger.BUYERS_FILE = b_file.name
        activity_logger.SENT_LOG_FILE = sl_file.name
        activity_logger.BUSINESS_EMAILS_FILE = be_file.name
        activity_logger.INDIVIDUAL_EMAILS_FILE = ie_file.name
        
        activity_logger.init_logs()
        
        # Add a sent log
        activity_logger.log_send_attempt("test@test.com", "sent")
        
        summary = generate_summary_report()
        assert summary["success_count"] == 1
        assert summary["failed_count"] == 0
        
        csv_report = generate_csv_report()
        assert "success_count,1" in csv_report
        assert "test@test.com,sent" in csv_report
