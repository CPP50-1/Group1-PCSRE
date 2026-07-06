from engine.suggest import levenshteinDistance


def test_levenshteinDistance():
    assert levenshteinDistance("abcd", "ebcfg") == 3
    assert levenshteinDistance("hello", "hello", 2) == 0
    assert levenshteinDistance("", "", 2) == 0
    assert levenshteinDistance("a" * 100, "a" * 100, 1) == 0

    # 2. Length Difference Exceeds k
    assert levenshteinDistance("a", "abcde", 2) == 3
    assert levenshteinDistance("", "abc", 1) == 2
    assert levenshteinDistance("abcde", "a", 2) == 3

    # 3. Prefix/Suffix Cases
    assert levenshteinDistance("abc", "abcdef", 3) == 3
    assert levenshteinDistance("def", "abcdef", 3) == 3
    assert levenshteinDistance("abc", "abcdef", 2) == 3

    # 4. Exact Distance == k
    assert levenshteinDistance("cat", "cut", 1) == 1
    assert levenshteinDistance("kitten", "sitting", 3) == 3

    # 5. Distance == k + 1 (Just out of bounds)
    assert levenshteinDistance("cat", "cot", 0) == 1
    assert levenshteinDistance("kitten", "sitting", 2) == 3

    # 6. Transpositions
    assert levenshteinDistance("ab", "ba", 2) == 2
    assert levenshteinDistance("ab", "ba", 1) == 2

    # 7. Long Strings with Minor Edits
    assert levenshteinDistance("a"*50 + "b" + "a"*50, "a"*101, 1) == 1
    assert levenshteinDistance("a"*50 + "bc" + "a"*50, "a"*102, 2) == 2

    # 8. Complete Mismatches
    assert levenshteinDistance("abc", "xyz", 3) == 3
    assert levenshteinDistance("abc", "xyz", 2) == 3

    # 9. No `k` Provided (k = None, full evaluation)
    assert levenshteinDistance("kitten", "sitting") == 3
    assert levenshteinDistance("flaw", "lawn") == 2
    assert levenshteinDistance("", "abc") == 3
    assert levenshteinDistance("abc", "") == 3
    assert levenshteinDistance("hello", "hello") == 0
    assert levenshteinDistance("abc", "xyz") == 3
    assert levenshteinDistance("short", "much_longer_string") == 14

    # 10. Regression Tests (Denis's reports)
    assert levenshteinDistance("kaybard", "keyboard", 2) == 2
    assert levenshteinDistance("kaybard", "keyboard", 3) == 2
    assert levenshteinDistance("abcdef", "ghijklm", 2) == 3
    assert levenshteinDistance("abcdef", "ghijklm") == 7
