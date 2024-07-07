from contextlib import nullcontext
import pytest
import rf_string

@pytest.mark.parametrize('r_string, f_string, valid', (
    (r'hello_world', 'hello_world', True),
    (r'(?P<number>\d+)_test', 'bad_test', False),
    (r'(?P<number>\d+)_test', '{number:%d}_test', True),
    (r'(?P<number>\d+)_test', '{number:%f}_test', True),
))
def test_validation(r_string, f_string, valid):
    test_context = nullcontext() if valid else pytest.raises(rf_string.rf_string.InconsistentRfStringDefError)
    with test_context:
        rf_string.RFstr(r_string, f_string)
