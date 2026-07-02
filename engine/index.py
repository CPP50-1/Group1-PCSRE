from engine.tokenize import tokenizer
import json


def build_reverse_index(data):
    reverse_index = dict()

    for product in data:
        tokens = tokenizer(product["name"]).union(product["tags"])
        for token in tokens:
            if token not in reverse_index:
                reverse_index[token] = set()
            reverse_index[token].add(product["id"])
    return reverse_index


with open("catalog.json") as json_data:
    data = json.load(
        json_data,
    )

reverse_index = build_reverse_index(data)
