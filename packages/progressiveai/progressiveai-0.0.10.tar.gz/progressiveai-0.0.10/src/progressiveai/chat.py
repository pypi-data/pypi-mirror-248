import json
import requests
from .exceptions import APIError


class Chat:
    def __init__(self, api_key, text, model):
        self.api_key = api_key
        self.text = text
        self.model = model
        self.session = requests.Session()

    def get_response(self):
        params = {
            'api_key': self.api_key,
            'prompt': self.text
        }
        try:
            response = self.session.get(
                f'https://api.progressiveai.org/v1/{self.model}/chat', params=params, timeout=95)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as errh:
            if response.status_code == 404:
                print("The AI Model is unavailable or doesn't exist at all!")
            elif response.status_code == 524:  # Cloudflare Timeout Error
                print("The request timed out. Please try again later.")
            elif response.status_code == 502:
                print("Oops! The Server failed to return a response!")
            else:
                print("HTTP Error: ", errh)
            return None
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
            return None
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
            return None
        except requests.exceptions.RequestException as err:
            print(f"Something went wrong with the request: {err}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        if 'error' in data:
            raise APIError(data['error'])
        return data['response']
