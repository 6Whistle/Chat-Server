from example import utils

class Calculator:
    def __init__(self, a, opcode, b):
        print(f'utils.py / myRandom() 을 이용하여 자동 랜덤 계산기를 생성합니다')
        print('(ex) 5 + 4 = 9')
    
    def calculate(self):
        a = utils.myRandom(1, 10)
        b = utils.myRandom(1, 10)
        op = {1: '+', 2: '-', 3: '*', 4: '/'}[utils.myRandom(1, 5)]
        return f'{a} {op} {b} = {op == "+" and a+b or op == "-" and a-b or op == "*" and a*b or a/b}' 