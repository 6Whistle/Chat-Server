import os, sys

import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from googlemaps import Client
import pandas as pd
from example.cctv_util import Reader
from context.service.data_service import DataService
from icecream import ic

class CCTVReport:
    def __init__(self) -> None:
        self.service = DataService(sname='./save/', dname='./data/', fname='cctv_in_seoul.csv')
        self.cctv = self.service.new_dframe("cctv_in_seoul.csv")
        self.crime = self.service.new_dframe("crime_in_seoul.csv")
        self.crime_rate_columes = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columes = ['살인 발생', '강도 발생', '강간 발생', '절도 발생', '폭력 발생']
        self.arrest_columes = ['살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']

        self.crime.replace(',', '', regex=True, inplace=True)
        self.crime = self.crime.astype({'살인 발생': 'int64', '강도 발생': 'int64', '강간 발생': 'int64', '절도 발생': 'int64', '폭력 발생': 'int64'})
        self.crime = self.crime.astype({'살인 검거': 'int64', '강도 검거': 'int64', '강간 검거': 'int64', '절도 검거': 'int64', '폭력 검거': 'int64'})
        
    
    def save_police_position(self) -> pd.DataFrame:
        gmaps = Reader().gmaps() 
        self.stations = pd.DataFrame(columns=['경찰서명', '위도', '경도', '구별'])
        
        self.stations['경찰서명'] = [ '서울' + str(name[:-1]) + '경찰서' for name in self.crime['관서명']]
        for i in range(len(self.stations['경찰서명'])):
            tmpMap = gmaps.geocode(self.stations['경찰서명'][i], language='ko')
            station_addrs = tmpMap[0].get('geometry')
            self.stations['위도'][i] = station_addrs['location']['lat']
            self.stations['경도'][i] = station_addrs['location']['lng']
            self.stations['구별'][i] = [gu['short_name'] for gu in tmpMap[0]['address_components'] if gu['short_name'][-1] == '구'][0]
        # self.service.save_model(stations, 'police_position.csv')

        return self.stations
    
    def save_cctv_population(self) -> None:
        self.cctv.rename(columns={self.cctv.columns[0]: '구별'}, inplace=True)
        self.population = Reader().excel(f'{self.service.model.dname}pop_in_seoul', 2, 'B, D, G, J, N')
        self.population.rename(columns={self.population.columns[0]: '구별',
                                        self.population.columns[1]: '인구수', 
                                        self.population.columns[2]: '한국인', 
                                        self.population.columns[3]: '외국인', 
                                        self.population.columns[4]: '고령자'
                                        }, inplace=True)
        self.population.dropna(inplace=True)
        self.population['외국인비율'] = self.population['외국인'] / self.population['인구수'] * 100
        self.population['고령자비율'] = self.population['고령자'] / self.population['인구수'] * 100

        self.cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], axis=1, inplace=True)
        self.cctv_per_population = pd.merge(self.cctv, self.population, on='구별')

        cur1 = np.corrcoef(self.cctv_per_population['고령자비율'], self.cctv_per_population['소계'])
        cur2 = np.corrcoef(self.cctv_per_population['외국인비율'], self.cctv_per_population['소계'])

        """
        r이 -1.0과 -0.7 사이이면, 강한 음적 선형관계,
        r이 -0.7과 -0.3 사이이면, 뚜렷한 음적 선형관계,
        r이 -0.3과 -0.1 사이이면, 약한 음적 선형관계,
        r이 -0.1과 +0.1 사이이면, 거의 무시될 수 있는 선형관계,
        r이 +0.1과 +0.3 사이이면, 약한 양적 선형관계,
        r이 +0.3과 +0.7 사이이면, 뚜렷한 양적 선형관계,
        r이 +0.7과 +1.0 사이이면, 강한 양적 선형관계
        """
        # ic(cur1, cur2)

        self.service.save_model(self.cctv_per_population, 'cctv_population.csv')
    
    def save_crime_arrest_normalization(self) -> None:
        self.crime['발생건수'] = 0
        self.crime['검거율'] = 0
        for(i, idx) in enumerate(self.crime_columes):
            self.crime['발생건수'] += self.crime[idx]
            self.crime['검거율'] = self.crime[self.arrest_columes[i]] / self.crime[idx] * 100
        
        self.stations['경찰서명'].replace('서울', '', regex=True, inplace=True)
        self.stations['경찰서명'].replace('경찰서', '서', regex=True, inplace=True)
        
        self.stations.rename(columns={'경찰서명': '관서명'}, inplace=True)
        self.stations.drop(['위도', '경도'], axis=1, inplace=True)

        self.crime = pd.merge(self.crime, self.stations, on='관서명')
        self.crime.drop(['관서명'], axis=1, inplace=True)

        self.crime_per_cctv = pd.merge(self.crime, self.cctv, on='구별')
        self.crime_per_cctv.drop(self.crime_columes + self.arrest_columes, axis=1, inplace=True)

        cur1 = np.corrcoef(self.crime_per_cctv['검거율'], self.crime_per_cctv['소계'])
        cur2 = np.corrcoef(self.crime_per_cctv['발생건수'], self.crime_per_cctv['소계'])

        ic(self.crime.head(5))
        ic(self.crime_per_cctv.head(5))
        ic(cur1, cur2)

        self.service.save_model(self.crime_per_cctv, 'crime_arrest_normalization.csv')


if __name__ == '__main__':
    cctv = CCTVReport()
    cctv.save_police_position()
    cctv.save_cctv_population()
    cctv.save_crime_arrest_normalization()
