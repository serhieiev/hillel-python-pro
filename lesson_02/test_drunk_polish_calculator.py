import pytest

from unittest.mock import patch

from drunk_polish_calculator import op_plus, op_minus, op_multiply, op_divide, main


# Test op_plus function
@pytest.mark.parametrize("x,y,expected_result", [(1, 2, 3), (-1, 1, 0), (0, 0, 0)])
def test_op_plus(x: float, y: float, expected_result: float):
    result = op_plus(x, y)
    
    assert result == expected_result

# Test op_minus function
@pytest.mark.parametrize("x,y,expected_result", [(1, 2, 1), (2, 1, -1), (0, 0, 0)])
def test_op_minus(x: float, y: float, expected_result: float):
    result = op_minus(x, y)
    
    assert result == expected_result

# Test op_multiply function
@pytest.mark.parametrize("x,y,expected_result", [(1, 2, 2), (-1, 1, -1), (0, 0, 0)])
def test_op_multiply(x: float, y: float, expected_result: float):
    result = op_multiply(x, y)
    
    assert result == expected_result

# Test op_divide function
@pytest.mark.parametrize("x,y,expected_result", [(1, 2, 0.5), (2, 1, 2.0), (-2, 1, -2.0)])
def test_op_divide(x: float, y: float, expected_result: float):
    result = op_divide(x, y)
    
    assert result == expected_result
    with pytest.raises(ZeroDivisionError):
        op_divide(1, 0)

# Test main function
@pytest.mark.parametrize(
    "expression, expected_output",
    [
        ("2 3 +", "5.0"),
        ("2 3 *", "6.0"),
        ("2 3 -", "1.0"),
        ("6 3 /", "2.0"),
        ("2 3 4 * +", "14.0"),
    ]
)
def test_main(capsys, expression, expected_output):
    with patch('builtins.input', return_value=expression):
        main()
    
    assert capsys.readouterr().out.rstrip() == expected_output