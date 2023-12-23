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
                f'https://api.progressiveai.org/v1/{self.model}/chat', params=params)
            # This will raise an HTTPError if the status code is 4XX or 5XX
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
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            print(f"Status code: {response.status_code}")
            print(f"Response content: {response.content}")
            return None
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None
        except Exception as e:
            print(f"Status code: {response.status_code}")
            print(f"Response content: {response.content}")
            return None

        if 'error' in data:
            raise APIError(data['error'])
        return data['response']
