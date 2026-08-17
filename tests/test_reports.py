import tempfile
import csv
from app.reports.report_generator import generate_summary_report, generate_csv_report
from app.logging import activity_logger

def test_report_generation():
    b_file = tempfile.NamedTemporaryFile(delete=False)
    sl_file = tempfile.NamedTemporaryFile(delete=False)
    be_file = tempfile.NamedTemporaryFile(delete=False)
    ie_file = tempfile.NamedTemporaryFile(delete=False)
    
    b_file.close()
    sl_file.close()
    be_file.close()
    ie_file.close()

    try:
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
    finally:
        import os
        for f in [b_file.name, sl_file.name, be_file.name, ie_file.name]:
            if os.path.exists(f):
                os.remove(f)
