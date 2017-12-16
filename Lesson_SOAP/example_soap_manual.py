import requests
from xml.etree.cElementTree import fromstring


def add(a, b):
    response = requests.post(
        'http://www.dneonline.com/calculator.asmx',
        headers={
            'Content-Type': 'text/xml; charset=utf-8'
        },
        data='''<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                  xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                  <soap:Body>
                    <Add xmlns="http://tempuri.org/">
                      <intA>''' + str(a) + '''</intA>
                      <intB>''' + str(b) + '''</intB>
                    </Add>
                  </soap:Body>
                </soap:Envelope>
            '''
    )

    result = fromstring(response.text)
    return int(result[0][0][0].text)


print(add(5, 9))
