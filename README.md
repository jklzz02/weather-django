# Weather Application

In this project i aim to create a Web application who can provide current and forecast weather info through an **API** from [Open Weather](https://openweathermap.org/)

## Services

There are a series of custom functions and a [Weather](main/main/services/Weather.py) **API**  made for this project in [services.py](/main/main/services/).
All of them are documented with comments in the code.

### Weather API

In the project there's a [Weather](main/main/services/Weather.py) **API** to make requests and retrieve various weather information.

* `current(city, lang) -> dict|bool`: makes an **API** call to [Open Weather](https://openweathermap.org/) retrieving the current weather conditions, of the requested city in the requested language.

```python
weather_service = Weather()
city_info = weather_service.current('New York', 'eng')
```

* `forecast(lat, lon, lang) -> dict|bool`: Similar to `current`, this function makes a request to retrieve a daily forecast for the upcoming week, and an hourly forecast for the current day.

```python
weather_service = Weather()
city_info = weather_service.forecast(you_city_latitude, your_city_longitude, 'eng')
```

* `air_condition(lat, lon, lang)  -> dict|bool`: makes an **API** call using the google [Air Quality API](https://developers.google.com/maps/documentation/air-quality/overview) to retrieve the current and general air conditions of the zone. The call requires a `KEY` provided by google, and returns in `json` format the local aqi, the dominant pollutant and it's concentration. The call is made via the library requests with `POST` method. The function requires the latitude and longitude of the area to check, the api key and the language in which you desire getting the information

```python
weather_service = Weather()
city_info = weather_service.air_condition(you_city_latitude, your_city_longitude, 'eng')
```

#### Google Maps Embed API

In this project we also use an API provided by [Google](https://developers.google.com/maps/documentation/embed/get-started) to embed a map of the place for which we are providing the weather information. The key can be retrieved with the `map() -> str` method of [Weather](main/main/services/Weather.py).

```django
https://www.google.com/maps/embed/v1/place?key={{developer key}}&q={{city name}}
```

to make the call, you need to provide the name of the place to query, and a developer key directly provided by google. You can review the API documentation [here](https://developers.google.com/maps/documentation/embed/get-started)

### Functions

Utility functions in [funcs](main/main/services/funcs.py)

* `unix_timestamp_converter(timestamp, date_format)`: Given a Unix timestamp, returns a human-readable date. The date format attribute is required to make the function reusable.

* `get_user_info()`: Using the `geocoder` library, this function returns the user's country code based on their IP address and their Language and Timezone. This function is called in the [Settings](main/main/settings.py) **Django** file to change default Timezone and Language for the application

* `translate(transalator, text, lang)`: requires a lang parameter, likely obtained via `get_user_info()`, and returns a translated version of a string in the specified language.

* `make_link(match)`: to be called with the `re.sub` method of a `regex object`. It takes a match object as input and returns the match wrapped in an `<a>` tag with the same match as the `href` attribute. converts plain text into clickable links.

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
