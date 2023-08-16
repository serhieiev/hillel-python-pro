import re
import pytest

def validate_vehicle_plate(plate):
    pattern = r'^(AX|KX|AE|KE)\d{4}[АВЕИКМНОРСТХ]{2}$'
    return bool(re.match(pattern, plate))


@pytest.mark.parametrize("plate, expected", [
    ('AX1234АВ', True),
    ('KX9876ЕХ', True),
    ('AE0000КМ', True),
    ('KE5555ОР', True),
    ('AX12345АВ', False),
    ('XY1234АВ', False),
    ('AX12АВ', False),
    ('AX1234AB', False),
    ('KE1234АВ', True),
    ('AE5678СТ', True),
    ('KX9012КМ', True),
    ('AE3410РС', True),
])
def test_validate_car_plate(plate, expected):
    assert validate_vehicle_plate(plate) == expected
