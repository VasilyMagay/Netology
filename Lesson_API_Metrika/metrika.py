from pprint import pprint
from urllib.parse import urlencode
import requests

# Формирование ссылки для получения токена

# APP_ID = 'c0e0188725484e829f2341c5ece691c1'
# AUTH_URL = 'https://oauth.yandex.ru/authorize'
#
# data = {
#     'response_type': 'token',
#     'client_id': APP_ID
# }
#
# url = '?'.join((AUTH_URL, urlencode(data)))
#
# print(url)
#
# exit()

# Получение списка доступных счетчиков метрики

my_token = 'AQAAAAABVf_TAAS5A3L52dmzNU-Ttymckz_pSG0'


class YaBase:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Authorization': 'OAuth {}'.format(self.token)}


class YaUser(YaBase):

    def get_counters(self):  # Список доступных счетчиков метрики
        response = requests.get('https://api-metrika.yandex.ru/management/v1/counters',
                                headers=self.get_headers())
        # pprint(response.json())
        return [c['id'] for c in response.json()['counters']]


class Counter(YaBase):

    def __init__(self, token, counter_id):
        self.counter_id = counter_id
        super().__init__(token)

    def get_info(self):  # Информация о счетчике
        response = requests.get('https://api-metrika.yandex.ru/management/v1/counter/{}'.format(self.counter_id),
                                headers=self.get_headers())
        return response.json()

    def get_metrik_info(self, metrics):
        params = {
            'id': self.counter_id,
            'metrics': metrics
        }
        response = requests.get(
            'https://api-metrika.yandex.ru/stat/v1/data',
            params,
            headers=self.get_headers()
        )
        return response.json()

    @property
    def visits(self):  # Кол-во посетителей
        return int(self.get_metrik_info('ym:s:visits')['totals'][0])

    @property
    def new_users(self):  # Количество новых посетителей
        return int(self.get_metrik_info('ym:s:newUsers')['totals'][0])

    @property
    def pageviews(self):  # Число просмотров страниц на сайте за отчетный период
        return int(self.get_metrik_info('ym:s:pageviews')['totals'][0])


class YMetrik(Counter):

    response_json = {}

    def __init__(self, token, counter_id, metrics):
        super().__init__(token, counter_id)
        self.metrics = metrics
        self.get_metrik_info()

    def get_metrik_info(self):
        params = {
            'id': self.counter_id,
            'metrics': self.metrics
        }
        response = requests.get(
            'https://api-metrika.yandex.ru/stat/v1/data',
            params,
            headers=self.get_headers()
        )
        self.response_json = response.json()

    @property
    def totals(self):
        return int(self.response_json['totals'][0])


ya_user1 = YaUser(my_token)

for counter_id in ya_user1.get_counters():
    counter = Counter(my_token, counter_id)
    # pprint(counter.get_info())
    metrik1 = YMetrik(my_token, counter_id, 'ym:s:visits')
    metrik2 = YMetrik(my_token, counter_id, 'ym:s:newUsers')
    metrik3 = YMetrik(my_token, counter_id, 'ym:s:pageviews')
    print('Счетчик {} ------------------'.format(counter_id))
    pprint('Кол-во посетителей: {}'.format(metrik1.totals))
    pprint('Кол-во новых посетителей: {}'.format(metrik2.totals))
    pprint('Число просмотров страниц: {}'.format(metrik3.totals))
