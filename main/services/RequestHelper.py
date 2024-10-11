from requests import get, post, RequestException
from urllib.parse import urlencode

class   RequestHelper:

    def build_url(self, base:str, endpoint: str, params: dict) -> str:

        return f"{base}{endpoint}?{urlencode(params)}"
    
    def get(self, url:str) -> dict|bool:

        try:
            response = get(url)
            response.raise_for_status()
            return response.json()
        
        except RequestException as e:
            status_code = e.response.status_code if e.response.status_code else "Uknown"
            print(f"GET request failed with status code: {status_code}")
            return False

    def post(self, url:str, headers:dict, data:dict) -> dict|bool:

        try:
            response = post(url, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        
        except RequestException as e:
            status_code = e.response.status_code if e.response.status_code else "Uknown"
            print(f"POST request failed with status code: {status_code}")
            return False