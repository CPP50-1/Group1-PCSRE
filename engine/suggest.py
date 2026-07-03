from engine.index import reverse_index
from engine.tokenize import tokenizer


def levenshteinDistance(s1, s2):
    ltable = list(list())
    ltable.append([c for c in range(0, len(s2) + 1)])
    for r in range(1, len(s1) + 1):
        ltable.append([r])
        for c in range(1, len(s2) + 1):
            ltable[r].append(0)
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                addon = 0
            else:
                addon = 1
            ltable[i][j] = min(
                ltable[i - 1][j] + 1,
                ltable[i][j - 1] + 1,
                ltable[i - 1][j - 1] + addon,
            )
    return ltable[-1][-1]


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

    print(levenshteinDistance("toto", "totore"))
