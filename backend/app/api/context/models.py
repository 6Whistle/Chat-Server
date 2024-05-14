from dataclasses import dataclass
import pandas as pd
from app.api.context.datasets import Datasets

@dataclass
class Models:
    def __init__(self):
        self.dataset = Datasets()
        this = self.dataset
        this.dname = './data/'
        this.sname = './save/'

    def __init__(self, dname:str, sname:str):
        self.dataset = Datasets()
        this = self.dataset
        this.dname = dname
        this.sname = sname

    # index_col=X: X번째 컬럼을 인덱스로 사용
    # index_col=None: 인덱스를 사용하지 않음
    def new_model(self, fname:str) -> pd.DataFrame:
        return pd.read_csv(f'{self.dataset.dname}{fname}', index_col=0)
    
    def new_dframe(self, fname:str) -> pd.DataFrame:
        return pd.read_csv(f'{self.dataset.dname}{fname}')
    
    """
        df.to_csv(f'{self.ds.sname}{fname}',sep=',',na_rep='NaN',
                         float_format='%.2f',  # 2 decimal places
                         columns=['ID', 'X2'],  # columns to write
                         index=False)  # do not write index
    """
    def save_model(self, dframe:pd.DataFrame, fname:str) -> None:
        dframe.to_csv(f'{self.dataset.sname}{fname}')
    
