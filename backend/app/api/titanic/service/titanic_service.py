from dataclasses import dataclass
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from app.api.titanic.model.titanic_model import TitanicModel

class TitanicService:
    model = TitanicModel()

    def preprocess(self) -> TitanicModel:
        self.model.preprocess('train.csv', 'test.csv')
        print(f'Preprocess Done')
        return self.model
    
    def modeling(self, model_name:str) -> object:
        return {"DT": DecisionTreeClassifier(), "RF": RandomForestClassifier(), "NB": GaussianNB(), "KNN": KNeighborsClassifier(), "SVM": SVC()}.get(model_name, DecisionTreeClassifier())

    def learning(self, model_type, model_name:str) -> float:
        print(f'{model_name} Algorithm accuracy is ')
        return self.model.learning(model_type)
    
    def postprocess(self):
        print(f'Postprocess Done')

    def submit(self):
        print(f'Submit Done')
