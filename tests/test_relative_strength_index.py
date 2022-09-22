import sys
sys.path.insert(1, '')
from indicators.views import relative_strength_index

def test_relative_strength_index():
    gains = {
        0: 0,
        1: 0.04,
        2: 0,
        3: 0.42,
        4: 0.55,
        5: 0.16,
        6: 0.23,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0.09,
        12: 0.13,
        13: 0.35
    }

    losses = {
        0: 0.17,
        1: 0,
        2: 0.20,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0.41,
        8: 0.40,
        9: 0.26,
        10: 0.78,
        11: 0,
        12: 0,
        13: 0
    }


    rsi = relative_strength_index(gains, losses)
    assert round(rsi, 2) == 47.02