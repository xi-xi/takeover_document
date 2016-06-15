def quadratic_function(a, b, c):
    def _func(x):
        return a * x ** 2 + b * x + c
    return _func


def main():
    fx = quadratic_function(2, 1, 5)
    for x in range(10):
        print(fx(x))

if __name__ == '__main__':
    main()
