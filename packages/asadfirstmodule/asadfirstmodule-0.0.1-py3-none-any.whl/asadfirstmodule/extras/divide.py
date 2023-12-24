def divide(a, b):
    """
    Divide two numbers.

    Parameters:
    - a (float or int): The numerator.
    - b (float or int): The denominator (should not be zero).

    Returns:
    float: The result of the division in decimal format.
    """
    if b == 0:
        raise ValueError("Division by zero is undefined.")
    
    result = a / b
    return result

# Example usage:
# numerator = 10
# denominator = 2
# result = divide(numerator, denominator)
# print(f"The result of {numerator} divided by {denominator} is: {result}")
