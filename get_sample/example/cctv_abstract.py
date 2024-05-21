from abc import *

import pandas as pd

class PrinterBase(metaclass=ABCMeta):
    @abstractmethod
    def print(self, msg):
        pass

class ReaderBase(PrinterBase):
    @abstractmethod
    def csv(self, msg):
        pass

    @abstractmethod    
    def excel(self, file) -> pd.DataFrame:
        pass

    @abstractmethod
    def json(self, file) -> pd.DataFrame:
        pass

    @abstractmethod
    def gmaps(self):
        pass

class ScrapperBase(PrinterBase):
    @abstractmethod
    def driver(self, msg):
        pass
