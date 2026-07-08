import argparse
import json

import engine.index
import engine.suggest
from engine.categories import search_in_category


def display_item(index: int, item: dict):
    print("{:>5}. [{}] {}".format(index, item["id"], item["name"]))
    print("       {}".format(item["category"]))
    print(
        "       €{} | {} in stock | rank #{}".format(
            item["price"], item["stock"], item["sales_rank"]
        )
    )
    print()


def main():
    parser = argparse.ArgumentParser(
        # prog="research-CLI",
        description="Products search tool"
    )

    parser.add_argument("query", help="search query")

    parser.add_argument("-t", "--top", help="top N results", type=int, default=10)
    parser.add_argument(
        "-c", "--category", help="Category filter", type=str, default=""
    )

    args = parser.parse_args()

    if not args.category:
        items_list = engine.ranking.search_ranking(args.query, args.top)
    else:
        items_list = search_in_category(args.query, args.category, args.top)

    with open("catalog.json") as json_data:
        data = json.load(json_data)

    for index, id in enumerate(items_list):
        for item in data:
            if item["id"] == id:
                display_item(index + 1, item)

    engine.suggest.suggest(args.query)


if __name__ == "__main__":
    main()
