import os
from api import API
from pprint import pprint
import matplotlib.pyplot as plt
from datetime import datetime
import time
import asyncio
from db_controller import Database

clear = lambda: os.system('clear')

async def get_stations_names_list() -> None:
    station_list = await API.get_stations()
    print([station['stationName'] for station in station_list])

async def get_stations_ids_list() -> list:
    station_list = await API.get_stations()
    return [station['id'] for station in station_list]


async def get_measuring_stands_list_for_station(station_id:int):
    stands_list = await API.get_measuring_stands_for_station(station_id)
    info = [stand['param']['paramName'] + " -> id: " + f"{stand['id']}" for stand in stands_list]
    print(info)


async def get_all_stand_data() -> dict:
    station_ids_list = await get_stations_ids_list()
    clear()
    data = {}
    stations_num = len(station_ids_list)

    for i, id in list((enumerate(station_ids_list))):
        percent = round(i/stations_num*100,2)
        percent = '0'+str(percent) if percent<10 else percent
        print('========= Loading data =========')
        print(f'============ {percent}% ============')
        print(f'{id} station data...')
        stand_data = await get_all_stand_data_for_station(id)
        data[id] = stand_data
        clear()
    return data


async def get_all_stand_data_for_station(station_id:int) -> list:
    stands_list = await API.get_measuring_stands_for_station(station_id)
    stand_id_list = [stand['id'] for stand in stands_list]
    data_for_stand = []
    for id in stand_id_list:
        print(f'---- {id} stand data...')
        element = await API.get_measuring_stand_data(id)
        data_for_stand.append(element)
    # pprint(data_for_stand)
    return data_for_stand

async def get_specific_stand_data(*args:int) -> None:
    data_for_stand = [await API.get_measuring_stand_data(id) for id in args]
    return data_for_stand


async def get_all_measuring_stands_list() -> None:
    station_list = await API.get_stations()
    result = []
    print('loading data...')
    specific_stand_id_list =[]
    for station in station_list:
        measuring_stands = await API.get_measuring_stands_for_station(station['id'])
        stands_list = [ (stand["id"], stand['param']['paramName'], stand['param']['paramCode']) for stand in measuring_stands]
        info = f'{[station["id"]]}{ station["stationName"]}: { ", ".join([f"[{stand[0]}]{stand[1]}({stand[2]})" for stand in stands_list]) }'
        result.append(info)
        for stand in stands_list:
            specific_stand_id_list.append((stand[2], stand[0]))
    # for info in result:
    #     print(info)
    return specific_stand_id_list


async def show_station_data_chart(station_id:int) -> None:
    stand_data = await get_all_stand_data_for_station(station_id)
    for stand in stand_data:
        values = []
        dates = []
        for element in stand['values']:
            date_str = element['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            values.append(element['value'])
            dates.append(date_obj)

        data = {'dates': dates, 'values': values}
        plt.plot('dates', 'values', data=data, label=stand['key'])

    plt.xlabel('Czas')
    plt.ylabel('Wartość wskaźnika')
    plt.legend()
    plt.show()

async def show_all_station_data_chart_for_param(param:str):
    specific_stand_id_list = await get_all_measuring_stands_list()
    data = []
    for stand_id in specific_stand_id_list:
        if stand_id[0] == param:
            stand_data = await API.get_measuring_stand_data(stand_id[1])
            data.append(stand_data)
    for stand_data in data:
        values = []
        dates = []
        for element in stand_data['values']:
            date_str = element['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            values.append(element['value'])
            dates.append(date_obj)
        data_dict ={'dates': dates, 'values': values}
        plt.plot('dates', 'values', data=data_dict)
    plt.xlabel('Czas')
    plt.ylabel('Wartość wskaźnika')
    plt.show()

# asyncio.run(show_all_station_data_chart_for_param("SO2"))
asyncio.run(get_stations_names_list())





# asyncio.run(show_station_data_chart(52))


# pprint(asyncio.run(get_all_stand_data_for_station(52)))

# data = asyncio.run(get_all_stand_data())
# Database.save_to_db(data)
# print(asyncio.run(get_stations_ids_list()))
# print(get_specific_stand_data(282))
# asyncio.run(get_stations_names_list())
# print(asyncio.run(get_all_measuring_stands_list()))