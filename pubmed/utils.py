import re
from typing import List

def is_non_academic(affiliation: str) -> bool:
    academic_keywords = ["university", "college", "school", "institute", "lab", "hospital"]
    return not any(word in affiliation.lower() for word in academic_keywords)

def extract_emails(text: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", text)