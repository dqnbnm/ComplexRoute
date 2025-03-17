import AllStation  # хранит функцию, которая получает города и их коды
import PrintResult  # хранит функции для вывода результатов
import CostProcessing  # обрабатывает цену
from Shedule import *  # хранит функции для создания маршрутов
import InputInformation  # хранит функции ввода данных
import requests
from Sorting import *
from dateutil.parser import parse  # для преобразования строк в дату и время формата datetime
import datetime  # для работы с типом datetime

api_key = "2bf3a1da-70bc-4b3d-a712-c29b164556a1"  # апи ключ для работы с Яндекс расписанием

city_code_dict = AllStation.dictAllStation(api_key)  # получение словаря формата Город : код(яндекс)
cord_stations = AllStation.cord_stations(api_key)
count_cities = InputInformation.input_count_cities()  # ввод пользователем кол-во городов
cities = InputInformation.input_cities(count_cities, city_code_dict)  # ввод пользователем городов
dates = InputInformation.input_dates(count_cities, cities)  # ввод пользователем дат отправления из городов
transfer_true = InputInformation.transfer_true()
sort_type = InputInformation.sort_type(transfer_true)
if count_cities > 2:  # если кол-во городов больше двух
    way_info = {}  # словарь для сохранения результатов
    index = 0
    for i in range(count_cities - 2):
        if i == 0:  # если первая итерация
            # получаем всевозможные пути из городов в определенную дату
            way_info1 = scheduling(api_key, cities[i], cities[i + 1], dates[i], city_code_dict, transfer_true,
                                   cord_stations)
            # CostProcessing.processing(way_info1)
        else:
            way_info1 = way_info
        way_info2 = scheduling(api_key, cities[i + 1], cities[i + 2], dates[i + 1], city_code_dict, transfer_true,
                               cord_stations)
        # CostProcessing.processing(way_info2)
        if i == 0:
            for j in way_info1:  # проходимся по маршрутам из города А в Б
                for k in way_info2:  # проходимся по маршрутам из города Б в В
                    # если отправление из города Б позже прибытия в город Б
                    if parse(getDeparture(way_info2, k)) > parse(getArrival(way_info1, j)):
                        # соединяем строки в результат
                        way_info[index] = {0: {**way_info1[j]}, 1: {**way_info2[k]}}
                        index += 1

        else:
            # print(way_info1)
            for j in range(len(way_info1)):  # проходимся по результату полученному в прердыдущем шаге
                for k in way_info2:  # проходимся по маршрутам из города Б в В
                    # если отправление из города Б позже прибытия в город Б
                    if parse(getDeparture(way_info2, k)) > parse(getArrival(way_info1[j], i)):
                        # if getCost(way_info1[j], i) is None or getCost(way_info2, k) is None:
                        way_info[index] = {**way_info1[j], **{i + 1: way_info2[k]}}
                        index += 1
                        # else:
                        # way_info[index] = {**way_info1[j], **{i + 1: way_info2[k]}}
                        # index += 1
    result = {}  # словарь с итоговым результатом
    index = 0
    for i in way_info:
        if len(way_info[i]) == count_cities - 1:  # если нужное кол-во маршрутов
            result[index] = {**way_info[i], **{"Duration": 0}, **{"Transfers": 0}}  # добавляем в итоговый результат
            for j in result[index]:
                if j != "Duration" and j != "Transfers":
                    result[index]["Duration"] += result[index][j]["Duration"]  # считаем общую длительность
                    if result[index][j]["It_transfer"] == 1:
                        result[index]["Transfers"] += result[index][j]["Transfers"] - 1
            index += 1
    if len(result) == 0:
        print("Маршруты не найдены")
    else:
        result = sort_result(result, sort_type)
        PrintResult.resultN(result, count_cities)  # выводим результат из n городов

    """for i in range(len(way_info)):
        if len(way_info[i]) != count_cities + 1:
            del way_info[i]"""
    # print(way_info)




else:
    way_info = scheduling(api_key, cities[0], cities[1], dates[0], city_code_dict, transfer_true,
                          cord_stations)  # считаем всевозможные маршруты
    if len(way_info) == 0:
        print("Маршруты не найдены")
    # CostProcessing.processing(way_info)
    way_info = sort_result(way_info, sort_type)
    PrintResult.result(way_info)  # выводим результат из 2 городов
