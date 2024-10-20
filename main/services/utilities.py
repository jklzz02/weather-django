from datetime import datetime
from logging import getLogger
from typing import Optional, Dict, Callable
import aiohttp
import re

__logger = getLogger(__name__)

# helper to make asyncronous requests, for API calls.
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