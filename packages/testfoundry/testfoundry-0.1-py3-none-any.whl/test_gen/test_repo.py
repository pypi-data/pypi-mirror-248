def multiply(a, b):
    """Multiplies two numbers."""
    return a * b

def power(a, b):
    """Raises a to the power of b."""
    return a ** b

def concatenate(a, b):
    """Concatenates two strings."""
    return a + b

def divide(a, b):
    """Divides a by b. Raises ZeroDivisionError if b is zero."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b

def greet(name):
    """Returns a greeting for the given name."""
    return f"Hello, {name}!"

def factorial(n):
    """Returns the factorial of n."""
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def fibonacci(n):
    """Returns the nth Fibonacci number."""
    if n <= 0:
        raise ValueError("Input must be a positive integer.")
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)