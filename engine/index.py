import json

from engine.tokenize import tokenizer


class ProductData:
    def __init__(self, id, category, stock, sales_rank):
        self.id = id
        self.category = category
        self.stock = stock
        self.sales_rank = sales_rank

    @property
    def get_stock(self):
        return self.stock

    @property
    def get_sales_rank(self):
        return self.sales_rank


reverse_index = dict()
products_index = dict()


def build_indexes():
    with open("catalog.json") as json_data:
        data = json.load(
            json_data,
        )

    for product in data:
        '''
        Iterating once over all the json an creating a reverse index for the researches
        '''
        tokens = tokenizer(product["name"]).union(product["tags"])
        for token in tokens:
            if token not in reverse_index:
                reverse_index[token] = set()
            reverse_index[token].add(product["id"])

        '''
        Tanking advantage of the iteration to build the second index to get easy lookup of all information of products
        '''
        products_index[product["id"]] = ProductData(product["id"],
                                                    product["category"],
                                                    product["stock"],
                                                    product["sales_rank"]
                                                    )


build_indexes()
