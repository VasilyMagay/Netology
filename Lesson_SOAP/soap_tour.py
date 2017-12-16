import osa


def cross_rate(base_currency, to_currency):
    client = osa.Client("http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL")
    return client.service.RateNum(baseCurrency=base_currency.upper(), toCurrency=to_currency.upper(), rounding='false')


with open('currencies.txt', 'r') as f:
    data = f.read()
    data_list = data.split('\n')
    travel_list = [i.split(' ') for i in data_list]

sum = 0
for travel in travel_list:
    sum += int(travel[1]) * cross_rate(travel[2], 'rub')

print('Стоимость путешествия в рублях: {}'.format('%d'%sum))
