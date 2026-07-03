## Inverted Index

### Data Structure Used and Why

The reverse index is implemented as a **dictionary of sets**. Each key is a unique token (a word extracted from the product name or tags), and its corresponding value is a set of all product IDs that contain that token.

We use dictionaries and sets because dictionary key lookups and set insertions both operate in **O(1) average time**.

To build the list of tokens for a given product, we tokenize the product name into a set and compute the union with the product's tags (which is already a list). Using a set operation here deduplicates the tokens for that specific product.

The tokenizer uses a regular expression to iterate over the product name, splitting it into raw words. It then iterates over these raw words, filtering out short words (length ≤2) and lowercasing the valid ones before adding them to the final token set. Finally, we iterate through this combined list of tokens. If a token is not yet a key in the reverse index, we add it. Then, we insert the product's ID into that token's set.

Using a set for the values prevents ID duplication and allows for fast lookups when searching.

### Build Time and Space Complexity

**Time Complexity: O(N)** Let N be the total number of products in the catalog. We iterate through the N products exactly once. For each product, we process its name through the tokenizer. While string processing takes time proportional to the string's length, the length of a product name is bounded and does not grow as the catalog gets larger. Therefore, relative to the total number of products, tokenizing takes a constant amount of time, O(1).

Similarly, inserting the resulting tokens into our dictionary and sets takes O(1) average time per token. Because we perform a constant number of operations for each of the N products, the overall build time complexity scales linearly, making it **O(N)**.

**Space Complexity: O(N)** The space complexity is also **O(N)**. The tokenizer requires temporary space proportional to the length of a single product name, which is O(1) relative to the catalog. However, the reverse index itself stores every unique token and maps it to product IDs. In the worst-case scenario, the number of unique tokens and IDs stored in the dictionary of sets will grow linearly with the number of products in the catalog.

### Average Query time complexity

-   **Single-Word Queries: O(1)** A single-word search requires only one dictionary lookup. Since hash map lookups operate in constant time, retrieving the set of matching product IDs is an O(1) operation.
-   **Multi-Word Queries (Inclusive / "OR" Search): O(M)** If the logic requires returning products that match _any_ of the searched words, we must perform a set union. The complexity becomes O(M), where M is the total sum of all product IDs across the matching sets.
-   **Multi-Word Queries (Total / "AND" Search): O(min(A,B))** If the logic requires returning only products that match _all_ searched words, we perform a set intersection. Python optimizes this by iterating through the smallest set and performing O(1) membership checks against the larger sets. This results in a time complexity of O(min(A,B)), where A and B represent the sizes of the sets being intersected.

---

## Ranked search

### Data structure used and why

The ranked search relies on two data structures built simultaneously during initialization: the **reverse index** and the **product index**.

The product index maps each `product_id` to an instance of `ProductData` (containing the ID, category, stock, and sales rank). Storing the product as a class instance makes the code more readable than using a tuple, while negligble memory / speed cost for a catalog of only 5,000 products.

**1\. Tokenization and Initial Match Count** The ranking process begins by tokenizing the user's search query. These query tokens are passed to the `get_query_results` method, which builds a results dictionary to track initial relevance.

To find matches, we iterate through the query tokens. For each token, we look up its corresponding set of product IDs in the reverse index. We then iterate through that set of IDs, adding each to our results dictionary and incrementing its count. The resulting dictionary uses the matching product IDs as keys, and the values represent the "match count" (how many individual tokens from the search query were found in that product).

**2\. Calculating the Weighted Score** To get the final ranked results, we pass the dictionary of matched products, the `top_k` limit (how many items to display), and the total length of the query to the `get_ranked_results` function.

This function builds a list of weighted results by iterating over every matched product. For each product, it retrieves the current stock and sales rank in O(1) time via the product index. It passes these metrics, along with the initial match count and query length, to the `_ponderer` helper function. This helper applies our business logic formula to return a final **weighted score** for the product.

**3\. Fetching the Top K Results** To optimize performance, we use a **min-heap** to keep only the `top_k` highest-scoring items in memory:

-   If the heap isn't full yet (`len < top_k`), we push the newly scored product onto the heap.
-   If the heap is full, we check the lowest score currently in our top K (`pondered_results[0]`). If the new product has a better score, it kicks out the lowest-scoring item and replaces it (`heapreplace`).

Finally, because a min-heap only guarantees the smallest item is at the front (but doesn't strictly sort the rest), we pass the heap through Python's `sorted()` function in descending order. This ensures we return the list of `product_id`s strictly ordered from best to worst score.

### Build time complexity

Given:

-   **C**: The number of characters in the user's search query.
-   **M**: The total number of matched IDs across all tokens.
-   **U**: The number of _unique_ products matched (U≤M).
-   **K**: The `top_k` limit (the maximum number of resultsto return)

Here is the step-by-step breakdown:

## 1\. Tokenizing the Query: O(C)

The `tokenizer` scans the search string to split it into words. This scales linearly with the length of the query (C). Because search queries are generally very short (a few words), this is practically instantaneous, but strictly speaking, it is O(C).

## 2\. Fetching Initial Match Counts: O(M)

As we established, `get_query_results` looks up each token in the reverse index and iterates through the resulting sets. It performs M total O(1) dictionary updates, resulting in O(M) time.

## 3\. Scoring and Min-Heap (`get_ranked_results`): O(UlogK)

We iterate through the U unique products found in step 2.

-   Calculating the score takes O(1).
-   Pushing to or replacing an item in a min-heap of size K takes O(logK) time. Because we perform a O(logK) operation for each of the U unique products, this step takes **O(UlogK)**.

## 4\. Final Sort: O(KlogK)

Because the heap contains K items, sorting it with `sorted()` takes **O(KlogK)**. Extracting the `product_id`s from the sorted list takes an additional O(K).

### Final Ranking Complexity

**Total Time = O(C+M+UlogK+KlogK)**

1.  C (query length) is negligible.
2.  K is smaller than or equal to U, so the sorting step O(KlogK) is overshadowed by the heap building step O(UlogK).

Therefore the simplified global time complexity is:

**O(M+UlogK)**


---

## Category tree filter

### Data structure used and why

### Build time complexity

### Average Query time complexity

---

## "Did you mean?" suggestions

### Data structure used and why

### Build time complexity

### Average Query time complexity

---

## CLI

### Data structure used and why

### Build time complexity

### Average Query time complexity


