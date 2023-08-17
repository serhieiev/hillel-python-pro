import re
import pytest


def validate_ukrainian_itn(itn):
    pattern = r'^[1-9]\d{9}$'
    return bool(re.match(pattern, itn))


@pytest.mark.parametrize("itn, expected", [
    ('1234567890', True),
    ('9876543210', True),
    ('0234567890', False),
    ('12345A7890', False),
    ('123456789', False),
    ('12345678901', False),
])
def test_validate_ukrainian_itn(itn, expected):
    assert validate_ukrainian_itn(itn) == expected
