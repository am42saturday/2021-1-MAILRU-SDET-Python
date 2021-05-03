import os
import re
import json
import sys


# Регулярка для разделения строки логов nginx на составляющие:
#   ip-адрес,
#   дата и время запроса
#   метод
#   location(url)
#   http/1.0 или http/1.1
#   статус код
#   размер запроса
#   referer
#   useragent
lineformat = re.compile(r'(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - '
                        r'\[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] '
                        r'(["](?P<method>[^"]+)[ ](?P<url>.+)(http\/1\.[01]")) '
                        r'(?P<statuscode>\d{3}) (?P<bytessent>\d+|-) (?P<referer>-|"([^"]*)"|".*[^\\]") '
                        r'(?P<useragent>"([^"]*)"|".*[^\\]")', re.IGNORECASE)


# 1) Общее количество запросов:
def number_of_requests():
    with open(os.path.abspath('access.log'), 'r', encoding='utf-8') as logs:
        count = 0
        for _ in logs.readlines():
            count += 1
        return {"Общее количество запросов": count}  # 225133


# 2) Общее количество запросов по типу, например: GET - 20, POST - 10 и т.д.
def number_of_requests_by_method():
    result_data = []
    with open(os.path.abspath('access.log'), 'r', encoding='utf-8') as logs:
        for line in logs.readlines():
            data = re.search(lineformat, line)
            if data:
                datadict = data.groupdict()
                method = datadict["method"]
                result_data.append(method)
            else:
                print(line)

    counts = dict()
    for i in result_data:
        counts[i] = counts.get(i, 0) + 1
        # {'POST': 102503,
        # 'GET': 122095,
        # 'HEAD': 528,
        # 'PUT': 6,
        # 'g369g=%40eval%01%28base64_decode%28%24_POST%5Bz0%5D%29%29%3B&z0=QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2bfCIpOztlY2hvKCJlNTBiNWYyYjRmNjc1NGFmMDljYzg0NWI4YjU4ZTA3NiIpOztlY2hvKCJ8PC0iKTs7ZGllKCk7GET': 1}
    return {"Общее количество запросов по типу": counts}


# 3) Топ 10 самых частых запросов:
#   должен выводиться url
#   должно выводиться число запросов
def top_10_frequent_requests():
    result_data = []
    with open(os.path.abspath('access.log'), 'r', encoding='utf-8') as logs:
        for line in logs.readlines():
            data = re.search(lineformat, line)
            datadict = data.groupdict()
            if data:
                url = datadict["url"]
                result_data.append(url)

    counts = dict()
    for i in result_data:
        counts[i] = counts.get(i, 0) + 1
    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
    # [('/administrator/index.php ', 103932),
    # ('/apache-log/access.log ', 26336),
    # ('/ ', 6940),
    # ('/templates/_system/css/general.css ', 4980),
    # ('/robots.txt ', 3199),
    # ('http://almhuette-raith.at/administrator/index.php ', 2356),
    # ('/favicon.ico ', 2201),
    # ('/wp-login.php ', 1644),
    # ('/administrator/ ', 1563),
    # ('/templates/jp_hotel/css/template.css ', 1287)]
    return {"Топ 10 самых частых запросов": list(sorted_counts.items())[:10]}


# 4) Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой:
#   должен выводиться url
#   должен выводиться статус код
#   должен выводиться размер запроса
#   должен выводиться ip адрес
def top_5_largest_4xx_requests():
    result_data = []
    with open(os.path.abspath('access.log'), 'r', encoding='utf-8') as logs:
        for line in logs.readlines():
            data = re.search(lineformat, line)
            datadict = data.groupdict()
            pattern = re.compile(r'4..')
            if data and pattern.search(datadict["statuscode"]):
                ip = datadict["ipaddress"]
                url = datadict["url"]
                bytessent = datadict["bytessent"]
                status = datadict["statuscode"]
                result_data.append([url, status, bytessent, ip])

    return {'Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой': sorted(result_data, key=lambda elem: int(elem[2]), reverse=True)[:5]}
    # [['/index.php?option=com_phocagallery&view=category&id=4025&Itemid=53 ', '404', '1417', '189.217.45.73'],
    # ['/index.php?option=com_phocagallery&view=category&id=7806&Itemid=53 ', '404', '1417', '189.217.45.73'],
    # ['/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%289168%3D4696%29%20THEN%209168%20ELSE%209168%2A%28SELECT%209168%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%29%20END%29%29&Itemid=53 ', '404', '1417', '189.217.45.73'],
    # ['/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%281753%3D1753%29%20THEN%201753%20ELSE%201753%2A%28SELECT%201753%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%29%20END%29%29&Itemid=53 ', '404', '1417', '189.217.45.73'],
    # ['/index.php?option=com_easyblog&view=dashboard&layout=write ', '404', '1397', '104.129.9.248']]


# 5) Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой:
#   должен выводиться ip адрес
#   должно выводиться количество запросов
def top_5_users_5xx_requests():
    result_data = []
    with open(os.path.abspath('access.log'), 'r', encoding='utf-8') as logs:
        for line in logs.readlines():
            data = re.search(lineformat, line)
            datadict = data.groupdict()
            pattern = re.compile(r'5..')
            if data and pattern.search(datadict["statuscode"]):
                ip = datadict["ipaddress"]
                result_data.append(ip)

    counts = dict()
    for i in result_data:
        counts[i] = counts.get(i, 0) + 1
    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
    return {"Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой":
          list(sorted_counts.items())[:5]}
    # [('189.217.45.73', 225), ('82.193.127.15', 4), ('91.210.145.36', 3), ('194.87.237.6', 2), ('198.38.94.207', 2)]


result = [number_of_requests(),
          number_of_requests_by_method(),
          top_10_frequent_requests(),
          top_5_largest_4xx_requests(),
          top_5_users_5xx_requests()]

if '--json' in sys.argv:
    with open('result.json', 'w') as file:
        json.dump(result, file, indent=3, ensure_ascii=False)
else:
    print(result)


