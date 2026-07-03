import heapq
import math

from engine.index import products_index, reverse_index
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


def search_ranking(query: str, top_k: int = 10):
    query_tokens = tokenizer(query)

    results = get_query_results(query_tokens)

    pondered_results = get_ranked_results(results, top_k, len(query_tokens))

    return [
        pondered_result.product_id
        for pondered_result in sorted(
            pondered_results, key=lambda x: x.get_score, reverse=True
        )
    ]


def get_query_results(query_tokens):
    results = dict()
    for token in query_tokens:
        for product_id in reverse_index[token]:
            if product_id in results:
                results[product_id] += 1
            else:
                results[product_id] = 1

    return results


def get_ranked_results(query_results, top_k: int, query_tokens_count: int):
    pondered_results = []

    for product_id, found_count in query_results.items():
        score = _ponderer(
            found_count,
            query_tokens_count,
            products_index[product_id].get_stock,
            products_index[product_id].get_sales_rank,
        )

        if len(pondered_results) < top_k:
            heapq.heappush(
                pondered_results, PonderedProduct(product_id, score)
            )
        elif score > pondered_results[0].get_score:
            heapq.heapreplace(
                pondered_results, PonderedProduct(product_id, score)
            )

    return pondered_results


def _ponderer(
    matched_tokens: int, total_query_token: int, stock: int, sales_rank: int
) -> float:
    score = (matched_tokens - total_query_token) * 0.5
    score += stock * 0.2 if sales_rank > 0 else 0
    score += (1 / math.log2(sales_rank + 2)) * 0.3

    return score
