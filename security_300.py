# Security Enhancement for Issue #300
import re
from typing import Tuple

def validate_email(email: str) -> Tuple[bool, str]:
    if not email or '@' not in email:
        return False, "Invalid email"
    return True, "OK"

def sanitize_input(input_str: str, max_len: int = 1000) -> str:
    if not input_str:
        return ""
    if len(input_str) > max_len:
        input_str = input_str[:max_len]
    patterns = [r"<script.*?>.*?</script>", r"javascript:"]
    for p in patterns:
        input_str = re.sub(p, "", input_str, flags=re.IGNORECASE)
    return input_str.strip()

# Tests
assert validate_email("test@example.com")[0] == True
print("Security tests passed!")
