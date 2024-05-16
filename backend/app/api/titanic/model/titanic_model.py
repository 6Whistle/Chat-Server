from dataclasses import dataclass
import numpy as np
import pandas as pd
from icecream import ic
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, cross_val_score

from app.api.context.models import Models
from app.api.context.datasets import Datasets

class TitanicModel:
    model = Models('./app/api/titanic/data/', './app/api/titanic/save/')
    dataset = Datasets()
    
    def preprocess(self, train_fname, test_fname) -> Datasets:
        that = self.model
        this = self.dataset

        this.train = that.new_model(train_fname)
        this.test = that.new_model(test_fname)

        that.dataset.train = that.new_dframe(train_fname)
        that.dataset.test = that.new_dframe(test_fname)

        this.id = that.dataset.test['PassengerId']
        this.label = that.dataset.train['Survived']

        self.extract_title_from_name(this)

        this = self.title_nominal(this)
        this = self.age_ratio(this)
        this = self.fare_ratio(this)
        this = self.embarked_nominal(this)
        this = self.sex_nominal(this)

        this = self.drop_feature(this, 'Name', 'Age', 'Fare', 'SibSp', 'Parch', 'Ticket', 'Cabin', 'Sex')
        this.train = this.train.drop(['Survived'], axis=1)

        # self.df_info(this)

        # ic(this.train)
        # ic(this.test)

        return this

    def df_info(self, this:Datasets) -> None:
        ic('='*50)
        ic(type(this.train))
        ic(this.train.columns)
        ic(this.train.head())
        ic(this.train.isnull().sum())
        ic(this.train.isin([0, 1, 2, 3, 4, 5, 6, 7, 8]).sum() == this.train.count())
        ic(type(this.test))
        ic(this.test.columns)
        ic(this.test.head())
        ic(this.test.isnull().sum())
        ic(this.test.isin([0, 1, 2, 3, 4, 5, 6, 7, 8]).sum() == this.test.count())
        ic('='*50)

    @staticmethod
    def extract_title_from_name(this:Datasets) -> Datasets:
        for i in [this.train, this.test]:
            i['Title'] = i['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
        return this

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
    def title_nominal(this:Datasets) -> Datasets:
        for i in [this.train, this.test]:
            i['Title'] = i['Title'].replace(['Countess', 'Lady', 'Sir'], 1) # Royal
            i['Title'] = i['Title'].replace(['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme'], 2) # Rare
            i['Title'] = i['Title'].replace(['Mlle', 'Mr', 'Mrs'], 3) # Mr
            i['Title'] = i['Title'].replace(['Miss', 'Ms'], 4) # Ms
            i['Title'] = i['Title'].replace(['Master'], 5)
            i['Title'] = i['Title'].fillna(0)
        return this
    
    @staticmethod
    def age_ratio(this:Datasets) -> Datasets:
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        labels = [0, 1, 2, 3, 4, 5, 6, 7]
        for i in [this.train, this.test]:
            i['AgeGroup'] = pd.cut(i['Age'].fillna(-0.5), bins, labels=labels)
        return this
    
    @staticmethod
    def fare_ratio(this:Datasets) -> Datasets:
        bins = [-1, 0, 8, 15, 31, np.inf]
        labels = [0, 1, 2, 3, 4]
        for i in [this.train, this.test]:
            i['FareGroup'] = pd.cut(i['Fare'].fillna(-0.5), bins, labels=labels)
        return this
    
    @staticmethod
    def embarked_nominal(this:Datasets) -> Datasets:
        for i in [this.train, this.test]:
            i['Embarked'] = i['Embarked'].fillna('X').map({'X':0, 'S':1, 'Q':2, 'C':3})
        return this
    
    @staticmethod
    def sex_nominal(this:Datasets) -> Datasets:
        for i in [this.train, this.test]:
            i['Gender'] = i['Sex'].map({'male':0, 'female':1})
        return this
    
    @staticmethod
    def drop_feature(this:Datasets, *features:str) -> Datasets:
        [i.drop([*features], axis=1, inplace=True) for i in [this.train, this.test]]
        return this
    
    @staticmethod
    def create_k_fold():
        return KFold(n_splits=10, shuffle=True, random_state=0)

    def get_accuracy(self, this:Datasets, model_type:object, k_fold:KFold) -> float:
        score = cross_val_score(model_type, this.train, this.label, cv=k_fold, n_jobs=1, scoring='accuracy')
        return round(np.mean(score)*100, 2)
    
    def learning(self, model_type:object) -> Models:
        k_fold = self.create_k_fold()
        accuarcy = self.get_accuracy(self.dataset, model_type, k_fold)
        ic(accuarcy)
        return accuarcy