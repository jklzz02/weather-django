from datetime import datetime
from django.conf import settings
from typing import Optional
import aiohttp
import re

# helpers to make asyncronous POST and GET requests, for API calls.

async def get_request(url: str, params: dict) -> Optional[dict]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientResponseError as e:
        code = e.status if e.status else "Unknown"
        print(f'GET request failed with status code {code}')

async def post_request(url: str, params: dict, json: dict) -> Optional[dict]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params, json=json) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientResponseError as e:
        code = e.status if e.status else "Unknown"
        print(f'POST request failed with status code {code}')

# function to call in re.sub
def make_link(match:re.Match[str]) -> str:
    url = match.group(0)
    return f'<a href="{url}" target="_blank">{url}</a>'

'''
converts a unix timestamp in the desired human-readable format
it takes as an argument the timestamp to be converted and 
the format you want it to be returned in, which get passed to the method strftime.
'''
def unix_timestamp_converter(timestamp:int, date_format:str) -> str:
     dt_object = datetime.fromtimestamp(timestamp)
     return dt_object.strftime(date_format)

'''

google trans library doesn't work properly

takes as arguments a translator object from googletrans, 
the text to be translated and the lang for which you want the text to be returned in
you can get the user language dinamically by simly importing it from the settings file
'''
# @lru_cache(maxsize=1024)
# def translate(text:str, lang:str=settings.USER_INFO['language']) -> str:
#      translation = Translator().translate(text, dest=lang)
#      return translation.text