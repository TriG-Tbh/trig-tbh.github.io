def happy(num):
    sequence = []
    testing = True
    number = num
    val = 0
    while testing:
        val = 0
        digits = list(str(number))
        for digit in digits:
            val = val + int(int(digit) ** 2)
        if val == 1:
            return True
        if val not in sequence:
            sequence.append(val)
        else:
            return False
        number = val

for i in range(8):
    go = False
    while not go:
        happy = happy(i)
        if happy:
            print(i)
        else:
            i = i + 1
        go = happy