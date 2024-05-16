import random


class BitBank:

    def __init__(self) -> None:
        '''
        [요구사항(RFP)]
        은행이름은 비트은행이다.
        입금자 이름(name), 계좌번호(account_number), 금액(money) 속성값으로 계좌를 생성한다.
        계좌번호는 3자리-2자리-6자리 형태로 랜덤하게 생성된다.
        예를들면 123-12-123456 이다.
        금액은 100 ~ 999 사이로 랜덤하게 입금된다. (단위는 만단위로 암묵적으로 판단한다)
        '''
    
        self.name:str = ""
        self.account_number:str = ""
        self.money:int = 0

    def __init__(self, name:str):
        self.name:str = name
        self.account_number:str = self.create_account_number()
        self.money:int = random.randint(100, 999)
    
    def create_account_number(self) -> str:
        return f"{"%03d".format(random.randint(0, 999))}-{"%02d".format(random.randint(0, 99))}-{"%06d".format(random.randint(0, 999999))}"