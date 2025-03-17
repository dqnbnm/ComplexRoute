def sort_result(result, sort_type):
    if sort_type == 1:
        result_sort = sorted(result.items(), key=lambda x: x[1]['Duration'])
        result = dict((i[0], i[1][1]) for i in enumerate(result_sort))
    elif sort_type == 2:
        result_sort = sorted(result.items(), key=lambda x: x[1]['Transfers'])
        result = dict((i[0], i[1][1]) for i in enumerate(result_sort))
    elif sort_type == 3:
        result_sort = sorted(result.items(), key=lambda x: x[1]['Transfers'] + x[1]['Duration'])
        result = dict((i[0], i[1][1]) for i in enumerate(result_sort))
    elif sort_type == -1:
        return result
    result_sort = {}
    if len(result) > 50:
        for i in range(50):
            result_sort[i] = result[i]
        return result_sort
    return result

    # {1: {Transfers, Duration}, 2: {Transfers, Duration}...}
