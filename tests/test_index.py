from engine.index import build_reverse_index


def test_build_reverse_index():
    sample_json_data = [
        {
            "id": "P04236",
            "name": "Ergonomic Adjustable",
            "category": "Electronics/Computers/Laptops",
            "tags": ["rechargeable", "portable", "wireless"],
            "price": 100.93,
            "stock": 66,
            "sales_rank": 3667,
        },
        {
            "id": "P04237",
            "name": "Max GamingSmart Mouse",
            "category": "Networking/Switches",
            "tags": ["desk", "portable", "plus"],
            "price": 490.38,
            "stock": 49,
            "sales_rank": 1912,
        },
        {
            "id": "P04238",
            "name": "Foldable Gaming Max",
            "category": "Electronics/Phones/Smartphones",
            "tags": ["adapter", "hdmi", "inkjet", "switch"],
            "price": 589.85,
            "stock": 457,
            "sales_rank": 4256,
        },
    ]

    assert build_reverse_index(sample_json_data) == {
        "portable": {"P04236", "P04237"},
        "wireless": {"P04236"},
        "rechargeable": {"P04236"},
        "adjustable": {"P04236"},
        "ergonomic": {"P04236"},
        "gamingsmart": {"P04237"},
        "desk": {"P04237"},
        "max": {"P04238", "P04237"},
        "plus": {"P04237"},
        "mouse": {"P04237"},
        "gaming": {"P04238"},
        "foldable": {"P04238"},
        "hdmi": {"P04238"},
        "switch": {"P04238"},
        "adapter": {"P04238"},
        "inkjet": {"P04238"},
    }
