import osa


def convert_temp_2_celsius(temp_fahrenheit):
    client = osa.Client("http://www.webservicex.net/ConvertTemperature.asmx?WSDL")
    return client.service.ConvertTemp(temp_fahrenheit, 'degreeFahrenheit', 'degreeCelsius')


with open('temps.txt', 'r') as f:
    data = f.read()
    data_list = data.split('\n')
    temp_list = [int(i.replace(' F', '')) for i in data_list]

average_temp_f = sum(temp_list) / len(temp_list)
print('{} F = {} C'.format(average_temp_f, convert_temp_2_celsius(average_temp_f)))
