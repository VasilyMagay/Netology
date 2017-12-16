import osa


def convert_mile_2_km(mile):
    client = osa.Client("http://www.webservicex.net/length.asmx?WSDL")
    return client.service.ChangeLengthUnit(mile, 'Miles', 'Kilometers')


with open('travel.txt', 'r') as f:
    data = f.read()
    data_list = data.split('\n')
    travel_list = [i.split(' ') for i in data_list]
    miles = float(0)
    for i in travel_list:
        miles += float(i[1].replace(',', ''))

print('Длина пути {} миль или {} километров'.format(miles, '%.2f' % convert_mile_2_km(miles)))
