import csv
from datetime import datetime
from api import API

class Database(object):

    @staticmethod
    def save_to_db(_dict: dict) -> None:
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
        print("Starting database update... please wait few minutes...")
        station_list = await API.get_stations()
        update_count = 0
        stations_count = 1
        stations_number = len([station['stationName'] for station in station_list])
        with open('db.csv', 'r') as file:
            fieldnames = ['station_id', 'stand_name', 'date', 'value']
            reader = csv.DictReader(file, fieldnames = fieldnames, delimiter = ',')
            line_list = list(reader)
            line_list_len = len(line_list)
            for station_id, stands_list in _dict.items():
                print(f'Integrating station {stations_count} of {stations_number}')
                stations_count += 1
                for stand_dict in stands_list:
                    stand_name, stand_data = stand_dict.values()
                    for record in stand_data:
                        date, value = record.values()
                        current_line = 1
                        for row in line_list:
                            if str(row['station_id']) == str(station_id) and str(row['stand_name']) == str(stand_name) and str(row['date']) == str(date):
                                break
                            elif current_line == line_list_len:
                                with open('db.csv', 'a', newline='') as file:
                                            writer = csv.DictWriter(file, fieldnames = fieldnames)
                                            writer.writerow({
                                                'station_id': station_id,
                                                'stand_name': stand_name,
                                                'date': date,
                                                'value': value
                                            })
                                update_count += 1
                            else:
                                current_line += 1
        print(f'Database integrating completed. Collected {update_count} new record(s)')