import requests
from dateutil.parser import parse  # для преобразования строк в дату и время формата datetime
import datetime


def scheduling(api_key, city_from, city_to, date, city_code_dict, transfer_true,
               cord_stations):  # функция для подсчета всеозвожных маршрутов
    url = "https://api.rasp.yandex.net/v3.0/search/"
    flag = "false"
    if transfer_true == 1:
        flag = "true"

    params = {
        "apikey": api_key,
        "from": city_code_dict[city_from],
        "to": city_code_dict[city_to],
        "date": date,
        "transfers": flag
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        # Обработка данных
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP ошибка: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Ошибка подключения: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Таймаут: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Ошибка: {err}")

    # Проверка статуса ответа
    if response.status_code == 200:
        # Парсинг JSON-ответа
        shedule = response.json()
        # Составление словаря с информацией о рейсах
        way_info = {}
        index = 0
        # print(shedule)
        for segment in shedule['segments']:
            # print(segment)
            if not segment['has_transfers']:
                way_info[index] = {"Title": segment['thread']['title'], "From": segment['from']['title'],
                                   "To": segment['to']['title'],
                                   "Departure": segment['departure'],
                                   "Arrival": segment['arrival'], "Duration": segment['duration'],
                                   "Type transport": segment['to']['transport_type'],
                                   "It_transfer": 0,
                                   "Transfers": 0,
                                   "longitude_from": cord_stations[segment['from']['code']]['longitude'],
                                   "longitude_to": cord_stations[segment['to']['code']]['longitude'],
                                   "latitude_from": cord_stations[segment['from']['code']]['latitude'],
                                   "latitude_to": cord_stations[segment['to']['code']]['latitude']}
                # "Cost": segment['tickets_info']['places']}
            else:
                way_info[index] = {}
                i = 0
                for detail in segment['details']:
                    if 'thread' in detail:
                        way_info[index][f"Title{i}"] = detail['thread']['title']
                        way_info[index][f"From{i}"] = detail['from']['title']
                        way_info[index][f"To{i}"] = detail['to']['title']
                        way_info[index][f"Departure{i}"] = detail['departure']
                        way_info[index][f"Arrival{i}"] = detail['arrival']
                        way_info[index][f"Duration{i}"] = detail['duration']
                        way_info[index][f"Type transport{i}"] = detail['thread']['transport_type']
                        way_info[index][f"Stop{i}"] = ''
                        i += 1
                way_info[index]['Departure'] = way_info[index]['Departure0']
                way_info[index]['Arrival'] = way_info[index][f'Arrival{i - 1}']
                way_info[index]['Duration'] = (
                            parse(way_info[index]['Arrival']) - parse(way_info[index]['Departure'])).total_seconds()
                way_info[index]['Transfers'] = i
                way_info[index]['It_transfer'] = 1

            # else:

            index += 1
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)  # Вывод текста ошибки

    return way_info


def getDeparture(way_info, i):  # функция для возврата времени Отправления
    return way_info[i]["Departure"]


def getArrival(way_info, i):  # функция для возврата времени прибытия
    return way_info[i]["Arrival"]


def getDuration(way_info, i):  # функция для возврата длительности
    return way_info[i]["Duration"]


def getCost(way_info, i):  # функция для возврата стоимости
    return way_info[i]["Cost"]
