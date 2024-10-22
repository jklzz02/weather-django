from asgiref.sync import sync_to_async
from datetime import datetime
from cities.models import City
from fuzzywuzzy import process
from logging import getLogger
from typing import Optional, Dict, Callable
import aiohttp
import re

__logger = getLogger(__name__)

# helper to make asynchronous requests, for API calls.
async def request(url: str, params: Optional[dict]=None, json:Optional[dict]=None, method:str="GET", timeout :int=10) -> Optional[dict]:

    try:
        async with aiohttp.ClientSession() as session:

            method_map: Dict[str, Callable] = {
                'GET': session.get,
                'POST': session.post,
                'PUT': session.put,
                'DELETE': session.delete,
            }

            request = method_map.get(method.upper())

            if request is None:
                __logger.error(f"Unsupported HTTP method {method}")
                return None
            
            async with request(url, params=params, json=json, timeout=timeout) as response:
                response.raise_for_status()
                return await response.json()
            
    except aiohttp.ClientResponseError as e:
        __logger.warning(f"GET request failed with status {e.status}: {e.message}, URL: {url}")

    except aiohttp.ClientConnectorError as e:
        __logger.error(f"GET request connection error: {e}, URL: {url}")

    except Exception as e:
        __logger.exception(f"GET request encountered an unexpected error: {e}, URL: {url}")

    return None

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
function to get city suggestions based on a user input resulted in a not found error
'''
@sync_to_async
def suggest_city(user_input :str) -> Optional[dict]:
    if not user_input or len(user_input) < 2:
        return []

    cities = City.objects.filter(name__istartswith=user_input[:1]).values_list('name', flat=True)

    if not cities:
        return []

    suggestions = process.extract(user_input, cities, limit=5)
    return [s[0] for s in suggestions]