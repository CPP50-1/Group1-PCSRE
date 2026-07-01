import os
import sys # Unused import

def my_messy_function(   ):
    x=10
    y   = 20
    # This line is intentionally way too long to see if the Ruff formatter will chop it down to adhere to the 79 character limit set in thetoml file
    return x+y