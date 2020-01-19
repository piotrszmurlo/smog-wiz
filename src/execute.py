from api import API
from app import get_measuring_stands_list_for_station, get_all_stand_data_for_station, get_station_list, get_specific_stand_data, get_all_measuring_stands_list
import requests
from pprint import pprint
import matplotlib.pyplot as plt

# pprint(API.get_measuring_stands_for_station(14))
# pprint(API.get_measuring_stand_data(92))





# try:
#     get_all_stand_data_for_station(52)
# except:
#     print('Błąd: proszę podać numer identyfikacyjny stanowiska pomiarowego')

# try:
#     get_specific_stand_data(6434, 52)
# except:
#     print('Błąd: proszę podać numery identyfikacyjne stanowisk pomiarowych po przecinku')


# try:
#     get_measuring_stands_list_for_station()
# except:
#     print('Błąd: proszę podąć numer identyfikacyjny stacji')

# try:
#     get_all_measuring_stands_list()
# except Exception as e:
#     print(e)

pprint(get_all_stand_data_for_station(52))
