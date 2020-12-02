import requests
import configparser
import json

url_template = 'http://api.ipstack.com/{url}?access_key={secret_key}'
url = 'wp.pl'

# read config file
config = configparser.ConfigParser()
config.read('config.ini')

response = requests.get(url_template.format(
    url=url,
    secret_key=config['SECRET']['secret_key'])
)
response_json = json.loads(response.text)

fields = eval(config['DATA']['fields'])
data = {field: response_json[field] for field in fields}
