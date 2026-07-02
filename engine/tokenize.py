import re


def tokenizer(str):
    """
    Tokenise by splitting on spaces and punctuation, lowercasing, stripping short words (≤ 2 chars)
    """
    raw_tokens = re.findall(r"\w+", str)

    formatted_tokens = []

    for token in raw_tokens:
        if len(token) > 2:
            formatted_tokens.append(token.lower())

    return formatted_tokens
