from app.extraction.data_extractor import extract_emails_from_text, create_buyer_records_from_data

def test_extract_emails_from_text():
    text = "Contact us at info@singingbowls.com or sales@singingbowls.com. See our logo at logo.png@domain.com."
    emails = extract_emails_from_text(text)
    assert "info@singingbowls.com" in emails
    assert "sales@singingbowls.com" in emails
    assert "logo.png@domain.com" not in emails

def test_create_buyer_records_empty_email():
    records = create_buyer_records_from_data("No email here", buyer_name="John")
    assert len(records) == 1
    assert records[0].email == ""
    assert records[0].buyer_name == "John"

def test_create_buyer_records_with_emails():
    text = "Contact me: alice@example.com and bob@test.com"
    records = create_buyer_records_from_data(text, company_name="Test Corp", source_platform="Google")
    assert len(records) == 2
    emails = [r.email for r in records]
    assert "alice@example.com" in emails
    assert "bob@test.com" in emails
    assert records[0].company_name == "Test Corp"
    assert records[0].source_platform == "Google"
