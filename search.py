import argparse

import engine.index


def main():
    parser = argparse.ArgumentParser(
        prog='research-CLI',
        description="Products search tool"
    )
    
    parser.add_argument("query", help="search query")
    
    parser.add_argument("-t", "--top", help="top N results", type=int, default=10)
    parser.add_argument("-c", "--cat", help="Category filter", type=str, default='')
    
    
    args = parser.parse_args()
    
    #engine.index.build_indexes()
    
    if not args.cat:
        engine.ranking.search_ranking(args.query, args.top)
    else:
        pass #use future search with cat function
if __name__ == "__main__":
    main()