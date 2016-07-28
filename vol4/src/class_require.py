class Car:
    # 中略
    def run(self):  # ここにはCarしかこない
        self.x += 1.0

def run(car):  # ここにはCarに関係ないものが来れる
    car.x += 1.0

def main():
    car1 = Car()
    car1.run()
    run(car1)  # car1.x == 2.0
    print(car1.x, car1.y)

if __name__ == '__main__':
    main()
