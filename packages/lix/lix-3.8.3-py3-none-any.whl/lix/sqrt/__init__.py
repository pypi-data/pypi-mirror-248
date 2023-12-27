def sqrt(n):
    if n == 0:
        return 0

    x = n / 2

    while True:
        new_x = 0.5 * (x + n / x)

        if abs(new_x - x) < 1e-9:
            return new_x

        x = new_x

square_root = sqrt
squareroot = sqrt