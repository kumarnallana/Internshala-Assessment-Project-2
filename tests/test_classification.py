from app.classification.mock_classifier import MockClassifier
from app.classification.gemini_classifier import GeminiClassifier

def test_mock_classifier():
    classifier = MockClassifier()
    emails = ["john@example.com", "sales@corp.com", "info@business.com", "jane@gmail.com"]
    b, i, u = classifier.classify_emails(emails)
    
    assert "sales@corp.com" in b
    assert "john@example.com" in i
    assert len(u) == 0

def test_gemini_fallback():
    # Should fallback to mock if no API key is provided
    classifier = GeminiClassifier(api_key=None, use_mock=False)
    assert classifier.use_mock == True
