import os
from api import API
from pprint import pprint
import matplotlib.pyplot as plt
from datetime import datetime
import time
import asyncio
from db_controller import Database

clear = lambda: os.system('cls') #terminal clear

async def get_stations_names_list() -> None:
    """prints a list of all available station names"""
    clear()
    station_list = await API.get_stations()
    print([station['stationName'] for station in station_list])

async def get_stations_ids_list() -> list:
    """returns all available station ids """
    station_list = await API.get_stations()
    return [station['id'] for station in station_list]

async def get_measuring_stands_list_for_station(station_id:int) -> None:
    clear()
    """prints all measuring stands list for station id specified in the argument"""
    stands_list = await API.get_measuring_stands_for_station(station_id)
    info = [stand['param']['paramName'] + " -> id: " + f"{stand['id']}" for stand in stands_list]
    print(info)

async def get_all_stand_data() -> dict:
    """returns a nested dictionary of all available data for all stations"""
    clear()
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
    print('All stand data collected successfully')
    return data

async def get_all_stand_data_for_station(station_id:int) -> list:
    """returns a nested dictionary list for station id specified in the argument"""
    stands_list = await API.get_measuring_stands_for_station(station_id)
    stand_id_list = [stand['id'] for stand in stands_list]
    data_for_stand = []
    for id in stand_id_list:
        print(f'---- {id} stand data...')
        element = await API.get_measuring_stand_data(id)
        data_for_stand.append(element)
    return data_for_stand

async def get_specific_stand_data(*args:int) -> list:
    """returns data for specific measuring stand ids specified in *args"""
    data_for_stand = [await API.get_measuring_stand_data(id) for id in args]
    return data_for_stand

async def get_all_measuring_stands_list(p = 0) -> list:
    """returns a list of tuples containing stand type and stand id gathered from all stations
    if argument p == 1, prints measuring stand list"""
    clear()
    station_list = await API.get_stations()
    result = []
    print('Loading data...')
    specific_stand_id_list =[]
    for station in station_list:
        measuring_stands = await API.get_measuring_stands_for_station(station['id'])
        stands_list = [ (stand["id"], stand['param']['paramName'], stand['param']['paramCode']) for stand in measuring_stands]
        info = f'{[station["id"]]}{ station["stationName"]}: { ", ".join([f"[{stand[0]}]{stand[1]}({stand[2]})" for stand in stands_list]) }'
        result.append(info)
        for stand in stands_list:
            specific_stand_id_list.append((stand[2], stand[0]))
    if p == 1:
        for info in result:
            print(info)
    return specific_stand_id_list

async def show_station_data_chart(station_id:int) -> None:
    """generates a chart presenting all data for station id specified in the argument"""
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
    plt.ylabel('Warto???? wska??nika')
    plt.legend()
    plt.show()

async def show_all_station_data_chart_for_param(param:str) -> None:
    """returns data for specific measuring stand type specified in the argument for all stations"""
    clear()
    specific_stand_id_list = await get_all_measuring_stands_list()
    data = []
    current_stand = 1
    clear()
    for stand_id in specific_stand_id_list:
        if stand_id[0] == param:
            print(f'Loading {current_stand} stand data...', end = '\r')
            stand_data = await API.get_measuring_stand_data(stand_id[1])
            data.append(stand_data)
            current_stand += 1
    if len(data) != 0:
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
        plt.ylabel('Warto???? wska??nika')
        plt.show()
    else:
        print('No stands with such parameter found.')
