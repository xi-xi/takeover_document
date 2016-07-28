class Car:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0


def main():
    car1 = Car()
    car2 = Car()
    car1.x, car1.y = 1.0, 1.0
    car2.x, car2.y = 5.0, 5.0
    print(car1)
    print(car2)


if __name__ == '__main__':
    main()
