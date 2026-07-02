import math
import heapq

from engine.tokenize import tokenizer


class PonderatedProduct:
    def __init__(self, product_id, score):
        self.product_id = product_id
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score

    @property
    def get_score(self):
        return self.score


def search_ranking(query: str, top_k: int = 10):
    # tokenize query
    query_tokens = tokenizer(query)
    
    # use indexed dict made in part 1 to lookup for results
    results = dict()
    inversed_dict = dict() # will be replaced by the one from index.py when it will be merged
    for token in query_tokens:
        for product_id in inversed_dict[token]:
            if product_id in results:
                results[product_id] += 1
            else:
                results[product_id] = 1
                
    ponderated_results = []

    for product_id, found_count in results.items():
        score = ponderate(found_count, len(query_tokens), 0, 0)#lookup on data to find stock et sales_rank

        if len(ponderated_results) < top_k:
            heapq.heappush(ponderated_results, PonderatedProduct(product_id, score))
        elif score > ponderated_results[0].get_score:
            heapq.heapreplace(ponderated_results, PonderatedProduct(product_id, score))

    return [ponderated_result.product_id for ponderated_result in
            sorted(ponderated_results, key=lambda x: x.get_score, reverse=True)]


def ponderate(matched_tokens: int, total_query_token: int, stock: int, sales_rank: int) -> float:
    score = (matched_tokens - total_query_token) * 0.5
    score += stock * 0.2 if sales_rank > 0 else 0
    score += (1 / math.log2(sales_rank + 2)) * 0.3

    return score
