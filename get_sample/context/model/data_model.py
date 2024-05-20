from dataclasses import dataclass

import pandas as pd


@dataclass
class DataModel:
    _dname : str = ""
    _fname : str = ""
    _sname : str = ""

    # NLTK
    _result : str = ""
    _nouns : list = None
    _stopwords : list = None
    _morpheme :list = None

    # Dataframe
    _dataframe : pd.DataFrame = None
    
    @property
    def dname(self) -> str:
        return self._dname
    
    @dname.setter
    def dname(self, dname: str):
        self._dname = dname
    
    @property
    def fname(self) -> str:
        return self._fname
    
    @fname.setter
    def fname(self, fname: str):
        self._fname = fname
    
    @property
    def sname(self) -> str:
        return self._sname
    
    @sname.setter
    def sname(self, sname: str):
        self._sname = sname

    @property
    def result(self) -> str:
        return self._result
    
    @result.setter
    def result(self, result: str):
        self._result = result

    @property
    def nouns(self) -> list:
        return self._nouns
    
    @nouns.setter
    def nouns(self, nouns: list):
        self._nouns = nouns

    @property
    def stopwords(self) -> list:
        return self._stopwords
    
    @stopwords.setter
    def stopwords(self, stopwords: list):
        self._stopwords = stopwords

    @property
    def morpheme(self) -> list:
        return self._morpheme
    
    @morpheme.setter
    def morpheme(self, morpheme: list):
        self._morpheme = morpheme

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe
    
    @dataframe.setter
    def dataframe(self, dataframe: pd.DataFrame):
        self._dataframe = dataframe