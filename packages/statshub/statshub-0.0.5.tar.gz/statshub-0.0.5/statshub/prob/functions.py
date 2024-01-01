def factorial(n):
    """
    Calculate the factorial of a non-negative integer.

    Args:
    - n (int): Non-negative integer for which factorial is calculated.

    Returns:
    - int: Factorial of the given integer 'n'.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer.")

    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def permutations(n):
    """
    Calculate the number of permutations of 'n' items.

    Args:
    - n (int): Number of items for permutations.

    Returns:
    - int: Number of permutations of 'n' items.
    """
    return factorial(n)


def variations(n, p, repetition=False):
    """
    Calculate the number of variations of 'n' items taken 'p' at a time.

    Args:
    - n (int): Total number of items.
    - p (int): Number of items taken at a time.
    - repetition (bool, optional): Whether repetition is allowed. Default is False.

    Returns:
    - int: Number of variations of 'n' items taken 'p' at a time.
    """
    if not all(isinstance(x, int) for x in [n, p]) or any(x < 0 for x in [n, p]):
        raise ValueError("Inputs must be non-negative integers.")

    if not repetition:
        return factorial(n) // factorial(n - p)
    else:
        return n ** p


def combinations(n, p, repetition=False):
    """
    Calculate the number of combinations of 'n' items taken 'p' at a time.

    Args:
    - n (int): Total number of items.
    - p (int): Number of items taken at a time.
    - repetition (bool, optional): Whether repetition is allowed. Default is False.

    Returns:
    - int: Number of combinations of 'n' items taken 'p' at a time.
    """
    if not all(isinstance(x, int) for x in [n, p]) or any(x < 0 for x in [n, p]):
        raise ValueError("Inputs must be non-negative integers.")

    if not repetition:
        return factorial(n) // (factorial(n - p) * factorial(p))
    else:
        return factorial(n + p - 1) // (factorial(n - 1) * factorial(p))
