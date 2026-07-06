def levenshteinDistance(s1, s2, max_edit):
    """
    Return the levenshtein distance between two words, or max_edit+1 where max_edit is
    the maximum levenshtein distance we tolerate
    """

    # early exit if the two strings are identical
    if s1 == s2:
        return 0

    OUT_OF_BOUND = max_edit + 1

    if len(s1) > len(s2):
        s1, s2 = s2, s1

    len_diff = len(s2) - len(s1)

    # early exit if the length of the target word is too big
    if len_diff > max_edit:
        return OUT_OF_BOUND

    # find the common prefix end if any
    min_len = min(len(s1), len(s2))

    left = 0
    while left < min_len and s1[left] == s2[left]:
        left += 1

    # find the common sufix start if any
    right1, right2 = len(s1) - 1, len(s2) - 1
    while right1 >= left and right2 >= left and s1[right1] == s2[right2]:
        right1 -= 1
        right2 -= 1

    # window of the strings to compare
    n = right1 - left + 1
    m = right2 - left + 1

    if n <= 0 or m <= 0:
        # one word is the prefix/sufix of the other
        return val if (val := n + m) <= max_edit else OUT_OF_BOUND

    row = [i if i <= max_edit else OUT_OF_BOUND for i in range(n + 1)]

    # shrink pointers for the matrix
    start = 1
    end = min(n + 1, (max_edit + m - n) // 2 + 1)

    for i in range(1, m + 1):
        c2 = s2[left + i - 1]

        if start == 1:
            row[0] = i

        prev = row[start - 1]
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

        # dynamic band squeezing
        while (
            end > 1 and row[end - 1] + abs((end - 1) - i - len_diff) > max_edit
        ):
            end -= 1
        end = min(n + 1, end + 1)
        while (
            start < end and abs(i + len_diff - start) + row[start] > max_edit
        ):
            start += 1
        if start >= end:
            return OUT_OF_BOUND

    return row[n] if row[n] <= max_edit else OUT_OF_BOUND
