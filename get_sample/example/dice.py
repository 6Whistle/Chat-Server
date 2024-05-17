from example import utils

class Dice:

    def __init__(self, sides=6):
        print(f'utils.py myRandom() 를 이용하여 주사위 객체를 생성합니다')
    
    def roll(self):
        return utils.myRandom(1, 7)