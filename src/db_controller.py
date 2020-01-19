import csv
class Database(object):

    @staticmethod
    def save_to_db(_dict: dict) -> None:
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
