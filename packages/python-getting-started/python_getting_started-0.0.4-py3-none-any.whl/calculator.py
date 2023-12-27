import logging
from typing import List
from enum import Enum

logging.basicConfig(filename='logger.log', filemode='w', format='%(levelname)s:%(funcName)s:%(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger("calculate")
logger.setLevel(logging.DEBUG)


class Operator(Enum):
    ADDITION = '+'
    SUBTRACTION = '-'
    MULTIPLICATION = '*'


def calculate(values: List[int], operator: str) -> int:
    logger.info('started calculation for values %s, operator %s', values, operator)
    result = values[0]
    match operator:
        case Operator.ADDITION.value:
            logger.debug('started addition operation')
            for i in range(1, len(values)):
                result = result + values[i]
        case Operator.SUBTRACTION.value:
            logger.debug('started subtraction operation')
            for i in range(1, len(values)):
                result = result - values[i]
        case Operator.MULTIPLICATION.value:
            logger.debug('started multiplication operation')
            for i in range(1, len(values)):
                result = result * values[i]
        case _:
            logger.error('unsupported operator %s is passed', operator)
            raise Exception('unsupported operation')
    return result


def main():
    values = list(input('enter the values').split(","))
    values = [int(i) for i in values]
    operator = input('enter operator')
    result = calculate(values, operator)
    logger.debug('result %s', result)


if __name__ == "__main__":
    main()
