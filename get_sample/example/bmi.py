from example.utils import Member


class BMI():
    def __init__(self) -> None:
        '''utils.py / Members(), myRandom() 를 이용하여 BMI 지수를 구하는 계산기를 작성합니다.'''
    
    def get_bmi(self, name:str) -> float:
        self.member = Member()
        self.member.name = name
        self.member.height = Member.myRandom(150, 200)
        self.member.weight = Member.myRandom(40, 100)
        return self.member.weight / (self.member.height/100)**2
        