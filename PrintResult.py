from dateutil.parser import parse  # для преобразования строк в дату и время формата datetime


def result(way_info):
    for i in way_info:
        print(f"=======Маршрут №{i + 1}=======")
        if 'Departure0' not in way_info[i]:
            print(f'Маршрут: {way_info[i]["Title"]}')
            # print(f'longitude_from: {way_info[i]["longitude_from"]}')
            # print(f'longitude_to: {way_info[i]["longitude_to"]}')
            # print(f'latitude_from: {way_info[i]["latitude_from"]}')
            # print(f'latitude_from: {way_info[i]["latitude_from"]}')
            print(f'От: {way_info[i]["From"]}')
            print(f'До: {way_info[i]["To"]}')
            print(f'Отправление: {parse(way_info[i]["Departure"])}')
            print(f'Прибытие: {parse(way_info[i]["Arrival"])}')
            print(
                f'Длительность: {int(way_info[i]["Duration"] // 3600)}ч. {int(way_info[i]["Duration"] % 3600 // 60)}мин.')
            # print(f'Длительность: {parse(way_info[i]["Departure"]) - parse(way_info[i]["Arrival"])}')
            # if way_info[i]["Cost"] is not None:
            # print(f'Цена: {way_info[i]["Cost"]} {way_info[i]["Currency"]}')
            # else:
            # print("Цена: Нет информации")
            print(f'Тип транспорта: {way_info[i]["Type transport"]}')
            print("----------------")
        else:
            for j in range(way_info[i]['Transfers']):
                print(f'Маршрут: {way_info[i][f"Title{j}"]}')
                print(f'От: {way_info[i][f"From{j}"]}')
                print(f'До: {way_info[i][f"To{j}"]}')
                print(f'Отправление: {parse(way_info[i][f"Departure{j}"])}')
                print(f'Прибытие: {parse(way_info[i][f"Arrival{j}"])}')
                print(
                    f'Длительность: {int(way_info[i][f"Duration{j}"] // 3600)}ч. {int(way_info[i][f"Duration{j}"] % 3600 / 60)}мин.')
                print(f'Тип транспорта: {way_info[i][f"Type transport{j}"]}')
                if j != way_info[i]['Transfers'] - 1:
                    print("----ПЕРЕСАДКА----")
            print("-------------------")
            print(
                f'Общая длительность: {int(way_info[i]["Duration"] // 3600)}ч. {int(way_info[i]["Duration"] % 3600 // 60)}мин.')
            print(f'Кол-во пересадок: {way_info[i]["Transfers"] - 1}')
            print("-------------------")
        print("")


def resultN(way_info, count_cities):
    # print(way_info)
    for i in way_info:
        print(f"============Маршрут №{i + 1}==========")
        for j in way_info[i]:
            # print(way_info[i][j])
            if j not in ['Total cost', 'Duration', 'Transfers']:
                if way_info[i][j]["It_transfer"] == 0:
                    print(f'Маршрут: {way_info[i][j]["Title"]}')
                    print(f'От: {way_info[i][j][f"From"]}')
                    print(f'До: {way_info[i][j][f"To"]}')
                    print(f'Отправление: {parse(way_info[i][j]["Departure"])}')
                    print(f'Прибытие: {parse(way_info[i][j]["Arrival"])}')
                    print(
                        f'Длительность: {int(way_info[i][j]["Duration"] // 3600)}ч. {int(way_info[i][j]["Duration"] % 3600 // 60)}мин.')
                    print(f'Тип транспорта: {way_info[i][j][f"Type transport"]}')

                else:
                    for k in range(way_info[i][j]['Transfers']):
                        print(f'Маршрут: {way_info[i][j][f"Title{k}"]}')
                        print(f'От: {way_info[i][j][f"From{k}"]}')
                        print(f'До: {way_info[i][j][f"To{k}"]}')
                        print(f'Отправление: {parse(way_info[i][j][f"Departure{k}"])}')
                        print(f'Прибытие: {parse(way_info[i][j][f"Arrival{k}"])}')
                        print(
                            f'Длительность: {int(way_info[i][j][f"Duration{k}"] // 3600)}ч. {int(way_info[i][j][f"Duration{k}"] % 3600 / 60)}мин.')
                        print(f'Тип транспорта: {way_info[i][j][f"Type transport{k}"]}')
                        if k != way_info[i][j]['Transfers'] - 1:
                            print("----ПЕРЕСАДКА----")
                print('-------------------')
            elif j != 'Transfers':
                print(
                    f'Общая длительность: {int(way_info[i]["Duration"] // 3600)}ч. {int(way_info[i]["Duration"] % 3600 // 60)}мин.')
                print(f'Кол-во пересадок: {way_info[i]["Transfers"]}')
                print('-------------------')

        print("")
