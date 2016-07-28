class Car:
    def __init__(self):
        self.x, self.y = 0.0, 0.0
    def run(self):
        self.x += 1.0  # selfのxを増加

def run(car):
    car.x += 1.0  # 与えられたcarのxを増加

def main():
    car1 = Car()
    car1.run()
    run(car1)  # car1.x == 2.0
    print(car1.x, car1.y)

if __name__ == '__main__':
    main()
