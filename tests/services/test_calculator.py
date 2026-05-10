import pytest
from service.calculations import Calculator
from models.service import Density, ConversionKoefficient


@pytest.mark.parametrize(
    "loops,rows,height,width,expected_loop,expected_row",
    [
        (6, 6, 1, 1, 6, 6),
        (10, 5, 2, 4, 2.5, 2.5),
        (8, 4, 2.5, 4.0, 2.0, 1.6),
    ],
)
def test_calculate_density(loops, rows, height, width, expected_loop, expected_row):
    loop, row = Calculator.calculate_density(loops, rows, height, width)
    assert loop == expected_loop
    assert row == expected_row


@pytest.mark.parametrize(
    "loops,rows,height,width",
    [
        (-1, 6, 1, 1),
        (6, -1, 1, 1),
        (6, 6, -1, 1),
        (6, 6, 1, -1),
        (0, 6, 1, 1),
        (6, 0, 1, 1),
        (6, 6, 0, 1),
        (6, 6, 1, 0),
    ],
)
def test_invalid_parameters_raise_value_error(loops, rows, height, width):
    with pytest.raises(ValueError, match="Все параметры должны быть больше 0"):
        Calculator.calculate_density(loops, rows, height, width)


@pytest.mark.parametrize(
    "orig_loops,orig_rows,target_loops,target_rows,expected_loops_k,expected_rows_k",
    [
        (5, 5, 10, 10, 2.0, 2.0),
        (10, 10, 5, 5, 0.5, 0.5),
        (2, 4, 6, 8, 3.0, 2.0),
        (8, 6, 4, 3, 0.5, 0.5),
        (1, 1, 1, 1, 1.0, 1.0),
    ],
)
def test_calculate_density_conversion(
    orig_loops, orig_rows, target_loops, target_rows, expected_loops_k, expected_rows_k
):
    original = Density(loops=orig_loops, rows=orig_rows)
    target = Density(loops=target_loops, rows=target_rows)

    result = Calculator.calculate_density_conversion(original, target)

    assert result.loops_k == expected_loops_k
    assert result.rows_k == expected_rows_k
    assert isinstance(result, ConversionKoefficient)


@pytest.mark.parametrize(
    "orig_loops,orig_rows,target_loops,target_rows",
    [
        (-1, 5, 10, 10),  # отрицательное значение loops в original
        (5, -1, 10, 10),  # отрицательное значение rows в original
        (5, 5, -1, 10),  # отрицательное значение loops в target
        (5, 5, 10, -1),  # отрицательное значение rows в target
        (0, 5, 10, 10),  # нулевое значение loops в original
        (5, 0, 10, 10),  # нулевое значение rows в original
        (5, 5, 0, 10),  # нулевое значение loops в target
        (5, 5, 10, 0),  # нулевое значение rows в target
    ],
)
def test_calculate_density_conversion_invalid_parameters(
    orig_loops, orig_rows, target_loops, target_rows
):
    original = Density(loops=orig_loops, rows=orig_rows)
    target = Density(loops=target_loops, rows=target_rows)

    with pytest.raises(ValueError, match="Все параметры должны быть больше 0"):
        Calculator.calculate_density_conversion(original, target)
