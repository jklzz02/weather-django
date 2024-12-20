# Weather Application

This project is a Web application that provides current and forecast weather info through an **API** from [Open Weather](https://openweathermap.org/)

## Services

There are a series of [utility](main/services/utilities.py) functions and a [weather](main/services/weather.py) module  made for this project in the [services](/main/services/) package.
All of them are documented with comments in the code.

### Weather API

In the project there's a [weather](main/services/weather.py) module with functions to make asynchronous requests and retrieve various weather information. All of the functions use `@cached` from [aiocache](https://pypi.org/project/aiocache/) for better performance and to litimate API call usage. The API keys are loaded using Django's [environ library](https://pypi.org/project/django-environ/). The keys are stored in pseudo private variables. The `lang` parameter has a default value retrieved from the [settings](main/main/settings.py) `LANGUAGE_CODE`, it can be specified a different languange as a parameter.

* `get_weather(city: str="", lat: str="", lon: str="", mode: str="current", lang: str=lang) -> Optional[dict]`: makes an **API** call to [Open Weather](https://openweathermap.org/) retrieving the current or forecast weather conditions, of the requested city, in the requested language.

```python
# Retrieves current weather conditions
weather_info = get_weather("milan") 

# Retrievies one week daily, and 24 hours, hourly forecast
forecast_info = get_weather("milan", mode="forecast") 
```

* `get_air_condition(lat, lon, lang)  -> Optional[dict]`: makes an **API** call using the google [Air Quality API](https://developers.google.com/maps/documentation/air-quality/overview) to retrieve the current and general air conditions of the zone. The call requires a `KEY` provided by google, and returns in `json` format the local aqi, the dominant pollutant and its concentration. The call is made using the request helper in the [utilities](/services/utilities.py) module.

```python
air_conditions = get_air_conditions(your_city_latitude, you_city_longitude)

```

#### Google Maps Embed API

This project uses an API provided by [Google](https://developers.google.com/maps/documentation/embed/get-started) to embed a map of the requested city. The key is retrieved from the [settings](main/main/settings.py).

```django
https://www.google.com/maps/embed/v1/place?key={{developer key}}&q={{city name}}
```

to make the call, is required to provide the name of the place and a developer key provided by google. Review the API documentation [here](https://developers.google.com/maps/documentation/embed/get-started)

### Functions

#### Utility functions in [utilities.py](main/services/utilities.py)

* `unix_timestamp_formatter(timestamp:int, date_format:str)`: Given a Unix timestamp, returns a human-readable date. The date format attribute is required to make the function reusable.

```python
readable_date = unix_timestamp_formatter(your_timestamp, date_format="%A %d/%m/%Y")
```

* `get_user_info()`: Using the `geocoder` library, this function returns the user's country code based on their IP address and their Language and Timezone. This function is called in the [Settings](main/main/settings.py) **Django** file to change default Timezone and Language for the application

```python
user_info = get_user_info()
```

* `make_link(match)`: To be called with the `re.sub` method of a `regex object`. It takes a match object as input and returns the match wrapped in an `<a>` tag with the same match as the `href` attribute. converts plain text into clickable links.

```python
alert = alertRegex.sub(make_link, alert)
```

* `suggest_city(user_input :str, matches_num :int=5) -> list[str]`: Receives a user input and with a score system returns the most similar results from the cities database table, the number of matches can be specified as a parameter.

#### Requests Helper

In utilities there are also 2 helpers to make **asynchronous** requests using the [aiohttp](https://docs.aiohttp.org/en/stable/) library.

* `get_request(url:str, params:dict) -> Optional[dict]`
* `post_request(url:str, params:dict, json) -> Optional[dict]`
Thery're used by the [weather](main/services/weather.py) functions to make calls, and upon failure returns `None`

## Libraries & Dependencies

`python3.11` or later and it's relative package manager are required.

In the [Requirements](requirements.txt) Document is listed every needed library.

Run this command to install needed libraries:

```bash
 pip install -r requirements.txt
```

This command will read line by line the [Requirements](requirements.txt) document
passing every package through `pip` installing them.

## How to Contribute

This application is built using **django**, a **python** framework specifically meant for web development.
To contribute is required a basic understanding of **django**, consult official documentation [here](https://docs.djangoproject.com/en/5.0/contents/).
