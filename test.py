import requests



payload = {'name': 'John', 'age': 25}
r = requests.post('https://httpbin.org/post', data = payload)

res_json = r.json()


print(res_json)