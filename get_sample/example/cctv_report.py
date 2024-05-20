import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from googlemaps import Client
import pandas as pd
from example.cctv_util import Reader
from context.service.data_service import DataService
from icecream import ic

class CCTVReport:
    def __init__(self):
        self.service = DataService(sname='./save/', dname='./data/', fname='cctv_in_seoul.csv')
        self.cctv = self.service.new_dframe("cctv_in_seoul.csv")
        self.crime = self.service.new_dframe("crime_in_seoul.csv")
        self.crime_rate_columes = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columes = ['살인', '강도', '강간', '절도', '폭력']
        self.arrest_columes = ['살인검거', '강도검거', '강간검거', '절도검거', '폭력검거']

        ic(self.cctv.head())
        ic(self.crime.head())
    
    def save_police_position(self):
        station_names = []
        for name in self.crime['관서명']:
            station_names.append('서울' + str(name[:-1]) + '경찰서')
        station_addrs = []
        station_lats = []
        station_lngs = []
        station_regions = []
        reader = Reader()
        gmaps = reader.gmaps()
        for name in station_names:
            tmpMap = gmaps.geocode(name, language='ko')
            station_addrs = tmpMap[0].get('geometry')
            station_lats.append(station_addrs['location']['lat'])
            station_lngs.append(station_addrs['location']['lng'])
            station_regions.append([gu['short_name'] for gu in tmpMap[0]['address_components'] if gu['short_name'][-1] == '구'][0])
        self.service.save_model(pd.DataFrame({'경찰서명': station_names, '위도': station_lats, '경도': station_lngs, '지역': station_regions}), 'temp.csv')
        return station_regions

if __name__ == '__main__':
    cctv = CCTVReport()
    cctv.save_police_position()
