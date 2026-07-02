from engine.tokenize import tokenizer


def test_tokenizer():
    assert tokenizer("Hello, world!") == {"hello", "world"}
