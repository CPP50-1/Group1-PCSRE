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

### Build time complexity

### Average Query time complexity

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


