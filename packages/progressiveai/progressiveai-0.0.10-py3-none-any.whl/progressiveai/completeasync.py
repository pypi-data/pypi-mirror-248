import aiohttp
import asyncio
import json
from .exceptions import APIError


class CompleteAsync:
    def __init__(self, api_key, text, model):
        self.api_key = api_key
        self.text = text
        self.model = model

    async def get_response(self):
        params = {
            'api_key': self.api_key,
            'prompt': self.text
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f'https://api.progressiveai.org/v1/{self.model}/complete', params=params, timeout=95) as response:
                    response.raise_for_status()
                    data = await response.json()
        except asyncio.TimeoutError as toe:
            print("The request timed out. Please try again later.")
            return None
        except aiohttp.ServerDisconnectedError as sde:
            print("The Server disconnected. Please try again later.")
            return None
        except aiohttp.ClientResponseError as cre:
            if cre.status == 404:
                print("The AI Model is unavailable or doesn't exist at all!")
            elif cre.status == 524:  # Cloudflare Timeout Error
                print("The request timed out. Please try again later.")
            elif cre.status == 502:
                print("Oops! The Server failed to return a response!")
            else:
                print("Client response error: ", cre)
            return None
        except aiohttp.ClientPayloadError as cpe:
            print(f"Client payload error: {cpe}")
            return None
        except json.JSONDecodeError as jde:
            print(f"JSON decoding error: {jde}")
            return None
        except aiohttp.ClientError as ce:
            print(f"Aiohttp client error: {ce}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

        # Use get() to avoid KeyError if 'response' is not present in data
        return data.get('response')
