import requests
import pandas as pd
from tabulate import tabulate

def get_ticket_price(origin_airport, destination_airport, depart_date_time):
    API_TOKEN = '976c7cac8bfc5a4e17307fd584038a90'
    BASE_URL = 'http://api.travelpayouts.com/aviasales/v3/get_latest_prices'

    airport_codes = {
        'Москва': ['SVO', 'DME', 'VKO', 'ZIA'],
        'Санкт-Петербург': ['LED'],
        'Новосибирск': ['OVB'],
        'Екатеринбург': ['SVX'],
        'Казань': ['KZN'],
        'Сочи': ['AER'],
        'Краснодар': ['KRR'],
        'Самара': ['KUF'],
        'Уфа': ['UFA'],
        'Ростов-на-Дону': ['ROV'],
        'Владивосток': ['VVO'],
        'Омск': ['OMS'],
        'Пермь': ['PEE'],
        'Челябинск': ['CEK'],
        'Хабаровск': ['KHV'],
        'Иркутск': ['IKT'],
        'Красноярск': ['KJA'],
        'Воронеж': ['VOZ'],
        'Калининград': ['KGD'],
        'Мурманск': ['MMK'],
        'Архангельск': ['ARH'],
        'Анапа': ['AAQ'],
        'Астрахань': ['ASF'],
        'Барнаул': ['BAX'],
        'Белгород': ['EGO'],
        'Благовещенск': ['BQS'],
        'Братск': ['BTK'],
        'Владикавказ': ['OGZ'],
        'Волгоград': ['VOG'],
        'Геленджик': ['GDZ'],
        'Грозный': ['GRV'],
        'Иваново': ['IWA'],
        'Ижевск': ['IJK'],
        'Калуга': ['KLF'],
        'Кемерово': ['KEJ'],
        'Киров': ['KVX'],
        'Курган': ['KRO'],
        'Курск': ['URS'],
        'Липецк': ['LPK'],
        'Магадан': ['GDX'],
        'Магнитогорск': ['MQF'],
        'Минеральные Воды': ['MRV'],
        'Надым': ['NYM'],
        'Нальчик': ['NAL'],
        'Нижнекамск': ['NBC'],
        'Нижний Новгород': ['GOJ'],
        'Новый Уренгой': ['NUX'],
        'Норильск': ['NSK'],
        'Оренбург': ['REN'],
        'Пенза': ['PEZ'],
        'Петрозаводск': ['PES'],
        'Петропавловск-Камчатский': ['PKC'],
        'Псков': ['PKV'],
        'Саратов': ['GSV'],
        'Симферополь': ['SIP'],
        'Ставрополь': ['STW'],
        'Сургут': ['SGC'],
        'Томск': ['TOF'],
        'Тюмень': ['TJM'],
        'Улан-Удэ': ['UUD'],
        'Ульяновск': ['ULY'],
        'Ханты-Мансийск': ['HMA'],
        'Чебоксары': ['CSY'],
        'Чита': ['HTA'],
        'Элиста': ['ESL'],
        'Южно-Сахалинск': ['UUS'],
        'Якутск': ['YKS'],
        'Ярославль': ['IAR']
    }

    params = {
        'origin': origin_airport.encode('utf-8').decode('utf-8', 'ignore'),  # Принудительно кодируем в UTF-8
        'destination': destination_airport.encode('utf-8').decode('utf-8', 'ignore'),
        'currency': 'rub',
        'period_type': 'day',
        'one_way': 'false',
        'show_to_affiliates': 'true',
        'limit': 30,
        'beginning_of_period': depart_date_time.split()[0],
        'token': API_TOKEN
    }

    params = {k: v.encode('utf-8', 'ignore').decode('utf-8') if isinstance(v, str) else v for k, v in params.items()}

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json().get('data', [])
        if not data:
            print("\nДанные отсутствуют! Попробуй изменить параметры запроса.")
            return None

        df = pd.DataFrame(data)

        df['depart_date'] = pd.to_datetime(df['depart_date']).dt.strftime('%Y-%m-%d %H:%M')
        df['return_date'] = pd.to_datetime(df['return_date']).dt.strftime('%Y-%m-%d %H:%M')

        df = df[df['depart_date'].str.contains(depart_date_time.split()[0])]

        if df.empty:
            print("\nНа указанную дату рейсов нет.")
            return None

        df['origin_airport'] = df['origin']
        df['destination_airport'] = df['destination']

        df = df[['origin_airport', 'destination_airport', 'depart_date', 'value']]
        df.columns = ['Аэропорт отправления', 'Аэропорт назначения', 'Дата вылета', 'Цена']


        #print("\nНайдено рейсов:")
        #print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))


        ticket = df[df['Дата вылета'] == depart_date_time]

        if not ticket.empty:
            price = int(ticket.iloc[0]['Цена'])
            return price
        else:
            return None
    else:
        print(f"\nОшибка: {response.status_code}, {response.text}")
        return None


origin_airport = input("код аэропорта отправления: ").strip().upper()
destination_airport = input("код аэропорта назначения: ").strip().upper()
depart_date_time = input("точное время отправления в формате YYYY-MM-DD HH:MM: ").strip()


price = get_ticket_price(origin_airport, destination_airport, depart_date_time)

if price:
    print(f"\nЦена билета: {price} рублей")
else:
    print("\nРейс с таким временем не найден.")
