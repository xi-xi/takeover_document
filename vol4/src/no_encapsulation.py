class Car:
    def __init__(self):
        self.gas = 0.0  # 燃料

def main():
    car = Car()
    car.gas = 10.0  # 燃料を外部から直接操作

if __name__ == '__main__':
    main()
