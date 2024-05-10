import pandas as pd
from app.api.titanic.model.titanic_model import TitanicModel


class TitanicService:
    model = TitanicModel()

    def new_model(self, payload) -> object:
        this = self.model
        this.context = '../data/'
        this.train = pd.read_csv(this.context + 'train.csv')
        this.test = pd.read_csv(this.context + 'test.csv')
        this.fname = payload
        return this