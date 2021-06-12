n = 8
t = 0
for i in range(2 * n):
    if (i // n) % 2 == 0:
        t = i % n
        print(t)
    else:
        t = n - 1 - (i % n)
        print(t)