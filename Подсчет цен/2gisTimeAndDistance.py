import requests


def get_coordinates(api_key, location_name):
    """Конвертирует название места в координаты (широта, долгота) с использованием 2GIS Geocoding API."""
    url = "https://catalog.api.2gis.com/3.0/items/geocode"
    params = {
        "q": location_name,  # Наименование локации
        "fields": "items.point",
        "key": api_key
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверяем, что запрос успешен
        data = response.json()
        if data.get('result') and data['result'].get('items'):
            point = data['result']['items'][0]['point']
            return point['lat'], point['lon']
        else:
            raise Exception(f"Место '{location_name}' не найдено.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при запросе к Geocoding API: {e}")


def get_travel_time(api_key, start_location, end_location):
    """Рассчитывает время в пути между двумя точками с использованием 2GIS Routing API."""
    try:
        # Получаем координаты начальной и конечной точек
        start_lat, start_lon = get_coordinates(api_key, start_location)
        end_lat, end_lon = get_coordinates(api_key, end_location)

        # Проверяем, что координаты получены
        if not all([start_lat, start_lon, end_lat, end_lon]):
            raise Exception("Не удалось получить координаты для одной из точек.")

        # Используем Routing API для расчета времени в пути
        url = f"http://routing.api.2gis.com/routing/7.0.0/global?key={api_key}"
        headers = {
            "Content-Type": "application/json"  # Указываем, что отправляем JSON
        }
        payload = {
            "points": [
                {"lat": start_lat, "lon": start_lon},
                {"lat": end_lat, "lon": end_lon}
            ],
            "route_mode": "fastest",
            "traffic_mode": "jam",
            "transport": "taxi",

        }

        # Выводим URL и тело запроса для диагностики
        # print(f"Диагностика: URL запроса: {url}")
        # print(f"Диагностика: Тело запроса (JSON): {payload}")

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Проверяем, что запрос успешен
        data = response.json()

        # Выводим полный ответ от API для диагностики
        # print(f"Диагностика: Ответ от API: {data}")

        if data.get('result'):
            # Возвращаем время в пути в секундах
            return data['result'][0]['total_duration']
        else:
            raise Exception("Маршрут не может быть построен.")
    except requests.exceptions.RequestException as e:
        # Выводим подробную информацию об ошибке
        if e.response is not None:
            error_details = e.response.json()
            raise Exception(f"Ошибка при запросе к Routing API: {e}. Детали: {error_details}")
        else:
            raise Exception(f"Ошибка при запросе к Routing API: {e}")


def get_travel_distance(api_key, start_location, end_location):
    """Рассчитывает расстояние в метрах между двумя точками с использованием 2GIS Routing API."""
    try:
        # Получаем координаты начальной и конечной точек
        start_lat, start_lon = get_coordinates(api_key, start_location)
        end_lat, end_lon = get_coordinates(api_key, end_location)

        # Проверяем, что координаты получены
        if not all([start_lat, start_lon, end_lat, end_lon]):
            raise Exception("Не удалось получить координаты для одной из точек.")

        # Используем Routing API для расчета длины пути
        url = f"http://routing.api.2gis.com/routing/7.0.0/global?key={api_key}"
        headers = {
            "Content-Type": "application/json"  # Указываем, что отправляем JSON
        }
        payload = {
            "points": [
                {"lat": start_lat, "lon": start_lon},
                {"lat": end_lat, "lon": end_lon}
            ],
            "route_mode": "fastest",
            "traffic_mode": "jam",
            "transport": "taxi",

        }

        # Выводим URL и тело запроса для диагностики
        # print(f"Диагностика: URL запроса: {url}")
        # print(f"Диагностика: Тело запроса (JSON): {payload}")

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Проверяем, что запрос успешен
        data = response.json()

        # Выводим полный ответ от API для диагностики
        # print(f"Диагностика: Ответ от API: {data}")

        if data.get('result'):
            # Возвращаем длину пути в метрах
            return data['result'][0]['total_distance']
        else:
            raise Exception("Маршрут не может быть построен.")
    except requests.exceptions.RequestException as e:
        # Выводим подробную информацию об ошибке
        if e.response is not None:
            error_details = e.response.json()
            raise Exception(f"Ошибка при запросе к Routing API: {e}. Детали: {error_details}")
        else:
            raise Exception(f"Ошибка при запросе к Routing API: {e}")


def calculate_taxi_price(city, travel_time, travel_distance):
    if city == 'Москва':
        return 189 + (travel_time // 60 - 3) * 13 + (travel_distance//1000 - 1) * 13
    elif city == 'Санкт-Петербург':
        return 149 + (travel_time // 60 - 3) * 12 + (travel_distance//1000 - 1) * 12
    else:
        return 90 + (travel_time // 60 - 3) * 6 + (travel_distance//1000 - 1) * 13


# Пример использования
api_key = "2d86e52d-8def-4f74-8a10-aeeb79d19364"
start_location = "Шереметьево"  # Стартовая точка
end_location = "Внуково"  # Конечная точка

try:
    travel_time = get_travel_time(api_key, start_location, end_location)
    travel_distance = get_travel_distance(api_key, start_location, end_location)
    print(f"Время в пути: {travel_time} секунд (~{travel_time // 60} минут)")
    print(f"Длина пути: {travel_distance} м")
except Exception as e:
    print(f"Ошибка: {e}")

