from typing import Optional
import re


def validate_question(question: str) -> tuple[bool, Optional[str]]:
    """
    Validate question input.
    
    Args:
        question: The question string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not question:
        return False, "Question cannot be empty"
    
    question = question.strip()
    
    if len(question) < 3:
        return False, "Question must be at least 3 characters long"
    
    if len(question) > 1000:
        return False, "Question must be less than 1000 characters"
    
    # Check for potentially malicious patterns
    suspicious_patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, question, re.IGNORECASE):
            return False, "Question contains invalid content"
    
    return True, None

