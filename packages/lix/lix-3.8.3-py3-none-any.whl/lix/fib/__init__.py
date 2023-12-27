def multiply_matrix(matrix1, matrix2):
    a = matrix1[0][0] * matrix2[0][0] + matrix1[0][1] * matrix2[1][0]
    b = matrix1[0][0] * matrix2[0][1] + matrix1[0][1] * matrix2[1][1]
    c = matrix1[1][0] * matrix2[0][0] + matrix1[1][1] * matrix2[1][0]
    d = matrix1[1][0] * matrix2[0][1] + matrix1[1][1] * matrix2[1][1]
    return [[a, b], [c, d]]


def power_matrix(matrix, n):
    if n == 0 or n == 1:
        return matrix
    half = power_matrix(matrix, n // 2)
    result = multiply_matrix(half, half)
    if n % 2 == 1:
        result = multiply_matrix(result, matrix)
    return result


def fibonacci(n):
    if n <= 1:
        return n
    matrix = [[1, 1], [1, 0]]
    result = power_matrix(matrix, n - 1)
    return result[0][0]

fib = fibonacci