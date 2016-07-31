class QuadraticFunction:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c
    def __call__(self, x):
        return self.a*x**2 + self.b*x + self.c
    def __str__(self):
        return "{}x^2+{}x+{}".format(
            self.a, self.b, self.c)
def main():
    fx = QuadraticFunction(1, 2, 1) #call __init__
    print(str(fx)) #call __str__
    for x in range(10):
        print(fx(x)) #call __call__
