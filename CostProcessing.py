def processing(way_info):
    # Обработка цены
    for i in way_info:
        if type(way_info[i]["Cost"]) == 'list':
            way_info[i]["Cost"] = way_info[i]["Cost"][0]['price']['whole'] + way_info[i]["Cost"][0]['price'][
                'cents'] / 100
            way_info[i]["Currency"] = way_info[i]["Cost"][0]['currency']
        else:
            way_info[i]["Cost"] = None
            way_info[i]["Currency"] = None
