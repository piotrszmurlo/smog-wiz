import requests
import time
import csv
from datetime import datetime
import asyncio

current_date = datetime.now()
date_str = current_date.strftime("%Y-%m-%d %H:%M:%S")
date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
# print(date_str, date_obj)


class API(object):

    @staticmethod
    async def get_stations() -> list:
        try:
            with open('get_stations.csv', newline='') as file:
                reader = csv.reader(file)
                date = next(reader)[0]
                data = next(reader)
                date_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                time_diff = (current_date - date_object).total_seconds()//60
                print(data)
            if time_diff >=10:
                response = requests.get('http://api.gios.gov.pl/pjp-api/rest/station/findAll').json()
                with open('get_stations.csv', 'w', newline ='') as file:
                    writer = csv.writer(file)
                    writer.writerow([date_str])
                    writer.writerow(response)
                    #print(response)
                return response
            else:
                return data


        except Exception as e:
            time.sleep(1)
            print(e)
            print(f'...fetch retry...')
            return await API.get_stations()
    
    @staticmethod
    async def get_measuring_stands_for_station(station_id:int) -> list:
        try:
            return requests.get(f'http://api.gios.gov.pl/pjp-api/rest/station/sensors/{station_id}').json()
        except Exception as e:
            time.sleep(1)
            print(e)
            print(f'...fetch retry...')
            return await API.get_measuring_stands_for_station(station_id)

    @staticmethod
    async def get_measuring_stand_data(stand_id:int) -> list:
        try:
            return requests.get(f"http://api.gios.gov.pl/pjp-api/rest/data/getData/{stand_id}").json()
        except Exception as e:
            time.sleep(1)
            print(e)
            print(f'...fetch retry...')
            return await API.get_measuring_stand_data(stand_id)

asyncio.run(API.get_stations())