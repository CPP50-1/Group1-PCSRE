## Inverted Index

### Data Structure Used and Why

The inverted index is implemented as a **dictionary of sets**. Each key is a unique token (a word extracted from the product name or tags), and its corresponding value is a set of all product IDs that contain that token.

We use dictionaries and sets because dictionary key lookups and set insertions both operate in **O(1)** average time.

To build the list of tokens for a given product, we tokenize the product name into a set and compute the union with the product's tags (which are already in a list). Using a set operation here deduplicates the tokens for that specific product.

The tokenizer uses a regular expression to iterate over the product name, splitting it into raw words. It then filters out short words (length ≤2) and lowercases the valid ones before adding them to the final token set. Finally, we iterate through this combined list of tokens. If a token is not yet a key in the inverted index, we add it. Then, we insert the product's ID into that token's set.

Using a set for the values prevents ID duplication and allows for fast, deduplicated lookups when searching.

### Build Time and Space Complexity

**Time Complexity: O(N)** Let N be the total number of products in the catalog. We iterate through the N products exactly once. For each product, we process its name through the tokenizer. While string processing takes time proportional to the string's length, the length of a product name is bounded and does not grow as the catalog gets larger. Therefore, relative to the total number of products, tokenizing takes a constant amount of time, O(1).

Similarly, inserting the resulting tokens into our dictionary and sets takes O(1) average time per token. Because we perform a constant number of operations for each of the N products, the overall build time complexity scales linearly, making it **O(N)**.

**Space Complexity: O(N)** The space complexity is also **O(N)**. The tokenizer requires temporary space proportional to the length of a single product name, which is O(1) relative to the catalog. However, the inverted index itself stores every unique token and maps it to product IDs. In the worst-case scenario, the number of unique tokens and IDs stored in the dictionary of sets will grow linearly with the number of products in the catalog.

### Average Query Time Complexity

-   **Single-Word Queries: O(1)** A single-word search requires only one dictionary lookup. Since hash map lookups operate in constant time, retrieving the set of matching product IDs is an O(1) operation.
-   **Multi-Word Queries (Inclusive / "OR" Search): O(M)** If the logic requires returning products that match _any_ of the searched words, we must perform a set union. The complexity becomes O(M), where M is the total sum of all product IDs across the matching sets.
-   **Multi-Word Queries (Total / "AND" Search): O(min(A,B))** If the logic requires returning only products that match _all_ searched words, we perform a set intersection. Python optimizes this by iterating through the smallest set and performing O(1) membership checks against the larger sets. This results in a time complexity of O(min(A,B)), where A and B represent the sizes of the sets being intersected.

## Ranked Search

### Data Structure Used and Why

The ranked search relies on two data structures built simultaneously during initialization: the **inverted index** and the **product index**.

The product index maps each `product_id` to an instance of `ProductData` (containing the ID, category, stock, and sales rank). Storing the product as a class instance makes the code more readable than using a tuple, adding negligible memory and speed overhead for a catalog of only 5,000 products.

**1\. Tokenization and Initial Match Count** The ranking process begins by tokenizing the user's search query. These query tokens are passed to the `get_query_results` method, which builds a results dictionary to track initial relevance.

To find matches, we iterate through the query tokens. For each token, we look up its corresponding set of product IDs in the inverted index. We then iterate through that set of IDs, adding each to our results dictionary and incrementing its count. The resulting dictionary uses the matching product IDs as keys, and the values represent the "match count" (how many individual tokens from the search query were found in that product).

**2\. Calculating the Weighted Score** To get the final ranked results, we pass the dictionary of matched products, the `top_k` limit (how many items to display), and the total length of the query to the `get_ranked_results` function.

This function builds a list of weighted results by iterating over every matched product. For each product, it retrieves the current stock and sales rank in O(1) time via the product index. It passes these metrics, along with the initial match count and query length, to the `_ponderer` helper function. This helper applies our business logic formula to return a final **weighted score** for the product.

**3\. Fetching the Top K Results** To optimize performance, we use a **min-heap** to keep only the `top_k` highest-scoring items in memory:

-   If the heap isn't full yet (`len < top_k`), we push the newly scored product onto the heap.
-   If the heap is full, we check the lowest score currently in our top K (`pondered_results[0]`). If the new product has a better score, it kicks out the lowest-scoring item and replaces it (`heapreplace`).

Finally, because a min-heap only guarantees the smallest item is at the front (but doesn't strictly sort the rest), we pass the heap through Python's `sorted()` function in descending order. This ensures we return the list of `product_id`s strictly ordered from best to worst score.

### Search Time Complexity

Given:

-   **C**: The number of characters in the user's search query.
-   **M**: The total number of matched IDs across all tokens.
-   **U**: The number of _unique_ products matched (U≤M).
-   **K**: The `top_k` limit (the maximum number of results to return).

Here is the step-by-step breakdown:

1.  **Tokenizing the Query: O(C)** The `tokenizer` scans the search string to split it into words. This scales linearly with the length of the query (C). Because search queries are generally very short, this is practically instantaneous, but strictly speaking, it is O(C).
2.  **Fetching Initial Match Counts: O(M)** As established, `get_query_results` looks up each token in the inverted index and iterates through the resulting sets. It performs M total O(1) dictionary updates, resulting in O(M) time.
3.  **Scoring and Min-Heap (`get_ranked_results`): O(UlogK)** We iterate through the U unique products found in step 2.
    
    -   Calculating the score takes O(1).
    -   Pushing to or replacing an item in a min-heap of size K takes O(logK) time. Because we perform an O(logK) operation for each of the U unique products, this step takes **O(UlogK)**.
4.  **Final Sort: O(KlogK)** Because the heap contains K items, sorting it with `sorted()` takes **O(KlogK)**. Extracting the `product_id`s from the sorted list takes an additional O(K).

**Final Ranking Complexity** Total Time = O(C+M+UlogK+KlogK)

1.  C (query length) is negligible.
2.  K is smaller than or equal to U, so the sorting step O(KlogK) is overshadowed by the heap building step O(UlogK).

Therefore, the simplified global time complexity is: **O(M+UlogK)**

## Category Tree Filter

### Data Structure Used and Why

`catalog.json` is parsed into a list of dictionaries. A list comprehension is then used to extract the categories, which are converted into a `set` of unique product paths and sorted alphabetically using `sorted()`. Sorting the paths groups categories with the same prefix together, allowing us to exit early during the depth-first search (DFS) traversal of the category tree.

We create an autovivification dictionary by defining a `nested_dict` function that returns a `defaultdict` using itself as the default factory. When attempting to access a key that doesn't exist, instead of throwing a `KeyError` like a standard dictionary, `defaultdict` catches the missing key, calls the `nested_dict` function, and assigns the resulting empty `defaultdict` as the value for the new key. This allows the dictionaries to spawn infinitely deep.

The category tree is built by splitting each string from the sorted list by its delimiter (`/`). We then iterate through these split components, moving a pointer progressively deeper into the autovivification dictionary, which automatically generates the required nested levels for each category component.

Once the dictionary is built, we simplify this recursive structure into a standard nested dictionary. This allows us to safely check for keys without accidentally creating new nested entries, and it replaces the trailing empty dictionaries with `None` to explicitly mark the leaves (endpoints) of the tree.

**Search Execution** To traverse the category tree, we use a Last-In, First-Out (LIFO) approach with a stack (DFS). This allows the algorithm to explore a complete category branch down to its leaves before backtracking to sibling categories.

When adding a node's children to the stack, we iterate through them in `reversed()` order. Because Python dictionaries maintain insertion order—and we previously built the tree from a `sorted()` list of paths—the children are naturally stored in alphabetical order. Pushing them onto the stack in reverse guarantees that they are popped off and evaluated in their original, correct left-to-right alphabetical order.

Because all matching subcategories of a target prefix will be grouped consecutively, we can append matches to `visited_order` as we find them. The moment we find a path that _does not_ match the prefix _after_ matches have already been found, we know we have completely exited the relevant alphabetical section of the tree. The loop `break`s immediately, skipping the evaluation of the rest of the catalog.

When a query is made, it is tokenized, and we find the list of products matching the tokens using the inverted index, tracking the match count for each product. Using the DFS tree traversal logic, we get a list of all valid subcategories, loop through the ranked results, and drop any result whose category is not in the valid DFS list. Finally, the raw hit counts of the filtered products are converted into relevance scores, sorted in descending order, and the top K clean IDs are returned.

### Time Complexity

#### Tree Building (Two-Pass Approach)

-   **Pass 1 (Building):** For N paths, we split the string and iterate through its L parts, doing a dictionary lookup/insertion for each. This takes O(N×L) time.
-   **Pass 2 (Simplifying):** The `simplify()` function recursively visits every unique node in the generated tree exactly once. Because many paths share the same parent categories, the number of unique nodes V is much smaller than N×L. This pass takes O(V) time.
-   **Total Build Complexity:** O(N×L)+O(V). Since V≤N×L, this simplifies to **O(N×L)**.

We could avoid iterating through the dictionary twice by using the `setdefault()` method (or a standard dictionary) and marking the leaves as `None` in a single pass. This would come at the cost of more complex end-of-path detection logic. However, because `simplify()` only iterates over the _unique_ categories in the tree rather than the original flat list of paths, the performance difference is negligible.

#### Depth-First Search Category Traversal

-   **Worst-case:** O(V), where V is the total number of unique nodes (categories) in the tree. This occurs if the target category is at the very end of the alphabet or doesn't exist, requiring us to visit every node.
-   **Best/Average-case:** O(M+Kcat​), where M is the number of nodes evaluated before finding the first match, and Kcat​ is the number of actual matching subcategories. Because of the early `break`, the time complexity is bound to traversing until the end of the matching block, completely bypassing the remaining V−(M+Kcat​) nodes.


---

## "Did you mean?" suggestions

### Data structure used and why

### Time complexity

---

## CLI

### Data structure used and why

### Time complexity


