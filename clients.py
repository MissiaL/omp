import requests


class ClientSub:
    def __init__(self):
        self.url = 'http://localhost:4000'

    def create(self, params):
        url = f'{self.url}/subscriptions'
        response = requests.post(url, json=params)
        response.raise_for_status()
        return response.json()

    def get(self):
        url = f'{self.url}/subscriptions'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def delete(self):
        url = f'{self.url}/subscriptions'
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()