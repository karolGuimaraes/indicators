import sys
sys.path.insert(1, '')
from indicators.views import bollinger_bands

quotes = {
    0: 90.70,
    1: 92.90,
    2: 92.98,
    3: 91.80,
    4: 92.66,
    5: 92.68,
    6: 92.30,
    7: 92.77,
    8: 92.54,
    9: 92.95,
    10: 93.20,
    11: 91.07,
    12: 89.83,
    13: 89.74,
    14: 90.40,
    15: 90.74,
    16: 88.02,
    17: 88.09,
    18: 88.84,
    19: 90.78,
    20: 90.54,
    21: 91.39,
    22: 90.65
}

def test_bollinger_upper_band():

    bolu, _ = bollinger_bands(quotes)
    
    assert round(bolu, 2) == 94.15

def test_bollinger_lower_band():

    _, bold = bollinger_bands(quotes)

    assert round(bold, 2) == 87.95
