from engine.index import reverse_index
from engine.tokenize import tokenizer


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(
                    1 + min((distances[i1], distances[i1 + 1], distances_[-1]))
                )
        distances = distances_
    return distances[-1]


def suggest(query: str, max_suggestions: int = 3):
    print_title = True
    for token in tokenizer(query):
        if token not in reverse_index.keys():
            if print_title:
                print("\nDid you mean?")
                print_title = False
            print(f"'{token}' -> ", end=" ")
            for term in list(reverse_index.keys()):
                if levenshteinDistance(token, term) <= 2:
                    print(f"{term} ", end=" ")
            print()


if __name__ == "__main__":
    query = "Keybard Montor"
    suggest(query)
