import re


def tokenizer(str) -> set:
    """
    Tokenise by splitting on spaces and punctuation, lowercasing, stripping short words (≤ 2 chars)
    """
    raw_tokens = re.findall(r"\w+", str)

    formatted_tokens = set()
    formatted_tokens = set()

    for token in raw_tokens:
        if len(token) > 2:
            formatted_tokens.add(token.lower())
        if len(token) > 2:
            formatted_tokens.add(token.lower())
    return formatted_tokens
