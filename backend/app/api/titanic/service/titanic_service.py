from dataclasses import dataclass
import os
import pandas as pd
from app.api.titanic.model.titanic_model import TitanicModel

class TitanicService:
    model = TitanicModel()

    def process(self):
        this = self.model
        this.train = self.new_model('train.csv')
        this.test = self.new_model('test.csv')

        print(f'Train columns: {this.train.columns}')
        print(f'Test columns: {this.test.columns}')
        
        this.id = this.test['PassengerId']
        print(f'Train id: {this.id}')

        this.label = self.create_label(this)
        print(f'Train Label: {this.label}')        

        this = self.drop_feature(this, 'Ticket', 'Name', 'SibSp', 'Parch', 'Cabin')
        print(f'Train columns: {this.train}')

        
    def new_model(self, payload):
        this = self.model
        this.context = "./app/api/titanic/data/"
        this.fname = payload

        return pd.read_csv(this.context + this.fname)
    
    @staticmethod
    def create_train(this: TitanicModel) -> pd.DataFrame:
        return this.train.drop("", axis=1)
    
        
    @staticmethod
    def create_label(this: TitanicModel) -> pd.DataFrame:
        return this.train['Survived']

    @staticmethod
    def drop_feature(this: TitanicModel, *feature:str):
        # for i in feature:
        #     this.train = this.train.drop([i], axis=1)
        #     this.test = this.test.drop(i, axis=1)

        # this.train = this.train.drop([*feature], axis=1)
        # this.test = this.test.drop([*feature], axis=1)
        # return this
          
        # for i in [this.train, this.test]:
        #     i.drop([*feature], axis=1, inplace=True)

        [i.drop([*feature], axis=1, inplace=True) for i in [this.train, this.test]]
        [print(f'{i.info()}') for i in [this.train, this.test]]
        
        return this