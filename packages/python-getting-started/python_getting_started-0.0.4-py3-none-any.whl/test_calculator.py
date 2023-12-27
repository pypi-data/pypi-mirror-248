from calculator import calculate
from unittest.mock import Mock
import pytest


def test_calculate():
    assert calculate([1, 2, 3], '+') == 6
    assert calculate([2, 3, 4], '-') == -5
    assert calculate([2, 1, 5], '*') == 10
    with pytest.raises(Exception):
        calculate([1, 2, 4], '!')


@pytest.fixture
def mock_get():
    mock = Mock()
    mock.calculate.return_value = 4
    return mock


def test_mock_calculate(mock_get):
    response = mock_get.calculate([1, 2, 4], '+')
    assert response == 4
    response = mock_get.calculate([123, 23], '!')
    assert response == 4
