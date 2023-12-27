import logging
from typing import List

logging.basicConfig()
logger = logging.getLogger("calculate")
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)


def calculate(values: List[int], operator: str) -> int:
    logger.info('started calculation for values %s, operator %s', values, operator)
    result = values[0]
    match operator:
        case '+':
            logger.debug('started addition operation')
            for i in range(1, len(values)):
                result = result + values[i]
        case '-':
            logger.debug('started subtraction operation')
            for i in range(1, len(values)):
                result = result - values[i]
        case '*':
            logger.debug('started multiplication operation')
            for i in range(1, len(values)):
                result = result * values[i]
    return result


def test_calculate():
    assert calculate([1, 2, 3], '+') == 6
    assert calculate([2, 3, 4], '-') == -5
    assert calculate([2, 1, 5], '*') == 10


def main():
    result = calculate([1, 2, 3], '+')
    logger.debug('result %s', result)


if __name__ == "__main__":
    main()
