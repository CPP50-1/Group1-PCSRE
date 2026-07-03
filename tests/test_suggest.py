from engine.suggest import levenshteinDistance, suggest


def test_levenshteinDistance():
    assert levenshteinDistance("abcd", "ebcfg") == 3

def test_suggest_existing_tokens_only(capsys):
    suggest("Keyboard Monitor")
    captured = capsys.readouterr()
    assert captured.out == ""

def test_suggest_title_non_existing_tokens_only(capsys):
    suggest("Keybard Montor")
    captured = capsys.readouterr()
    all_lines = captured.out.split("\n")
    assert all_lines[1] == "Did you mean?"
