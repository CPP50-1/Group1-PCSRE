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

The **Levenshtein distance** represents the minimal number of single-character edits (insertions, deletions, or substitutions) required to transform a source string into a target string.

To map out these edits, we place the two words on the perpendicular axes of a matrix: the source word on the horizontal axis (left to right) and the target word on the vertical axis (top to bottom). Every step through this matrix represents a potential string manipulation.

### Navigating the Matrix

Moving through the matrix reflect how the word is altered. The cost of an edit depends on the direction of your movement:

-   **Diagonal (↘):** Represents a **Match** (no cost) or a **Substitution** (+1 cost).
-   **Right (→):** Represents a **Deletion** from the source string (+1 cost).
-   **Down (↓):** Represents an **Insertion** into the target string (+1 cost).

### Computing the Shortest Path

To find the minimum edit distance, the algorithm calculates a numerical cost for every cell in the grid by looking at the three adjacent cells that could lead to the current cell (top, left, and top-left diagonal), calculates the cost of that specific move, and carries forward the lowest resulting number.

Here is how the costs are calculated for the first two rows using the transition from **COT** to **CAT**:

|     | **None** | **C** | **O** | **T** |
| --- | --- | --- | --- | --- |
| **None** | 0 (↘) | 1 (→) | 2 (→) | 3 (→) |
| **C** | 1 (↓) | 0 (↘) | 1 (→) | 2 (→) |

**1\. First Row (`None`)** To go from "COT" to an empty string ("None"), our only option is to keep moving right and deleting letters:

-   `None` to `None` = 0
-   `C` to `None` = 0 + 1 = **1**
-   `O` to `None` = 1 + 1 = **2**
-   `T` to `None` = 2 + 1 = **3**

**2\. Second Row (`C`)** The algorithm evaluates all three incoming paths to pick the lowest cost.

-   **For the cell (`C`, `C`):**
    
    -   From Top: 1 + 1 = 2
    -   From Left: 1 + 1 = 2
    -   From Diagonal: 0 + 0 (Letters match) = **0**
    -   _Result:_ We pick the diagonal move (↘) because 0 is the lowest cost.
-   **For the cell (`O`, `C`):**
    
    -   From Top: 2 + 1 = 3
    -   From Left: 0 + 1 = **1**
    -   From Diagonal: 1 + 1 (Letters don't match) = 2
    -   _Result:_ We pick the move from the left (→) because 1 is the lowest cost.

By filling out the entire grid using these rules, the final minimal cost will land in the bottom-right cell.

## Optimization (Bounded Approach)

A standard Levenshtein calculation requires O(N⋅M) compute time and memory. However, per spec, our goal is simply to find words that fall within a strict Levenshtein threshold of 2 and discard the rest. Therefore, computing the entire matrix wastes significant resources.

We can heavily optimize the algorithm using the following heuristics:

### 1\. Early Exits

-   **Length Delta:** The Levenshtein distance will always be at least the difference in length between the two words. If the length difference strictly exceeds our maximum allowed edits, we can skip the calculation entirely.
-   **Equality Check:** If the strings are completely identical, we immediately return 0.

### 2\. Prefix and Suffix Stripping

Identical consecutive letters at the beginning or end of the words do not contribute to the edit cost. We can effectively strip these common prefixes and suffixes. To achieve this without creating temporary strings in memory via slicing, we use two pointers to mark the bounds of the "unmatched" middle section. This allows us to skip large portions of the strings or exit early if one word is a direct substring of the other, which happens when a user make a typo toward the end of a word.

Benchmarks of two versions of the Levenshtein algorithm (both using the squeeze heuristic, but only one utilizing prefix/suffix stripping) shows that skipping 7.8% of the characters leads to a 12% speedup. The gain is large for two reasons: 

- we are effictively eliminating entire columns and rows from the matrix before computing it.
- shifting a pointer with a simple while loop is much cheaper than reading/writing to a list inside a nested `for` loop.

Code for the benchmarks:

```python
import timeit

# The exact vocabulary from the dataset generator
WORDS = [
    "wireless", "ergonomic", "compact", "portable", "mechanical",
    "bluetooth", "usb", "hdmi", "rechargeable", "adjustable",
    "gaming", "professional", "silent", "backlit", "foldable",
    "keyboard", "mouse", "monitor", "headset", "webcam",
    "chair", "desk", "lamp", "cable", "adapter",
    "router", "switch", "hub", "drive", "printer",
    "laser", "inkjet", "optical", "digital", "smart",
    "pro", "lite", "plus", "max", "ultra",
]

# Simulated user queries containing 1 or 2 typos
TEST_QUERIES = [
    "wireles",     # 1 edit from "wireless"
    "keyborad",    # 2 edits from "keyboard"
    "blutooth",    # 1 edit from "bluetooth"
    "mechancal",   # 1 edit from "mechanical"
    "rechargable", # 1 edit from "rechargeable"
    "comptact",    # 1 edit from "compact"
    "profesional", # 1 edit from "professional"
    "gamng",       # 1 edit from "gaming"
]

def levenshtein_with_stripping(s1, s2, max_edit=2):
    """The fully optimized algorithm with both squeeze and stripping."""
    if max_edit is None:
        max_edit = max(len(s1), len(s2))
    if s1 == s2: return 0
    OUT_OF_BOUND = max_edit + 1
    if len(s1) > len(s2): s1, s2 = s2, s1
    len_diff = len(s2) - len(s1)
    if len_diff > max_edit: return OUT_OF_BOUND

    min_len = min(len(s1), len(s2))
    left = 0
    while left < min_len and s1[left] == s2[left]:
        left += 1

    right1, right2 = len(s1) - 1, len(s2) - 1
    while right1 >= left and right2 >= left and s1[right1] == s2[right2]:
        right1 -= 1
        right2 -= 1

    n = right1 - left + 1
    m = right2 - left + 1

    if n <= 0 or m <= 0:
        val = n + m
        return val if val <= max_edit else OUT_OF_BOUND

    row = [i if i <= max_edit else OUT_OF_BOUND for i in range(n + 1)]
    start = 1
    end = min(n + 1, max_edit + 2)

    for i in range(1, m + 1):
        c2 = s2[left + i - 1]
        prev = row[start - 1]
        row[start - 1] = OUT_OF_BOUND
        if start == 1:
            row[0] = i
        curr_min = OUT_OF_BOUND

        for j in range(start, end):
            if s1[left + j - 1] == c2:
                val = prev
            else:
                val = min(row[j], row[j - 1], prev) + 1
            prev = row[j]
            row[j] = val
            if val < curr_min:
                curr_min = val

        if curr_min > max_edit: return OUT_OF_BOUND

        while end > 1 and row[end - 1] + abs((end - 1) - i + len_diff) > max_edit:
            end -= 1
        end = min(n + 1, end + 1)
        while start < end and row[start] + abs(start - i + len_diff) > max_edit:
            start += 1
        if start >= end: return OUT_OF_BOUND

    return row[n] if row[n] <= max_edit else OUT_OF_BOUND


def levenshtein_without_stripping(s1, s2, max_edit=2):
    """The algorithm with the squeeze heuristic, but NO prefix/suffix stripping."""
    if max_edit is None:
        max_edit = max(len(s1), len(s2))
    if s1 == s2: return 0
    OUT_OF_BOUND = max_edit + 1
    if len(s1) > len(s2): s1, s2 = s2, s1
    len_diff = len(s2) - len(s1)
    if len_diff > max_edit: return OUT_OF_BOUND

    n = len(s1)
    m = len(s2)

    row = [i if i <= max_edit else OUT_OF_BOUND for i in range(n + 1)]
    start = 1
    end = min(n + 1, max_edit + 2)

    for i in range(1, m + 1):
        c2 = s2[i - 1]
        prev = row[start - 1]
        row[start - 1] = OUT_OF_BOUND
        if start == 1:
            row[0] = i
        curr_min = OUT_OF_BOUND

        for j in range(start, end):
            if s1[j - 1] == c2:
                val = prev
            else:
                val = min(row[j], row[j - 1], prev) + 1
            prev = row[j]
            row[j] = val
            if val < curr_min:
                curr_min = val

        if curr_min > max_edit: return OUT_OF_BOUND

        while end > 1 and row[end - 1] + abs((end - 1) - i + len_diff) > max_edit:
            end -= 1
        end = min(n + 1, end + 1)
        while start < end and row[start] + abs(start - i + len_diff) > max_edit:
            start += 1
        if start >= end: return OUT_OF_BOUND

    return row[n] if row[n] <= max_edit else OUT_OF_BOUND

def calculate_skip_stats():
    """Calculates how many characters are bypassed by the stripping logic."""
    total_evaluated_chars = 0
    skipped_chars = 0
    
    for query in TEST_QUERIES:
        for word in WORDS:
            # We only evaluate pairs that pass the initial length delta check
            if abs(len(query) - len(word)) <= 2:
                s1, s2 = query, word
                if len(s1) > len(s2): s1, s2 = s2, s1
                
                total_evaluated_chars += len(s1) + len(s2)
                
                left = 0
                min_len = min(len(s1), len(s2))
                while left < min_len and s1[left] == s2[left]:
                    left += 1
                    
                right1, right2 = len(s1) - 1, len(s2) - 1
                while right1 >= left and right2 >= left and s1[right1] == s2[right2]:
                    right1 -= 1
                    right2 -= 1
                
                n = right1 - left + 1
                m = right2 - left + 1
                
                if n > 0 and m > 0:
                    skipped_chars += (len(s1) - n) + (len(s2) - m)
                else:
                    skipped_chars += len(s1) + len(s2)
                    
    return total_evaluated_chars, skipped_chars

def run_test(func):
    for query in TEST_QUERIES:
        for word in WORDS:
            func(query, word, max_edit=2)

if __name__ == "__main__":
    ITERATIONS = 5000 
    
    print("--- PREFIX & SUFFIX STRIPPING STATISTICS ---")
    total_chars, skipped_chars = calculate_skip_stats()
    percentage_skipped = (skipped_chars / total_chars) * 100 if total_chars else 0
    print(f"Total characters in evaluated pairs: {total_chars}")
    print(f"Characters skipped by pointers:      {skipped_chars}")
    print(f"Percentage of work bypassed:         {percentage_skipped:.1f}%\n")
    
    print(f"--- TIMING BENCHMARK ({ITERATIONS} iterations) ---")
    
    time_without = timeit.timeit(lambda: run_test(levenshtein_without_stripping), number=ITERATIONS)
    print(f"Without Stripping: {time_without:.4f} seconds")
    
    time_with = timeit.timeit(lambda: run_test(levenshtein_with_stripping), number=ITERATIONS)
    print(f"With Stripping:    {time_with:.4f} seconds")
    print("-" * 50)
    
    if time_with < time_without:
        improvement = ((time_without - time_with) / time_without) * 100
        print(f"Result: Prefix/Suffix stripping is {improvement:.1f}% FASTER.")
    else:
        penalty = ((time_with - time_without) / time_without) * 100
        print(f"Result: Prefix/Suffix stripping is {penalty:.1f}% SLOWER.")
```

### 3\. Space Complexity Reduction (1D Array)

The algorithm only ever moves forward (right, down, or diagonal-right), therefor calculating the current row only requires the data from the immediately preceding row. Instead of storing the full N×M matrix in memory, we only need to store a single array representing the previous row, updating it as we step downward.

Because the row length is based on the length of the horizontal string (`s1`), making `s1` the shortest string ensures that the array take as little memory as possible.

### 4\. Dynamic Band Width

Because we have a strict threshold (maximum of 2 edits, per spec), we do not need to compute the entire grid. Any path that strays too far from the diagonal will naturally exceed our limit. To save compute time, we only evaluate a narrow "band" of cells around the diagonal and apply two optimization rules as we process each row:

-   **Row-Level Early Exit:** If the absolute lowest cost in the current row is already higher than our threshold, we stop computing immediately: no valid path remains.
-   **Dynamic Squeezing:** After finishing a row, we evaluate the outer edges of our calculation band. For these edge cells, we calculate the absolute minimum number of grid steps required to reach the bottom-right corner. If a cell's current cost plus this remaining distance exceeds the threshold, that path is mathematically doomed. We shrink the band to exclude these failing paths, reducing the number of cells computed in the next row.

Because the squeeze calculation runs only once per row, on average the overhead of this calculation is worth it if the band is smaller than the matrix, and the max_edit distance is small, to allow paths to fail quickly. E.g words under 4 chars wont benefit from this optimisation, because the band will be approximatively the same size as the matrix. For longer words, with a small treshold, this significantly improve performance as the matrix expand quickly (length of s1 x length of s2). 

(Benchmarks)[./tests/benchmarks/benchmarks_levenshtein_with_squeeze.py] show that implementing the dynamic band width logic with our current dictionnary produce in average a 32% speed up.

### Trie-based Levenshtein Automaton Approach

Because our entire catalog uses a vocabulary pool of 40 words, implementing a Trie, which would involves jumping through nested dictionary keys or object pointers for every single letter (slow in Python) would only start to pay off if the user make a lot of mistakes and we allow a high treshold (since we already strip the suffix/prefix), or if the dictionary list becomes very large (thousands of words), were branch prunning would allow saving thousands of loops: if the dictionary double in size, the compute time double, while using a Trie would NOT double the work because prefixes are shared, flattening the execution time into a logarithmic curve. The exact cutoff point where a Trie become more performant than the the list approach depend on the density of prefixes of our dictionary


We (benchmarked)[./tests/benchmarks/benchmarks_trie.py] the Trie approach against our optimized, flat-list bounded Levenshtein algorithm (utilizing dynamic band squeezing and prefix/suffix pointer stripping). The benchmark showed that the flat-list approach was ~65% faster (approx. 4.1s vs 12.1s over 5,000 iterations). We therefore chose the list approach, which is currently the better fit for the dataset size.

Same conclusion for the DAWG approach (Trie where the identical leaves are fused together using hashing) + NFA (Nondeterministic Finite Automaton). 

### Time complexity

---

## CLI

### Data structure used and why

### Time complexity
