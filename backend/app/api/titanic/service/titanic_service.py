from dataclasses import dataclass
import os
import numpy as np
import pandas as pd
from app.api.titanic.model.titanic_model import TitanicModel

class TitanicService:
    model = TitanicModel()

    def preprocess(self) -> TitanicModel:
        self.model.preprocess('train.csv', 'test.csv')
        print(f'Preprocess Done')
        return self.model
    
    def modeling(self):
        print(f'Modeling Done')

    def learning(self):
        print(f'DescisionTree Algorithm accuracy is ')
        print(f'RandomForest Algorithm accuracy is ')
        print(f'NavieBayes Algorithm accuracy is ')
        print(f'KNN Algorithm accuracy is ')
        print(f'SVM Algorithm accuracy is ')
        print(f'Learning Done')
    
    def postprocess(self):
        print(f'Postprocess Done')

    def submit(self):
        print(f'Submit Done')
