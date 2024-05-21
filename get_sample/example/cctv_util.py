import json
import os
from dotenv import load_dotenv
import googlemaps
import selenium
import pandas as pd
from icecream import ic
from example.cctv_abstract import PrinterBase, ReaderBase, ScrapperBase

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

class Printer(PrinterBase):
    def print(self, msg):
        ic(msg)

    def dframe(self, this: pd.DataFrame):
        print('=' * 100)
        print(type(this))
        print(this.columns)
        print(this.head(1))
        print(this.isnull().sum())
        print('=' * 100)
        

class Reader(ReaderBase):
    def __init__(self) -> None:
        pass

    def print(self, msg):
        ic(msg)

    def csv(self, msg) -> pd.DataFrame:
        return pd.read_csv(f'{msg}.csv', encoding='utf-8', thousands=',')

    def excel(self, file, headers, usecols) -> pd.DataFrame:
        return pd.read_excel(f'{file}.xls', header=headers, usecols=usecols)

    def json(self, msg):
        return json.loads(open(f'{msg}.json', encoding='utf-8').read())
    
    def gmaps(self):
        return googlemaps.Client(key=os.environ['GOOGLEMAP_KEY'])
    

class Scrapper(ScrapperBase):
    def driver(self, msg):
        print(f'DRIVER: {msg}')