from dataclasses import dataclass
import pandas as pd

@dataclass
class TitanicModel:
    __context: str = ""
    __fname: str = ""
    __train: pd.DataFrame = None
    __test: pd.DataFrame = None
    __id: str = ""
    __label: str = ""

    @property
    def context(self) -> str:    return self.__context

    @context.setter
    def context(self, context:str): self.__context = context

    @property
    def fname(self) -> str:    return self.__fname

    @fname.setter
    def fname(self, fname:str): self.__fname = fname

    @property
    def train(self) -> pd.DataFrame:    return self.__train

    @train.setter
    def train(self, train:pd.DataFrame): self.__train = train

    @property
    def test(self) -> pd.DataFrame:    return self.__test
    
    @test.setter
    def test(self, test:pd.DataFrame): self.__test = test

    @property
    def id(self) -> str:    return self.__id

    @id.setter
    def id(self, id:str): self.__id = id

    @property
    def label(self) -> str:    return self.__label

    @label.setter
    def label(self, label:str): self.__label = label
