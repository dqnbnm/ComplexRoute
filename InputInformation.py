import datetime


def input_count_cities():  # функция для ввода пользоваталем кол-ва городов
    f = 0
    while f == 0:
        try:
            count_cities = int(input("Введите кол-во городов в маршруте: "))
        except:
            print("Введено не число")
        else:
            if count_cities < 2:
                print("Число должно быть больше 2")
            else:
                f = 1
    return count_cities


def input_cities(count_cities, city_code_dict):  # функция для ввода пользоваталем городов
    cities = []
    for i in range(count_cities):
        f = 0
        while f == 0:
            city = input(f"Введите город_{i + 1}: ")
            if city not in city_code_dict:
                print("Город не существует или введен неверно")
            elif len(cities) != 0 and city == cities[-1]:
                print("Нельзя вводить два одинаковых города подряд")

            elif city in city_code_dict:
                cities.append(city)
                f = 1

    return cities


def input_dates(count_cities, cities):  # функция для ввода пользоваталем дат
    dates = []
    current_date = datetime.datetime.now()
    for i in range(count_cities - 1):
        f = 0
        while f == 0:
            date = input(f'Введите дату отправления из {cities[i]}(YYYY-MM-DD): ')
            try:
                date_try = datetime.datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                print('Введена неверная дата')
            else:
                date_difference = date_try - current_date
                if date_difference < datetime.timedelta(days=-1) or date_difference > datetime.timedelta(days=330):
                    print("Введеная дата должна быть не меньше текущей даты и не позже 11 месяцев текущей даты")
                else:
                    dates.append(date)
                    f = 1
    return dates


def transfer_true():
    f = 0
    while f == 0:
        try:
            transfer = int(input("Введите '0' - если пересадки не нужны\nВведите '1' - если пересадки позволительны: "))
        except:
            print("Введено не число")
        else:
            if transfer != 1 and transfer != 0:
                print("Введите 0 или 1")
            else:
                f = 1
    return transfer


def sort_type(transfers_flag):
    f = 0
    if transfers_flag == 1:
        while f == 0:
            try:
                type = int(input(
                    "Введите '0' - если сортировка не нужна(сокращает до 50 вариантов)\nВведите '1' - если сортировать по длительности маршрута(сокращает до 50 вариантов)\nВведите '2' - если сортировать по кол-ву пересадок(сокращает до 50 вариантов)\nВведите '3' - если сортировать по длительности и кол-ву пересадок(сокращает до 50 вариантов)\nВведите '-1' - если сортировка не нужна и сокращать кол-во вариантов не нужно: "))
            except:
                print("Введено не число")
            else:
                if type != 1 and type != 2 and type != 3 and type != 0 and type != -1:
                    print("Введите 0, 1, 2, 3 или -1")
                else:
                    f = 1
    else:
        try:
            type = int(input(
                "Введите '0' - если сортировка не нужна(сокращает до 50 вариантов)\nВведите '1' - если сортировать по длительности маршрута(сокращает до 50 вариантов)\nВведите '-1' - если сортировка не нужна и сокращать кол-во вариантов не нужно: "))
        except:
            print("Введено не число")
        else:
            if type != 1 and type != 0 and type != -1:
                print("Введите 0, 1 или -1")
            else:
                f = 1
    return type
