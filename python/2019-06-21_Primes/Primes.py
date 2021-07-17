primes = [1]

while True:
    num = 1
    for prime in primes:
        num = num * prime
    num = num + 1
    if len(str(num)) > 1000000:
        print(str(num))
        break
    primes.append(num)