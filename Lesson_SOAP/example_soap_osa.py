import osa


def add(a, b):
    client = osa.Client('http://www.dneonline.com/calculator.asmx?WSDL')
    return client.service.Add(a, b)


print(add(3, 9))
