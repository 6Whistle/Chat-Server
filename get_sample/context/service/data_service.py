import re
from matplotlib import pyplot as plt
import pandas as pd
import nltk
from nltk import FreqDist
from konlpy.tag import Okt
from wordcloud import WordCloud
from context.model.data_model import DataModel


class DataService:    
    def __init__(self) -> None:
        self.model : DataModel = DataModel()
        self.okt : Okt = Okt()
        self.model.dname = './data/'
        self.model.fname = 'samsung.csv'
        self.model.sname = './save/'
        self.model.nouns = []
        self.model.stopwords = []
        self.model.morpheme = []

    def __init__(self, fname:str) -> None:
        self.model : DataModel = DataModel()
        self.okt : Okt = Okt()
        self.model.dname = './data/'
        self.model.fname = fname
        self.model.sname = './save/'
        self.model.nouns = []
        self.model.stopwords = []
        self.model.morpheme = []

    
    def __init__(self, dname:str, sname:str, fname:str) -> None:
        self.model : DataModel = DataModel()
        self.okt : Okt = Okt()
        self.model.dname = dname
        self.model.fname = fname
        self.model.sname = sname
        self.model.nouns = []
        self.model.stopwords = []
        self.model.morpheme = []

    def read_file(self, fname:str) -> str:
        self.model.result = open(f'{self.model.dname}{fname}', 'r', encoding='utf-8').read()
        return self.model.result

    def new_dframe(self, fname:str) -> pd.DataFrame:
        return pd.read_csv(f'{self.model.dname}{fname}')
    
    def save_model(self, dframe:pd.DataFrame, fname:str) -> None:
        dframe.to_csv(f'{self.model.sname}{fname}', index=False, encoding='utf-8')

    def preprocessing(self, phrase:str, fname:str) -> None:
        self.read_file(fname)
        self.okt.pos(phrase=phrase, stem=True)
        self.model.result = self.model.result.replace('\n', ' ')
        tokenizer = re.compile(r'[^ㄱ-힣]+')
        self.model.result = tokenizer.sub(' ', self.model.result)
    
    def noun_embedding(self) -> None:
        tokens = nltk.word_tokenize(self.model.result)
        for token in tokens:
            pos = self.okt.pos(token)
            _ = [j[0] for j in pos if j[1] == 'Noun']
            if len(''.join(_)) > 1:
                self.model.nouns.append(''.join(_))
    
    def stopword_emmbedding(self, phrase:str, fname:str) -> None:
        self.okt.pos(phrase=phrase, stem=True)
        with open(f'{self.model.dname}{fname}', 'r', encoding='utf-8') as f:
            self.model.stopwords = f.read()
        self.model.stopwords = self.model.stopwords.split(" ")
    
    def morpheme_embedding(self) -> None:
        self.model.morpheme = [word for word in self.model.nouns if word not in self.model.stopwords]
    
    def draw_wordcloud(self, fname) -> None:
        freqtext = pd.Series(dict(FreqDist(self.model.morpheme))).sort_values(ascending=False)
        wcloud = WordCloud(font_path=f'{self.model.dname}{fname}', relative_scaling=0.2, background_color='white').generate_from_frequencies(freqtext)
        plt.figure(figsize=(12, 12))
        plt.imshow(wcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()