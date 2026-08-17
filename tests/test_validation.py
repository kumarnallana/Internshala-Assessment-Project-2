from app.validation.email_validator import validate_email, is_valid_syntax, is_placeholder

def test_is_valid_syntax():
    assert is_valid_syntax("test@example.com") == True
    assert is_valid_syntax("john.doe+123@sub.domain.co.uk") == True
    assert is_valid_syntax("invalid-email") == False
    assert is_valid_syntax("@domain.com") == False
    assert is_valid_syntax("") == False

def test_is_placeholder():
    assert is_placeholder("admin@example.com") == True
    assert is_placeholder("test@test.com") == True
    assert is_placeholder("noreply@company.com") == True
    assert is_placeholder("real.user@gmail.com") == False

def test_validate_email():
    assert validate_email("real.user@gmail.com") == "VALID"
    assert validate_email("admin@example.com") == "INVALID"
    assert validate_email("invalid-email") == "INVALID"
    assert validate_email("") == "REVIEW_REQUIRED"
    assert validate_email("   ") == "REVIEW_REQUIRED"
