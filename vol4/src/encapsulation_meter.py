class Car:
    def __init__(self, gas):
        self.__gas = gas  # 燃料
    def set_gas(self, value):
        self.__gas = value
        if value <= 0.1:
            self.lamp()
    def lamp(self):
        print("燃料が少ない!")
def main():
    car = Car(10.0)  # ガスを渡して初期化
    # 何らかの処理
    car.set_gas(0.05)
    # 何らかの処理

if __name__ == '__main__':
    main()
