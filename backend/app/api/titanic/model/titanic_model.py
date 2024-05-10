from dataclasses import dataclass
import pandas as pd

@dataclass
class TitanicModel:
    context: str
    fname: str
    train: pd.DataFrame
    test: pd.DataFrame
    id: str
    label: str

    @property
    def context(self) -> str:    return self.context

    @context.setter
    def context(self, context): self.context = context

    @property
    def fname(self) -> str:    return self.fname

    @fname.setter
    def fname(self, fname): self.fname = fname

    @property
    def train(self) -> pd.DataFrame:    return self.train

    @train.setter
    def train(self, train): self.train = train

    @train.getter
    def train(self) -> pd.DataFrame:    return self.train

    @property
    def test(self) -> pd.DataFrame:    return self.test
    
    @test.setter
    def test(self, test): self.test = test

    @property
    def id(self) -> str:    return self.id

    @id.setter
    def id(self, id): self.id = id

    @property
    def label(self) -> str:    return self.label

    @label.setter
    def label(self, label): self.label = label
