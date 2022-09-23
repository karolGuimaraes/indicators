import sys
sys.path.insert(1, '')
import pytest
from indicators.views import exponential_moving_average

@pytest.mark.parametrize("current_price, days, last_ema, expected_ema", [
    (59.4, 3, 60.4, 59.9),
    (54.9, 3, 56.1, 55.5),
])
def test_exponential_moving_average(current_price, days, last_ema, expected_ema):
    ema = exponential_moving_average(current_price, days, last_ema)
    
    assert round(ema, 2) == expected_ema