from engine.suggest import levenshteinDistance


def test_levenshteinDistance():
    assert levenshteinDistance("abcd", "ebcfg") == 3
