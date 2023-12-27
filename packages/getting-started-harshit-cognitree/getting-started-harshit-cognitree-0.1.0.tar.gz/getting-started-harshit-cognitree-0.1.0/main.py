import logging

logger = logging.getLogger("Calculator_logger")


def addition(a, b):
    logger.warning("Performing addition operation for operands: " + str(a) + " and " + str(b))
    return a + b


def subtract(a, b):
    logger.warning("Performing subtraction operation for operands: " + str(a) + " and " + str(b))
    return a - b


def multiply(a, b):
    logger.warning("Performing multiplication operation for operands: " + str(a) + " and " + str(b))
    return a * b


def divide(a, b):
    logger.warning("Performing division operation for operands: " + str(a) + " and " + str(b))
    return a // b


def calculate(operation, a, b):
    if operation == "addition":
        return addition(a, b)
    elif operation == "subtract":
        return subtract(a, b)
    elif operation == "multiply":
        return multiply(a, b)
    elif operation == "divide":
        return divide(a, b)
    else:
        print("Unsupported operation: " + operation)


if __name__ == '__main__':
    print(calculate("addition", int(3), int(4)))
