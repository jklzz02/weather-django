# Weather Application

In this project i aim to create a Web application who can provide current and forecast weather info through an **API** from [Open Weather](https://openweathermap.org/)

## Services

There are a series of [utility](main/services/utilities.py) functions and a [weather](main/services/weather.py) **module**  made for this project in the [services](/main/services/) package.
All of them are documented with comments in the code.

### Weather API

In the project there's a [weather](main/services/weather.py) **module** to make requests and retrieve various weather information. All of the functions use `@lru_cache` from [functools](https://docs.python.org/3/library/functools.html) for better performance and to litimate API calls usage. The API keys are loaded using Django's [environ library](https://pypi.org/project/django-environ/). The keys are then stored in pseudo private variable to make them accessible to the functions without needing to pass them as parameters, that's why they're optional parameters. The `lang` parameter has a default value retrieved from the [settings](main/main/settings.py) `LANGUAGE_CODE`, it can be specified a different languange as a parameter.

* `get_current_weather(city:str, lang:str=lang) -> Optional[dict]`: makes an **API** call to [Open Weather](https://openweathermap.org/) retrieving the current weather conditions, of the requested city, in the requested language.

```python
weather_info = get_current_weather("milan")
```

* `get_forecast_weather(lat:str, lon:str, lang:str=lang) -> Optional[dict]`: Similar to `current`, this function makes a request to retrieve a daily forecast for the upcoming week, and an hourly forecast for the current day.

```python
forecast_weather_info = get_forecast_weather(your_city_latitude, your_city_longitude)
```

* `get_air_condition(lat, lon, lang)  -> Optional[dict]`: makes an **API** call using the google [Air Quality API](https://developers.google.com/maps/documentation/air-quality/overview) to retrieve the current and general air conditions of the zone. The call requires a `KEY` provided by google, and returns in `json` format the local aqi, the dominant pollutant and it's concentration. The call is made via the library requests with `POST` method. The function requires the latitude and longitude of the area to check and the language in which you desire getting the information

```python
air_conditions = get_air_conditions(your_city_latitude, you_city_longitude)

```

#### Google Maps Embed API

In this project we also use an API provided by [Google](https://developers.google.com/maps/documentation/embed/get-started) to embed a map of the place for which we are providing the weather information. The key is retrieved from the [settings](main/main/settings.py).

```django
https://www.google.com/maps/embed/v1/place?key={{developer key}}&q={{city name}}
```

to make the call, you need to provide the name of the place to query, and a developer key directly provided by google. You can review the API documentation [here](https://developers.google.com/maps/documentation/embed/get-started)

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

* `translate(text:str, lang:str=lang)`: requires a lang parameter, likely obtained via `get_user_info()`, and returns a translated version of a string in the specified language, the default value of `lang` is retrieved from the [settings](main/main/settings.py), the function uses the Translator object from [googletrans](https://pypi.org/project/googletrans/).

```python
# will translate the string in the language retrieved from the settings
translated_text = translate("Hello, World")

# will translate the string in spanish, regardless of the languange in the settings
translated_text = translate("Hello, World", "es")

```

* `make_link(match)`: to be called with the `re.sub` method of a `regex object`. It takes a match object as input and returns the match wrapped in an `<a>` tag with the same match as the `href` attribute. converts plain text into clickable links.

```python
alert = alertRegex.sub(make_link, alert)
```

#### Requests Helpers

In utilities there are also 2 helpers to make `GET`and `POST` requests using the [requests](https://pypi.org/project/requests/) lybrary.

* `get_request(url:str, params:dict) -> Optional[dict]`
* `post_request(url:str, params:dict, json) -> Optional[dict]`
Thery're used by the [weather](main/services/weather.py) functions to make the calls, and upon failure return `None`

## Libraries & Dependencies

`python3.11`or later and it's relative package manager are required.

In the [Requirements](requirements.txt) Document, you can find every needed library which can be installed using this simple command:

```bash
 pip install -r requirements.txt
```

This command will read line by line the [Requirements](requirements.txt) document
passing every package through `pip` installing them.

## How to Contribute

This application is built using **django**, a **python** framework specifically meant for web development.
To contribute you should have a basic understanding of **django** you can consult official documentation [here](https://docs.djangoproject.com/en/5.0/contents/).

You can download all the source code directly from **GitHub** and start contributing via a `Pull Request`.
