import requests
import json


def dictAllStation(api_key):
    # Создание словаря с названиями городов и их кодами
    with open('stations_list.json', 'r') as fcc_file:
        data = json.load(fcc_file)
    city_code_dict = {}

    for country in data['countries']:
        for region in country.get('regions', []) + country.get('regions', []):
            for settlement in region.get('settlements', []):
                title = settlement.get('title')
                code = settlement.get('codes', {}).get('yandex_code')
                if title and code:
                    city_code_dict[title] = code
    return city_code_dict


def cord_stations(api_key):
    with open('stations_list.json', 'r') as fcc_file:
        data = json.load(fcc_file)

    result = {}

    # Обрабатываем JSON
    for country in data["countries"]:
        for region in country["regions"]:
            for settlement in region["settlements"]:
                for station in settlement["stations"]:
                    # Извлекаем код станции, долготу и широту
                    station_code = station["codes"]["yandex_code"]
                    longitude = station["longitude"]
                    latitude = station["latitude"]

                    # Добавляем в результат
                    result[station_code] = {
                        "longitude": longitude,
                        "latitude": latitude
                    }

    return result
