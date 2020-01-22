import requests
import time
import csv
from datetime import datetime
import asyncio
import docx
import os
import json


dirname = os.path.dirname(__file__) + '/cache/'
current_date = datetime.now()
date_str = current_date.strftime("%Y-%m-%d %H:%M:%S")
date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')


def delete_paragraph(paragraph) -> None:
    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None


class API(object):

    @staticmethod
    async def get_stations() -> list:
        try:
            cached_response = docx.Document(dirname + 'get_stations.docx')
            date = cached_response.paragraphs[0].text
            data = cached_response.paragraphs[1].text
            date_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            time_diff = (current_date - date_object).total_seconds()//60
            
            if time_diff >=10:
                response = requests.get('http://api.gios.gov.pl/pjp-api/rest/station/findAll').text
                delete_paragraph(cached_response.paragraphs[1])
                delete_paragraph(cached_response.paragraphs[0])
                cached_response.add_paragraph(date_str)
                cached_response.add_paragraph(response)
                cached_response.save(dirname + 'get_stations.docx')
                return json.loads(response)
            else:
                return json.loads(data)

        except docx.opc.exceptions.PackageNotFoundError:
            print(f'get_stations.docx not found. Creating new file...')
            doc = docx.Document()
            doc.add_paragraph('2000-01-21 16:16:09')
            doc.add_paragraph('null')
            doc.save(dirname + f'get_stations.docx')
            return await API.get_stations()
    
    @staticmethod
    async def get_measuring_stands_for_station(station_id:int) -> list:
        try:
            cached_response = docx.Document(dirname + f'get_measuring_stands_for_station({station_id}).docx')
            date = cached_response.paragraphs[0].text
            data = cached_response.paragraphs[1].text
            date_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            time_diff = (current_date - date_object).total_seconds()//60
            if time_diff >=10:
                response = requests.get(f'http://api.gios.gov.pl/pjp-api/rest/station/sensors/{station_id}').text
                delete_paragraph(cached_response.paragraphs[1])
                delete_paragraph(cached_response.paragraphs[0])
                cached_response.add_paragraph(date_str)
                cached_response.add_paragraph(response)
                cached_response.save(dirname + f'get_measuring_stands_for_station({station_id}).docx')
                return json.loads(response)
            else:
                return json.loads(data)
        except docx.opc.exceptions.PackageNotFoundError:
            print(f'get_measuring_stands_for_station({station_id}).docx not found. Creating new file...')
            doc = docx.Document()
            doc.add_paragraph('2000-01-21 16:16:09')
            doc.add_paragraph('null')
            doc.save(dirname + f'get_measuring_stands_for_station({station_id}).docx')
            return await API.get_measuring_stands_for_station(station_id)
        except Exception as e:
            time.sleep(1)
            print(e)
            print(f'...fetch retry...')
            return await API.get_measuring_stands_for_station(station_id)

    @staticmethod
    async def get_measuring_stand_data(stand_id:int) -> list:
        try:
            cached_response = docx.Document(dirname + f'get_measuring_stand_data({stand_id}).docx')
            date = cached_response.paragraphs[0].text
            data = cached_response.paragraphs[1].text
            date_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            time_diff = (current_date - date_object).total_seconds()//60
            if time_diff >=10:
                response = requests.get(f'http://api.gios.gov.pl/pjp-api/rest/data/getData/{stand_id}').text
                delete_paragraph(cached_response.paragraphs[1])
                delete_paragraph(cached_response.paragraphs[0])
                cached_response.add_paragraph(date_str)
                cached_response.add_paragraph(response)
                cached_response.save(dirname + f'get_measuring_stand_data({stand_id}).docx')
                return json.loads(response)
            else:
                return json.loads(data)
        except docx.opc.exceptions.PackageNotFoundError:
            print(f'get_measuring_stand_data({stand_id}).docx not found. Creating new file...')
            doc = docx.Document()
            doc.add_paragraph('2000-01-21 16:16:09')
            doc.add_paragraph('null')
            doc.save(dirname + f'get_measuring_stand_data({stand_id}).docx')
            return await API.get_measuring_stand_data(stand_id)

            
        except Exception as e:
            time.sleep(1)
            print(e)
            print(f'...fetch retry...')
            return await API.get_measuring_stand_data(stand_id)

# asyncio.run(API.get_stations())
# asyncio.run(API.get_measuring_stand_data(292))
# asyncio.run(API.get_measuring_stands_for_station(52))