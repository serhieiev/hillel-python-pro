import re
import pytest


# explanation https://auto.24tv.ua/nomery_avtomobiliv_v_ukraini_po_oblastiakh_khto_zvidky_n5661
def validate_vehicle_plate(plate):
    pattern = r'^(AX|KX|AE|KE)(?!0000)\d{4}[АВЕИКМНОРСТХ]{2}$'
    return bool(re.match(pattern, plate))


@pytest.mark.parametrize("plate, expected", [
    ('AX1234АВ', True),
    ('KX9876ЕХ', True),
    ('AE0001КМ', True),
    ('KE5555ОР', True),
    ('AE0000КМ', False),
    ('AE123AКМ', False),
    ('AX12345АВ', False),
    ('XY1234АВ', False),
    ('AX123АВ', False),
    ('AX1234AB', False),
    ('KE1234АП', False),
    ('AE5678СI', False),
])
def test_validate_car_plate(plate, expected):
    assert validate_vehicle_plate(plate) == expected
