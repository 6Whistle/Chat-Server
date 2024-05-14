from dataclasses import dataclass
import os
import numpy as np
import pandas as pd
from app.api.titanic.model.titanic_model import TitanicModel

class TitanicService:
    model = TitanicModel()

    def process(self):
        self.model.preprocess('train.csv', 'test.csv')
        # this = self.model
        # this.train = self.new_model('train.csv')
        # this.test = self.new_model('test.csv')

        # print(f'Train columns: {this.train.columns}')
        # print(f'Test columns: {this.test.columns}')
        
        # this.id = this.test['PassengerId']
        # this = self.name_nominal(this)

        # self.print_model(this)

        # # this.label = self.create_label(this)
        # # print(f'Train Label: {this.label}')        

        # this = self.drop_feature(this, 'Ticket', 'Name', 'SibSp', 'Parch', 'Cabin')

        # this = self.pclass_ordinal(this)
        # this = self.sex_nominal(this)
        # this = self.age_ratio(this)

        # self.print_model(this)
        
    def new_model(self, payload):
        this = self.model
        this.context = "./app/api/titanic/data/"
        this.fname = payload

        return pd.read_csv(this.context + this.fname)

    def print_model(self, this):
        [print(f'{i}') for i in [this.train, this.test]]

    @staticmethod
    def create_train(this: TitanicModel) -> pd.DataFrame:
        return this.train.drop("", axis=1)
    
        
    @staticmethod
    def create_label(this: TitanicModel) -> pd.DataFrame:
        return this.train['Survived']

    @staticmethod
    def drop_feature(this: TitanicModel, *feature:str):
        [i.drop([*feature], axis=1, inplace=True) for i in [this.train, this.test]]
        
        return this
    
    # ['PassengerId','Survived','Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked']

    @staticmethod
    def pclass_ordinal(this: TitanicModel) -> TitanicModel:
        this.train['Pclass'] = this.train['Pclass'].map({1: '1st', 2: '2nd', 3: '3rd'})
        this.test['Pclass'] = this.test['Pclass'].map({1: '1st', 2: '2nd', 3: '3rd'})
        return this
    
    @staticmethod
    def name_nominal(this: TitanicModel) -> TitanicModel:
        this.train['Name'] = this.train['Name'].str.extract('([A-Za-z]+)\.', expand=False)
        this.test['Name'] = this.test['Name'].str.extract('([A-Za-z]+)\.', expand=False)
        return this
    
    @staticmethod
    def sex_nominal(this: TitanicModel) -> TitanicModel:
        this.train['Sex'] = this.train['Sex'].map({'male': 'M', 'female': 'F'})
        this.test['Sex'] = this.test['Sex'].map({'male': 'M', 'female': 'F'})
        return this

    @staticmethod
    def age_ratio(this: TitanicModel) -> TitanicModel:
        for dataset in [this.train, this.test]:
            dataset['Age'] = dataset['Age'].fillna(-0.5)
            bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
            labels = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior']
            dataset['AgeGroup'] = pd.cut(dataset['Age'], bins, labels=labels)
        return this
    
    
    @staticmethod
    def embarked_nominal(this: TitanicModel) -> TitanicModel:
        this.train['Embarked'] = this.train['Embarked'].str.extract('([A-Za-z]+)\.', expand=False)
        this.test['Embarked'] = this.test['Embarked'].str.extract('([A-Za-z]+)\.', expand=False)
        return this

    @staticmethod
    def extract_title_from_name(this: TitanicModel) -> TitanicModel:
        combine = [this.train, this.test]
        for dataset in combine:
            dataset['Title'] = dataset.Name.str.extract('([A-Za-z]+)\.', expand=False)
        return this