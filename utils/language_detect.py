import re


def detect_main_language(text):
    """Detects if the main language is Arabic or English based on character ratio."""
    arabic_chars = re.findall(r"[\u0600-\u06FF]", text)
    english_chars = re.findall(r"[a-zA-Z]", text)

    arabic_ratio = len(arabic_chars) / (len(arabic_chars) + len(english_chars) + 1)

    return "ar" if arabic_ratio > 0.7 else "en"
