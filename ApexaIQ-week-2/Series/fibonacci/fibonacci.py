def fibonacci_series(n):
    fib = []
    a, b = 0, 1
    for _ in range(n):
        fib.append(a)
        a, b = b, a + b
    return fib

num_terms = 10
print(f"Fibonacci series up to {num_terms} terms:")
print(fibonacci_series(num_terms))