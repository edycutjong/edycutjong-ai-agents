import textstat

def analyze_text(text: str) -> dict:
    """
    Analyzes the text for readability and basic statistics.
    """
    if not text.strip():
        return {
            "flesch_reading_ease": 0,
            "flesch_kincaid_grade": 0,
            "smog_index": 0,
            "word_count": 0,
            "sentence_count": 0,
        }

    return {
        "flesch_reading_ease": textstat.flesch_reading_ease(text),
        "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
        "smog_index": textstat.smog_index(text),
        "word_count": textstat.lexicon_count(text, removepunct=True),
        "sentence_count": textstat.sentence_count(text),
    }

def interpret_flesch_score(score: float) -> str:
    """
    Interprets the Flesch Reading Ease score.
    """
    if score >= 90:
        return "Very Easy"
    elif score >= 80:
        return "Easy"
    elif score >= 70:
        return "Fairly Easy"
    elif score >= 60:
        return "Standard"
    elif score >= 50:
        return "Fairly Difficult"
    elif score >= 30:
        return "Difficult"
    else:
        return "Very Difficult"
