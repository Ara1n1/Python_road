import time


def fib(n):
    if n < 1:
        return -1
    if n == 1 or n == 2:
        return 1
    return fib(n - 1) + fib(n - 2)


if __name__ == '__main__':
    t1 = time.time()
    sum = fib(45)
    print("sum=", sum)
    t2 = time.time()
    print(t2, t1)
    print("use time :", t2 - t1)
