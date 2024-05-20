from dataclasses import dataclass
import pandas as pd

@dataclass
class Datasets:
    __fname: str = ""
    __dname: str = ""
    __sname: str = ""
    __train: pd.DataFrame = None
    __test: pd.DataFrame = None
    __id: pd.DataFrame = None
    __label: pd.DataFrame = None

    @property
    def fname(self) -> str:    return self.__fname

    @fname.setter
    def fname(self, fname:str): self.__fname = fname

    @property
    def dname(self) -> str:    return self.__dname

    @dname.setter
    def dname(self, dname:str): self.__dname = dname

    @property
    def sname(self) -> str:    return self.__sname

    @sname.setter
    def sname(self, sname:str): self.__sname = sname

    @property
    def train(self) -> pd.DataFrame:    return self.__train

    @train.setter
    def train(self, train:pd.DataFrame): self.__train = train

    @property
    def test(self) -> pd.DataFrame:    return self.__test
    
    @test.setter
    def test(self, test:pd.DataFrame): self.__test = test

    @property
    def id(self) -> pd.DataFrame:    return self.__id

    @id.setter
    def id(self, id:pd.DataFrame): self.__id = id

    @property
    def label(self) -> pd.DataFrame:    return self.__label

    @label.setter
    def label(self, label:pd.DataFrame): self.__label = label
