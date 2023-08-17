import re
import pytest


def validate_ukrainian_passport(passport):
    pattern = r'^[A-Z]{2}\d{6}$'
    return bool(re.match(pattern, passport))


@pytest.mark.parametrize("passport, expected", [
    ('AB123456', True),
    ('XY987654', True),
    ('12345678', False),
    ('ABC45678', False),
    ('A1234567', False),
    ('AA12345', False),
    ('AB1234567', False),
    ('ab123456', False),
])
def test_validate_ukrainian_passport(passport, expected):
    assert validate_ukrainian_passport(passport) == expected
