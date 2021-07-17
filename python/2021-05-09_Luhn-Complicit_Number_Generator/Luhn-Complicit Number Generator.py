def check(i):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(i)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10 == 0


x = 2221000000000000
for i in range(x):
    i = i + x + 500
    if check(i):
        print(i)