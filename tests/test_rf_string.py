from contextlib import nullcontext
import pytest

from rf_string import rf_string, exceptions


@pytest.mark.parametrize('r_string, f_string, valid', (
        (r'hello_world', 'hello_world', True),
        (r'(?P<number>\d+)_test', '{number}_test', True),
        (r'(?P<word>\w+)_test', '{word}_test', True),
        (r'(?P<number>\d+)_test', 'bad_test', False),
        (r'(?P<number>\d+)_test', '05_test_{number}', False),
    ),
    ids=(
        'no-groups',
        'matching-int',
        'matching-word',
        'missing-f-param',
        'bad-roundtrip',
    )
)
def test_validation(r_string, f_string, valid):
    test_context = nullcontext() if valid else pytest.raises(exceptions.RFStringError)
    with test_context:
        rf_string.RFString(r_string, f_string)


def test_match_not_found():
    rf_stringer = rf_string.RFString(
        r'(?P<word>\w+)(?P<number>\d+)',
        '{word}{number}',
    )
    with pytest.raises(rf_string.MatchNotFoundError):
        rf_stringer.parse('15hello')


def test_redefining_values():
    rf_stringer = rf_string.RFString(
        r'(?P<word>\w+)(?P<number>\d+)',
        '{word}{number}',
    )
    values = rf_stringer.parse('hello15')
    values['number'] = 16
    values['word'] = 'goodbye'
    return_sample = rf_stringer.write(values)
    assert return_sample == 'goodbye16'


@pytest.mark.parametrize('r_string, f_string, sample', [
    (
        r'(?P<word>\w+)(?P<number>\d+)',
        '{word}{number}',
        'hello15',
    ),
    (
        r'(?P<number1>\d+)_(?P<number2>\d)(?P<word>\w+)(?P<number3>\d)',
        '{number1}_{number2}{word}{number3}',
        '1234_5hello6',
    ),
])
def test_roundtrip(r_string, f_string, sample):
    rf_stringer = rf_string.RFString(r_string, f_string)
    values = rf_stringer.parse(sample)
    roundtrip_sample = rf_stringer.write(values)
    assert sample == roundtrip_sample


def test_fstring_inference():
    rstring = r'(?P<digit>\d)hello(?P<character>\w)'
    rf_stringer = rf_string.RFString(rstring)
    assert rf_stringer._fstring == '{digit}hello{character}'
