"""
Prompts definition function
"""
def get_keyword_prompt(extracted_words):
    """
    Generates the prompt for extracting keywords.
    
    Args:
        extracted_words (list): List of extracted words.

    Returns:
        list: A formatted message structure for keyword extraction.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are a tool that extracts keywords from a given text. "
                "Provide a comma-separated list of keywords. Just give keywords list and don't reply anything else. "
                "Don't add anything else in starting. Remember it!"
            ),
        },
        {
            "role": "user",
            "content": "Extract keywords from: " + ", ".join(extracted_words),
        }
    ]
