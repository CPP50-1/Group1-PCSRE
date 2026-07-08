import json
from collections import defaultdict

from engine.index import products_index
from engine.ranking import get_query_results, get_ranked_results
from engine.tokenize import tokenizer

with open("catalog.json") as catalog_file:
    catalog = json.load(catalog_file)

paths = sorted(set([product["category"] for product in catalog]))

# ---------------------------------------------------------------------------
# 1. Build a nested tree structure from a flat list of "/"-separated paths
# ---------------------------------------------------------------------------


def nested_dict():
    return defaultdict(nested_dict)


def simplify(node):
    # Recursively converts a nested_dict into a clean dict structure
    # where every leaf is represented by None (Option A).
    if not isinstance(node, dict):
        return node  # already a leaf value

    if len(node) == 0:
        return None  # empty dict -> this is a leaf

    # Otherwise, keep recursing into each child
    return {k: simplify(v) for k, v in node.items()}


def build_tree(paths):
    raw_tree = nested_dict()

    # Build a raw nested-dict structure from each "/"-separated path
    for line in paths:
        parts = line.strip().split("/")
        node = raw_tree
        for part in parts:
            node = node[part]

    # At this point, raw_tree is a nested dict where every leaf is an empty dict,
    # e.g. raw_tree["Networking"]["Cables"] == {}
    # Simplify replaces the empty dict by None
    return simplify(raw_tree)


category_tree = build_tree(paths)

# ---------------------------------------------------------------------------
# 2. DFS traversal of the resulting tree
# ---------------------------------------------------------------------------


def list_categories_dfs(tree, category):
    # Initialize the stack with a (path, content) tuple for the root.
    # Using a list as a stack (LIFO) instead of a deque (FIFO) is what
    # turns this into a depth-first traversal instead of breadth-first.
    stack = [("root", tree)]
    visited_order = []

    while stack:
        # Pop from the right -> most recently pushed node is explored first,
        # so we go as deep as possible before backtracking to siblings.
        path, node = stack.pop()

        # Start to fill the list as soon as the category matches
        if path.startswith(category):
            visited_order.append(path)
        # If visited_order is not empty and the category no longer matches
        # there will be no more category match so the loop can stop there
        elif visited_order:
            break

        # Top-level children are shown without the "root" prefix,
        # every deeper level gets "parent_path/child_name"
        prefix = "" if path == "root" else f"{path}/"

        if node:  # non-empty dict -> has children
            # Push children in reverse order so that, once popped one by one,
            # they come out in their original left-to-right order.
            for key, value in reversed(node.items()):
                stack.append((f"{prefix}{key}", value))

    return visited_order


def search_in_category(query: str, category: str, top_k: int = 10):
    query_tokens = tokenizer(query)

    results = get_query_results(query_tokens)

    cat_results = get_category_results(results, category)

    pondered_results = get_ranked_results(cat_results, top_k, len(query_tokens))

    return [
        pondered_result.product_id
        for pondered_result in sorted(
            pondered_results, key=lambda x: x.get_score, reverse=True
        )
    ]


def get_category_results(results, category: str):
    cat_results = dict()

    categories = list_categories_dfs(category_tree, category)

    for product_id, found_count in results.items():
        if products_index[product_id].get_category in categories:
            cat_results[product_id] = found_count
    return cat_results


if __name__ == "__main__":
    kb = [prod["id"] for prod in catalog if "Keyboard" in prod["name"]]

    order_cats = list_categories_dfs(category_tree, "Soft")
    print("\nList Categories:")
    print(order_cats)

    print("\nMatches:")
    prod_cat_list = [
        prod["id"]
        for prod in [product for product in catalog if product["id"] in kb]
        if prod["category"] in order_cats
    ]
    print(prod_cat_list)

    search_result = search_in_category("Keyboard Monitor", "Electronics")
    print("\nSearch in Category")
    print(search_result)
