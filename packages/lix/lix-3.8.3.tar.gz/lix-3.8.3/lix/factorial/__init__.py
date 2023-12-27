import math

cache = {}

def factorial(n):
    if n in cache:
        return cache[n]

    if n == 0:
        result = 1
    else:
        result = math.factorial(n)

    cache[n] = result

    return result