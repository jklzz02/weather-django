from datetime import datetime
from cities.models import City
from functools import lru_cache
from logging import getLogger
from typing import Optional, Dict, Callable
import aiohttp
import re

__logger = getLogger(__name__)

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

def make_link(match:re.Match[str]) -> str:
    url = match.group(0)
    return f'<a href="{url}" target="_blank">{url}</a>'

def unix_timestamp_converter(timestamp:int, date_format:str) -> str:
     dt_object = datetime.fromtimestamp(timestamp)
     return dt_object.strftime(date_format)

@lru_cache(maxsize=128)
def suggest_city(user_input :str, matches_num :int=5) -> list[str]:

    if not user_input:
        return []
    
    cities = list(City.objects.values_list('name', flat=True))

    matches = []
    input_len = len(user_input)
    input_lower = user_input.lower()
    seen = set()

    for city in cities:
        points = 0
        city_lower = city.lower()

        if input_lower in city_lower:
            points += input_len + 2

        if city_lower.startswith(user_input[:1]):
            points += 2

        for i, letter in enumerate(input_lower):
            if letter in city_lower:
                points += 1
            
            if i == city.find(letter):
                points += 2

        if points > 0 and city not in seen:
            matches.append({"match" : city, "score" : points})
            seen.add(city)

    
    matches = sorted(matches, key=lambda x: x['score'], reverse=True)[:matches_num]
    return [city['match'] for city in matches]