import timeit

# The exact vocabulary from the dataset generator
WORDS = [
    "wireless",
    "ergonomic",
    "compact",
    "portable",
    "mechanical",
    "bluetooth",
    "usb",
    "hdmi",
    "rechargeable",
    "adjustable",
    "gaming",
    "professional",
    "silent",
    "backlit",
    "foldable",
    "keyboard",
    "mouse",
    "monitor",
    "headset",
    "webcam",
    "chair",
    "desk",
    "lamp",
    "cable",
    "adapter",
    "router",
    "switch",
    "hub",
    "drive",
    "printer",
    "laser",
    "inkjet",
    "optical",
    "digital",
    "smart",
    "pro",
    "lite",
    "plus",
    "max",
    "ultra",
]

# Simulated user queries containing 1 or 2 typos
TEST_QUERIES = [
    "wireles",  # 1 edit from "wireless"
    "keyborad",  # 2 edits from "keyboard"
    "blutooth",  # 1 edit from "bluetooth"
    "mechancal",  # 1 edit from "mechanical"
    "rechargable",  # 1 edit from "rechargeable"
    "comptact",  # 1 edit from "compact"
    "profesional",  # 1 edit from "professional"
    "gamng",  # 1 edit from "gaming"
]


def levenshtein_with_stripping(s1, s2, max_edit=2):
    """The fully optimized algorithm with both squeeze and stripping."""
    if max_edit is None:
        max_edit = max(len(s1), len(s2))
    if s1 == s2:
        return 0
    OUT_OF_BOUND = max_edit + 1
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    len_diff = len(s2) - len(s1)
    if len_diff > max_edit:
        return OUT_OF_BOUND

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

        if curr_min > max_edit:
            return OUT_OF_BOUND

        while (
            end > 1 and row[end - 1] + abs((end - 1) - i + len_diff) > max_edit
        ):
            end -= 1
        end = min(n + 1, end + 1)
        while (
            start < end and row[start] + abs(start - i + len_diff) > max_edit
        ):
            start += 1
        if start >= end:
            return OUT_OF_BOUND

    return row[n] if row[n] <= max_edit else OUT_OF_BOUND


def levenshtein_without_stripping(s1, s2, max_edit=2):
    """The algorithm with the squeeze heuristic, but NO prefix/suffix stripping."""
    if max_edit is None:
        max_edit = max(len(s1), len(s2))
    if s1 == s2:
        return 0
    OUT_OF_BOUND = max_edit + 1
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    len_diff = len(s2) - len(s1)
    if len_diff > max_edit:
        return OUT_OF_BOUND

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

        if curr_min > max_edit:
            return OUT_OF_BOUND

        while (
            end > 1 and row[end - 1] + abs((end - 1) - i + len_diff) > max_edit
        ):
            end -= 1
        end = min(n + 1, end + 1)
        while (
            start < end and row[start] + abs(start - i + len_diff) > max_edit
        ):
            start += 1
        if start >= end:
            return OUT_OF_BOUND

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
                if len(s1) > len(s2):
                    s1, s2 = s2, s1

                total_evaluated_chars += len(s1) + len(s2)

                left = 0
                min_len = min(len(s1), len(s2))
                while left < min_len and s1[left] == s2[left]:
                    left += 1

                right1, right2 = len(s1) - 1, len(s2) - 1
                while (
                    right1 >= left
                    and right2 >= left
                    and s1[right1] == s2[right2]
                ):
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
    percentage_skipped = (
        (skipped_chars / total_chars) * 100 if total_chars else 0
    )
    print(f"Total characters in evaluated pairs: {total_chars}")
    print(f"Characters skipped by pointers:      {skipped_chars}")
    print(f"Percentage of work bypassed:         {percentage_skipped:.1f}%\n")

    print(f"--- TIMING BENCHMARK ({ITERATIONS} iterations) ---")

    time_without = timeit.timeit(
        lambda: run_test(levenshtein_without_stripping), number=ITERATIONS
    )
    print(f"Without Stripping: {time_without:.4f} seconds")

    time_with = timeit.timeit(
        lambda: run_test(levenshtein_with_stripping), number=ITERATIONS
    )
    print(f"With Stripping:    {time_with:.4f} seconds")
    print("-" * 50)

    if time_with < time_without:
        improvement = ((time_without - time_with) / time_without) * 100
        print(f"Result: Prefix/Suffix stripping is {improvement:.1f}% FASTER.")
    else:
        penalty = ((time_with - time_without) / time_without) * 100
        print(f"Result: Prefix/Suffix stripping is {penalty:.1f}% SLOWER.")
