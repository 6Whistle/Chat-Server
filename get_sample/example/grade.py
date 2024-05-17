from example.utils import myRandom


class Grade:

    def __init__(self) -> None:
        # 아래 주석된 부분을 완성합니다.
        kor = myRandom(0,100)
        eng = myRandom(0, 100)
        math = myRandom(0, 100)
        sum = self.sum(kor, eng, math)
        avg = self.avg(kor, eng, math)
        grade = self.getGrade(avg)
        passChk = self.passChk(avg)
        return [sum, avg, grade, passChk] 

    def sum(self, kor, eng, math) -> int:
        return kor + eng + math
    
    def avg(self, kor, eng, math) -> float:
        return (kor + eng + math) / 3
    
    def getGrade(self, avg) -> str:
        if avg >= 90: return 'A'
        elif avg >= 80: return 'B'
        elif avg >= 70: return 'C'
        elif avg >= 60: return 'D'
        else: return 'F'
    
    def passChk(self, avg) -> bool:
        return avg >= 70