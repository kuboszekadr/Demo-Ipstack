import json
import requests


class Ipstack():
    def __init__(self, secret_key: str):
        """
        Creates new class member of Ipstack

        @param: secret_key- can be obtained from https://ipstack.com/
        """
        self.__secret_key = secret_key

    def fetch_data_about_url(self, url: str) -> json:
        """
        Downloads data from Ipstack about provided webpage

        @param: url - IP address or URL of the webpage
        @returns: json
        """
        url_template = 'http://api.ipstack.com/{url}?access_key={secret_key}'
        response = requests.get(url_template.format(
            url=url,
            secret_key=self.__secret_key))
        return json.loads(response.text)
