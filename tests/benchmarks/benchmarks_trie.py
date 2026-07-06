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

# --- 1. TRIE IMPLEMENTATION ---

class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

class LevenshteinTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.word = word

    def search(self, query, max_edit=2):
        """Finds all words in the Trie within max_edit distance of the query."""
        results = []
        # The first row of the matrix is simply 0 to len(query)
        current_row = range(len(query) + 1)
        
        for char, node in self.root.children.items():
            self._search_recursive(node, char, query, current_row, results, max_edit)
            
        return results

    def _search_recursive(self, node, char, query, previous_row, results, max_edit):
        columns = len(query) + 1
        current_row = [previous_row[0] + 1]

        # Build the current row based on the previous row
        for c in range(1, columns):
            insert_cost = current_row[c - 1] + 1
            delete_cost = previous_row[c] + 1
            replace_cost = previous_row[c - 1] + (0 if query[c - 1] == char else 1)
            current_row.append(min(insert_cost, delete_cost, replace_cost))

        # If we reached the end of a word, check if it's within our threshold
        if current_row[-1] <= max_edit and node.word is not None:
            results.append(node.word)

        # BRANCH PRUNING: Only continue down this branch if the minimum cost 
        # in the current row is within the max_edit threshold.
        if min(current_row) <= max_edit:
            for next_char, next_node in node.children.items():
                self._search_recursive(next_node, next_char, query, current_row, results, max_edit)


# --- 2. LIST IMPLEMENTATION (Your optimized version) ---

def levenshtein_with_stripping(s1, s2, max_edit=2):
    if max_edit is None: max_edit = max(len(s1), len(s2))
    if s1 == s2: return 0
    OUT_OF_BOUND = max_edit + 1
    if len(s1) > len(s2): s1, s2 = s2, s1
    len_diff = len(s2) - len(s1)
    if len_diff > max_edit: return OUT_OF_BOUND

    min_len = min(len(s1), len(s2))
    left = 0
    while left < min_len and s1[left] == s2[left]: left += 1

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
        if start == 1: row[0] = i
        curr_min = OUT_OF_BOUND

        for j in range(start, end):
            if s1[left + j - 1] == c2:
                val = prev
            else:
                val = min(row[j], row[j - 1], prev) + 1
            prev = row[j]
            row[j] = val
            if val < curr_min: curr_min = val

        if curr_min > max_edit: return OUT_OF_BOUND

        while end > 1 and row[end - 1] + abs((end - 1) - i + len_diff) > max_edit: end -= 1
        end = min(n + 1, end + 1)
        while start < end and row[start] + abs(start - i + len_diff) > max_edit: start += 1
        if start >= end: return OUT_OF_BOUND

    return row[n] if row[n] <= max_edit else OUT_OF_BOUND

def search_list(query, vocabulary, max_edit=2):
    """Wraps the standalone function to match the Trie's output behavior."""
    results = []
    for word in vocabulary:
        if levenshtein_with_stripping(query, word, max_edit) <= max_edit:
            results.append(word)
    return results

# --- BENCHMARK EXECUTION ---

def run_trie_test(trie):
    for query in TEST_QUERIES:
        trie.search(query, max_edit=2)

def run_list_test(vocabulary):
    for query in TEST_QUERIES:
        search_list(query, vocabulary, max_edit=2)

if __name__ == "__main__":
    ITERATIONS = 5000 
    
    # 1. Measure Build Time (Load time complexity)
    build_start = timeit.default_timer()
    trie = LevenshteinTrie()
    for word in WORDS:
        trie.insert(word)
    build_end = timeit.default_timer()
    trie_build_time = (build_end - build_start) * 1000 # in ms
    
    print("--- BUILD TIME COMPLEXITY ---")
    print(f"List (No build needed):    0.00 ms")
    print(f"Trie Construction Time:    {trie_build_time:.2f} ms\n")
    
    print(f"--- QUERY TIME COMPLEXITY ({ITERATIONS} iterations) ---")
    
    time_list = timeit.timeit(lambda: run_list_test(WORDS), number=ITERATIONS)
    print(f"List + Bound Heuristics: {time_list:.4f} seconds")
    
    time_trie = timeit.timeit(lambda: run_trie_test(trie), number=ITERATIONS)
    print(f"Trie + Branch Pruning:   {time_trie:.4f} seconds")
    print("-" * 50)
    
    if time_trie < time_list:
        improvement = ((time_list - time_trie) / time_list) * 100
        print(f"Result: The Trie approach is {improvement:.1f}% FASTER.")
    else:
        penalty = ((time_trie - time_list) / time_list) * 100
        print(f"Result: The Trie approach is {penalty:.1f}% SLOWER.")