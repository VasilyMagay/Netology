import requests

# author = requests.__author__
print(requests.get('http://httpbin.org/user-agent').text)