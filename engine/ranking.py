import json
import math
import heapq

from engine.tokenize import tokenizer


class PonderedProduct:
    def __init__(self, product_id, score):
        self.product_id = product_id
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score
        

    @property
    def get_score(self) -> float:
        return self.score


#:NOTE: I have to create a new index because I need the stock and the sales_rank to calculate the score
# I Have intentionally kept all the information of the product because the Part 3 will need event more than the score and the sales_rank
# TLDR : Should be a good idea to discuss all together about that and if it is not better to create class for the inverted index as we talk about day 1

with open("catalog.json") as catalog_file:
    catalog = json.load(catalog_file)
    id_indexed_products = {product["id"]: product
                           for product in catalog}


def search_ranking(query: str, top_k: int = 10):
    query_tokens = tokenizer(query)

    results = get_query_results(query_tokens)

    pondered_results = get_ranked_results(results, top_k, len(query_tokens))

    return [pondered_result.product_id for pondered_result in
            sorted(pondered_results, key=lambda x: x.get_score, reverse=True)]


def get_query_results(query_tokens):
    inversed_dict = dict()  # will be replaced by the one from index.py when it will be merged
    results = dict()
    for token in query_tokens:
        for product_id in inversed_dict[token]:
            if product_id in results:
                results[product_id] += 1
            else:
                results[product_id] = 1

    return results


def get_ranked_results(query_results, top_k: int, query_tokens_count: int):
    pondered_results = []

    for product_id, found_count in query_results.items():
        score = _ponderate(found_count,
                           query_tokens_count,
                           id_indexed_products[product_id].get("stock"),
                           id_indexed_products[product_id].get("sales_rank")
                           )

        if len(pondered_results) < top_k:
            heapq.heappush(pondered_results, PonderedProduct(product_id, score))
        elif score > pondered_results[0].get_score:
            heapq.heapreplace(pondered_results, PonderedProduct(product_id, score))

    return pondered_results


def _ponderate(matched_tokens: int, total_query_token: int, stock: int, sales_rank: int) -> float:
    score = (matched_tokens - total_query_token) * 0.5
    score += stock * 0.2 if sales_rank > 0 else 0
    score += (1 / math.log2(sales_rank + 2)) * 0.3

    return score
