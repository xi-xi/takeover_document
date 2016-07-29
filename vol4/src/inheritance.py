class Car:
    def __init__(self):
        self.gas = 0.0  # prublic
class SunRoof(Car):
    def __init__(self):
        self.__roof_opend = False  # private
    def open_roof(self):  # public
        self.__roof_opend = True
def main():
    car = SunRoof()  # carはgasとopen_roofを持つ
    car.gas = 10.0  # ガスを注入
    car.open_roof()  # 屋根を開く!

if __name__ == '__main__':
    main()
