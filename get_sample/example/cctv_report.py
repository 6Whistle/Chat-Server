import os, sys

import numpy as np
from sklearn import preprocessing
import folium

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
            self.stations['위도'][i], self.stations['경도'][i] = station_addrs['location']['lat'], station_addrs['location']['lng']
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
        
        self.police = Reader().csv(f'{self.service.model.sname}police_position')

        self.police['경찰서명'].replace('서울', '', regex=True, inplace=True)
        self.police['경찰서명'].replace('경찰서', '서', regex=True, inplace=True)
        self.police.rename(columns={'경찰서명': '관서명'}, inplace=True)
        self.police.drop(['위도', '경도'], axis=1, inplace=True)

        self.police = pd.merge(self.police, self.crime, on='관서명')
        self.police = pd.pivot_table(self.police, index='구별', aggfunc=np.sum)

        self.police['살인검거율'] = self.police['살인 검거'] / self.police['살인 발생'] * 100
        self.police['강도검거율'] = self.police['강도 검거'] / self.police['강도 발생'] * 100
        self.police['강간검거율'] = self.police['강간 검거'] / self.police['강간 발생'] * 100
        self.police['절도검거율'] = self.police['절도 검거'] / self.police['절도 발생'] * 100
        self.police['폭력검거율'] = self.police['폭력 검거'] / self.police['폭력 발생'] * 100

        for i in self.crime_rate_columes:
            self.police.loc[self.police[i] > 100, i] = 100
        
        x = self.police[self.crime_rate_columes].values
        min_max_scalar = preprocessing.MinMaxScaler()
        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        self.police_norm = pd.DataFrame(x_scaled, columns=self.crime_rate_columes, index=self.police.index)
        self.police_norm['범죄'] = np.sum(self.police[self.crime_columes], axis=1)
        self.police_norm['검거'] = np.sum(self.police[self.arrest_columes], axis=1)
        self.police_norm['검거율'] = self.police_norm['검거'] / self.police_norm['범죄'] * 100
        self.police_norm['구별'] = self.police_norm.index

        self.service.save_model(self.police_norm, 'crime_arrest.csv')

        # self.police['살인검거율'] = self.police['살인 검거'] / self.police['살인 발생'] * 100
        # self.police['강도검거율'] = self.police['강도 검거'] / self.police['강도 발생'] * 100
        # self.police['강간검거율'] = self.police['강간 검거'] / self.police['강간 발생'] * 100
        # self.police['절도검거율'] = self.police['절도 검거'] / self.police['절도 발생'] * 100
        # self.police['폭력검거율'] = self.police['폭력 검거'] / self.police['폭력 발생'] * 100

        # self.police.drop(["관서명"], axis=1, inplace=True)

        # ic(self.police.head(5))

        # x = self.police[self.crime_rate_columes].values
        # min_max_scalar = preprocessing.MinMaxScaler()

        # x_scaled = min_max_scalar.fit_transform(x.astype(float))
        # self.police_norm = pd.DataFrame(x_scaled, columns=self.crime_rate_columes, index=self.police.index)
        # self.police_norm[self.crime_columes] = self.crime[self.crime_columes]
        # self.police_norm['발생건수'] = np.sum(self.police_norm[self.crime_columes], axis=1)
        # self.police_norm['검거건수'] = np.sum(self.police_norm[self.arrest_columes], axis=1)
        # self.police_norm['검거율'] = self.police_norm['검거건수'] / self.police_norm['발생건수'] * 100
        # self.service.save_model(self.police_norm, 'crime_arrest.csv')

        """     
        피쳐 스케일링(Feature scalining)은 해당 피쳐들의 값을 일정한 수준으로 맞춰주는 것이다.
        이때 적용되는 스케일링 방법이 표준화(standardization) 와 정규화(normalization)다.
        
        1단계: 표준화(공통 척도)를 진행한다.
            표준화는 정규분포를 데이터의 평균을 0, 분산이 1인 표준정규분포로 만드는 것이다.
            x = (x - mu) / sigma
            scale = (x - np.mean(x, axis=0)) / np.std(x, axis=0)
        2단계: 이상치 발견 및 제거
        3단계: 정규화(공통 간격)를 진행한다.
            정규화에는 평균 정규화, 최소-최대 정규화, 분위수 정규화가 있다.
             * 최소최대 정규화는 모든 데이터를 최대값을 1, 최솟값을 0으로 만드는 것이다.
            도메인은 데이터의 범위이다.
            스케일은 데이터의 분포이다.
            목적은 도메인을 일치시키거나 스케일을 유사하게 만든다.     
        """

        # # self.crime['발생건수'] = self.crime.loc[:, self.crime_columes].sum(axis=1)
        # self.stations = Reader().csv(f'{self.service.model.sname}police_position')
        # self.crime['발생건수'] = self.crime[self.crime_columes].sum(axis=1)
        # self.crime['검거건수'] = self.crime[self.arrest_columes].sum(axis=1)
        # self.crime['검거율'] = self.crime['검거건수'] / self.crime['발생건수'] * 100

        # self.stations['경찰서명'].replace('서울', '', regex=True, inplace=True)
        # self.stations['경찰서명'].replace('경찰서', '서', regex=True, inplace=True)
        
        # self.stations.rename(columns={'경찰서명': '관서명'}, inplace=True)
        # self.stations.drop(['위도', '경도'], axis=1, inplace=True)

        # self.crime = pd.merge(self.crime, self.stations, on='관서명')
        # self.crime.drop(['관서명'], axis=1, inplace=True)

        # self.crime_per_cctv = pd.merge(self.crime, self.cctv, on='구별')
        # self.crime_per_cctv.drop(self.crime_columes + self.arrest_columes, axis=1, inplace=True)

        # cur1 = np.corrcoef(self.crime_per_cctv['검거율'], self.crime_per_cctv['소계'])
        # cur2 = np.corrcoef(self.crime_per_cctv['발생건수'], self.crime_per_cctv['소계'])
        # cur3 = np.corrcoef(self.crime_per_cctv['검거건수'], self.crime_per_cctv['소계'])

        # ic(self.crime.head(5))
        # ic(self.crime_per_cctv.head(5))
        # ic(cur1, cur2, cur3)

        # self.service.save_model(self.crime_per_cctv, 'crime_arrest_normalization.csv')

    def follum_test(self):
        state_kor = Reader().json(self.service.model.dname + 'kr-states')
        m = folium.Map(location=[37.5502, 126.982], zoom_start=12)

        folium.Marker(
            location=[45.3288, -121.6625],
            tooltip="Click me!",
            popup="Mt. Hood Meadows",
            icon=folium.Icon(icon="cloud"),
        ).add_to(m)

        folium.Marker(
            location=[45.3311, -121.7113],
            tooltip="Click me!",
            popup="Timberline Lodge",
            icon=folium.Icon(color="green"),
        ).add_to(m)

        m.save(f'{self.service.model.sname}test.html')

    def draw_crime_map(self):
        reader = Reader()
        state_geo = reader.json(self.service.model.dname + 'kr-states')
    
        ic(state_geo)

        self.police = Reader().csv(f'{self.service.model.sname}crime_arrest')
        self.stations = Reader().csv(f'{self.service.model.sname}police_position')
        self.map_infos = pd.merge(self.stations, self.police, on='구별')

        ic(self.map_infos.head(5))

        m = folium.Map(location=[37.5502, 126.982], zoom_start=12)

        folium.Choropleth(
            geo_data=state_geo,
            name="choropleth",
            data=tuple(zip(self.map_infos['구별'], self.map_infos['범죄'])),
            columns=["State", "Crime Rate"],
            key_on="feature.id",
            fill_color="PuRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Crime Rate (%)",
            reset=True
        ).add_to(m)

        for i in self.map_infos.index:
            folium.CircleMarker([self.map_infos['위도'][i], self.map_infos['경도'][i]],
                radius=(self.map_infos['검거율'][i] / 30) ** 4,
                fill_color='#0a0a32').add_to(m)

        folium.LayerControl().add_to(m)
        m.save(f'{self.service.model.sname}kr_states.html')

if __name__ == '__main__':
    cctv = CCTVReport()
    # cctv.save_police_position()
    cctv.save_cctv_population()
    cctv.save_crime_arrest_normalization()
    # cctv.follum_test()
    cctv.draw_crime_map()

