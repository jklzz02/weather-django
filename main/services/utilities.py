from datetime import datetime
from django.conf import settings
from googletrans import Translator
from requests import get, post, RequestException
from typing import Optional
import re

# helpers to make POST and GET requests, for API calls.

def get_request(url:str, params:dict) -> Optional[dict]:
    try:
        response = get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    except RequestException as e:
        code = e.response.status_code if e.response.status_code else "Unknown"
        print(f'GET request failed with status code {code}')

def post_request(url:str, params:dict, json) -> Optional[dict]:
    try:
        response = post(url, params=params, json=json)
        response.raise_for_status()
        return response.json()

    except RequestException as e:
        code = e.response.status_code if e.response.status_code else "Unknown"
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
takes as arguments a translator object from googletrans, 
the text to be translated and the lang for which you want the text to be returned in
you can get the user language dinamically by simly importing it from the settings file
'''
def translate(text:str, lang:str=settings.USER_INFO['language'], translator:Translator=Translator()) -> str:
     translation = translator.translate(text, dest=lang)
     return translation.text