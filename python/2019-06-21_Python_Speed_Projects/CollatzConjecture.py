def conjecture(n):
    if n <= 1:
        raise UserWarning("Passed number cannot be less than or equal to one")
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n / 2
        elif n % 2 == 1:
            n = (n * 3) + 1
        steps += 1
    print(str(steps))

conjecture(int(input("Number: ")))