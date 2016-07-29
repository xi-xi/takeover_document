class Car:
    def __init__(self):
        self.gas = 0.0  # 燃料

    def lamp(self):
        # 燃料が少なくなったら呼びたい!
        print("燃料が少ない!")

def main():
    car = Car()
    car.gas = 10.0  # 燃料を外部から直接操作
    # 何らかの処理
    if car.gas <= 1.0:  # main関数側でチェック
        car.lamp()

if __name__ == '__main__':
    main()
