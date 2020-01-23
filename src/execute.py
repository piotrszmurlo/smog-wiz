from api import API
import app
import requests
from pprint import pprint
import matplotlib.pyplot as plt
import os
import asyncio
from db_controller import Database

if __name__ == "__main__":
    clear = lambda: os.system('cls')
    clear()
    print('Welcome to SmogWiz 2.0. Type "help" to get a list of commands.')
    command = ''
    while command != 'quit':
        command = input('Type in a command: ').lower()
        if command == 'help':
            print('To run following functions, type in the value written in square brackets.')
            print('Available functions:')
            print(' [1] -> list all available GIOS stations', '\n', 
            '[2] -> list all measuring stands for a GIOS station', '\n',
            '[3] -> list all available measuring stands for all stations', '\n',
            '[4] -> list all measuring stand data for station', '\n',
            '[5] -> show station data chart', '\n',
            '[6] -> show all station data chart for a specified parameter', '\n',
            '[7] -> update database', '\n',
            '[8] -> erase and overwrite database')
        elif command == '1':
            asyncio.run(app.get_stations_names_list())
        elif command == '2':
            try:
                station_id = int(input('Type in station id: '))
                asyncio.run(app.get_measuring_stands_list_for_station(station_id))
            except ValueError:
                print('Invalid station id')
        elif command == '3':
            asyncio.run(app.get_all_measuring_stands_list(p=1))
        elif command == '4':
            try:
                station_id = int(input('Type in station id: '))
                pprint(asyncio.run(app.get_all_stand_data_for_station(station_id)))
            except ValueError:
                print('Invalid station id')
        elif command == '5':
            try:
                station_id = int(input('Type in station id: '))
                asyncio.run(app.show_station_data_chart(station_id))
            except ValueError:
                print('Invalid station id')
        elif command == '6':
            param = input('Provide a valid param (ex. "CO2"): ').upper()
            asyncio.run(app.show_all_station_data_chart_for_param(param))
        elif command == '7':
            data = asyncio.run(app.get_all_stand_data())
            asyncio.run(Database.append_to_db(data))
        elif command == '8':
            print('Warning! This will overwrite (erase) all current database records.')
            consent = input('Do you wish to continue? (y/n) ').lower()
            if consent == 'y':
                data = asyncio.run(app.get_all_stand_data())
                asyncio.run(Database.overwrite_db(data))
        elif command != 'quit':
            print('Unknown command. Type "help" to get a list of commands.')
    else:
        print('Quitting SmogWiz...')

