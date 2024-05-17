from example import utils

class RPS:

    def __init__(self) -> None:
        print(f'utils.py myRandom() 를 이용하여 가위바위보 객체를 생성합니다')
    
    def play(self):
        return {1: '가위', 2: '바위', 3: '보'}[utils.myRandom(1, 4)]