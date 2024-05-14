from dataclasses import dataclass
import numpy as np
import pandas as pd
from icecream import ic

from app.api.context.models import Models
from app.api.context.datasets import Datasets

class TitanicModel:
    model = Models('./app/api/titanic/data/', './app/api/titanic/save/')
    dataset = Datasets()
    
    def preprocess(self, train_fname, test_fname) -> Datasets:
        that = self.model
        this = self.dataset

        that.dataset.train = that.new_model(train_fname)
        that.dataset.test = that.new_model(test_fname)

        this.train = that.new_dframe(train_fname)
        this.test = that.new_dframe(test_fname)

        this.id = this.test['PassengerId']
        this.label = this.train['Survived']

        self.extract_title_from_name(that.dataset)
        self.remove_duplicate_title(that.dataset)

        that.dataset = self.title_nominal(that.dataset)
        that.dataset = self.age_ratio(that.dataset)
        that.dataset = self.fare_ratio(that.dataset)
        that.dataset = self.embarked_nominal(that.dataset)
        that.dataset = self.sex_nominal(that.dataset)

        that.dataset = self.drop_feature(that.dataset, 'Name', 'Age', 'Fare', 'SibSp', 'Parch', 'Ticket', 'Cabin')

        ic(that.dataset.train)
        ic(that.dataset.test)

        return this

    @staticmethod
    def extract_title_from_name(this:Datasets) -> Datasets:
        for i in [this.train, this.test]:
            i['Title'] = i['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
        return this
    
    @staticmethod
    def remove_duplicate_title(this:Datasets) -> Datasets:
        titles = [list(set(i['Title'])) for i in [this.train, this.test]]
        return titles[0] + titles[1]

    '''
        ['Mr', 'Sir', 'Major', 'Don', 'Rev', 'Countess', 'Lady', 'Jonkheer', 'Dr',
        'Miss', 'Col', 'Ms', 'Dona', 'Mlle', 'Mme', 'Mrs', 'Master', 'Capt']
        Royal : ['Countess', 'Lady', 'Sir']
        Rare : ['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme' ]
        Mr : ['Mlle']
        Ms : ['Miss']
        Master
        Mrs
    '''
    @staticmethod
    def title_nominal(this:Datasets, title_mapping:list = None) -> Datasets:
        for i in [this.train, this.test]:
            i['Title'] = i['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            i['Title'] = i['Title'].replace(['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme'], 'Rare')
            i['Title'] = i['Title'].replace(['Mlle'], 'Mr')
            i['Title'] = i['Title'].replace(['Miss'], 'Ms')
            # Master 는 변화없음
            # Mrs 는 변화없음
            i['Title'] = i['Title'].fillna(0)
            # i['Title'] = i['Title'].map(title_mapping)
        return this
    
    @staticmethod
    def age_ratio(this:Datasets) -> Datasets:
        this.train['Age'] = this.train['Age'].fillna(-0.5)
        this.test['Age'] = this.test['Age'].fillna(-0.5)
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        labels = [0, 1, 2, 3, 4, 5, 6, 7]
        for i in [this.train, this.test]:
            i['AgeGroup'] = pd.cut(i['Age'], bins, labels=labels)
        return this
    
    @staticmethod
    def fare_ratio(this:Datasets) -> Datasets:
        this.train['Fare'] = this.train['Fare'].fillna(-0.5)
        this.test['Fare'] = this.test['Fare'].fillna(-0.5)
        bins = [-1, 0, 8, 15, 31, np.inf]
        labels = [0, 1, 2, 3, 4]
        for i in [this.train, this.test]:
            i['FareGroup'] = pd.cut(i['Fare'], bins, labels=labels)
        return this
    
    @staticmethod
    def embarked_nominal(this:Datasets) -> Datasets:
        for i in [this.train, this.test]:
            i['Embarked'] = i['Embarked'].fillna('X')
        return this
    
    @staticmethod
    def sex_nominal(this:Datasets) -> Datasets:
        for i in [this.train, this.test]:
            i['Sex'] = i['Sex'].map({'male':'M', 'female':'F'})
        return this
    
    @staticmethod
    def drop_feature(this:Datasets, *features) -> Datasets:
        [i.drop([*features], axis=1, inplace=True) for i in [this.train, this.test]]
        return this