import csv
from datetime import datetime
from api import API
import os

clear = lambda: os.system('cls')

class Database(object):

    @staticmethod
    def overwrite_db(_dict: dict) -> None:
        """overwrites db.csv with API data"""
        with open('db.csv', 'w', newline='') as file:
            fieldnames = ['station_id', 'stand_name', 'date', 'value']
            writer = csv.DictWriter(file, fieldnames = fieldnames)
            writer.writeheader()
            for station_id, stands_list in _dict.items():
                for stand_dict in stands_list:
                    stand_name, stand_data = stand_dict.values()
                    for record in stand_data:
                        date, value = record.values()
                        writer.writerow({
                            'station_id': station_id,
                            'stand_name': stand_name,
                            'date': date,
                            'value': value
                        })

    @staticmethod
    async def append_to_db(_dict: dict) -> None:
        """appends new API data to db.csv"""
        print("Starting database update...")
        station_list = await API.get_stations()
        update_count = 0
        stations_count = 1
        stations_number = len([station['stationName'] for station in station_list])
        newest_db_date = datetime.strptime('2020-01-01 17:00:00', '%Y-%m-%d %H:%M:%S')
        with open('db.csv', 'r') as file:
            fieldnames = ['station_id', 'stand_name', 'date', 'value']
            reader = csv.DictReader(file, fieldnames = fieldnames, delimiter = ',')
            line_list = list(reader)
            for row in line_list:
                try:
                    record_date = datetime.strptime(str(row['date']), '%Y-%m-%d %H:%M:%S')
                    time_diff = (record_date - newest_db_date).total_seconds()
                    if time_diff > 0:
                        newest_db_date = record_date
                except ValueError:
                    pass
        for station_id, stands_list in _dict.items():
            # print("Starting database update...")
            print(f'Integrating station {stations_count} of {stations_number}', end= '\r')
            stations_count += 1
            for stand_dict in stands_list:
                stand_name, stand_data = stand_dict.values()
                for record in stand_data:
                    date, value = record.values()
                    try:
                        date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        pass
                    time_diff = (date_obj - newest_db_date).total_seconds()
                    if time_diff > 0:
                        with open('db.csv', 'a', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames = fieldnames)
                                    writer.writerow({
                                        'station_id': station_id,
                                        'stand_name': stand_name,
                                        'date': date,
                                        'value': value
                                    })
                        update_count += 1
        print(f'Database integrating completed. Collected {update_count} new record(s)')