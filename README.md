# Weather Application
In this project i aim to create a Web application who can provide current and forecast weather infos through a `API` from [Open Weather](https://openweathermap.org/)

## API Call Example
```
def get_weather(city, key, lang):
        request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={key}&q={city}&units=metric&lang={lang}'
        weather_data = requests.get(request_url).json()
        return weather_data

```
In the provided code Snippet youn can see how the API call is made to get current weather informations. 

**3 parameters are required**:
* `city` the name of the city to be geocoded 
* `key` Developer key from [Open Weather](https://openweathermap.org/)
* `lang` the language that you want the response with the infos to be

## Services

There are a series of custom function made for this project in the [services.py](/main/main/services.py).
All of them are documented with comments in the code.

**Services**

* `get_weather(city, key, lang)`: makes an `API` request to retrieve the current weather conditions.

* `get_forecast_weather(lat, lon, key, lang)`: Similar to `get_weather()`, this function makes an `API` request to retrieve a daily forecast for the upcoming week.

* `unix_converter(timestamp)`: Given a Unix timestamp, returns a human-readable date.

* `get_user_info()`: Using the `geocoder` library, this function returns the user's country code based on their IP address and their Languange and Timezone. This function is called in the [Settings](main/main/settings.py) **Django** file to change default Timezone and Language for the application

* `translate(transalator, text, lang)`: requires a lang parameter, likely obtained via `get_user_info()`, and returns a translated version of a string in the specified language.

* `make_link(match)`: to be called with the `re.sub` method of a `regex object`. It takes a match object as input and returns the match wrapped in an `<a> ` tag with the same match as the `href` attribute. converts plain text into clickable links.

## Libraries & Dependancies

in the [Requirements](requirements.txt) Document, you can find every needed library which can be installed using this simple command:

**Linux & MacOS**
```
cat requirements.txt | xargs -n 1 pip install -U

```
**Windows (PowerShell)**

```
Get-Content requirements.txt | ForEach-Object {pip install -U $_}

```

This command will read line by line the [Requirements](requirements.txt) document
passing every package through `pip install -U` wich is the **python** package manager.

## How to Contribute

This application is built using **django**, a **python** framework specifically meant for web development.
To contribute you should have a basic understanding of **django** you can consult official documentation [here](https://docs.djangoproject.com/en/5.0/contents/).

You can download all the source code directly from **GitHub** and start contributing via a `Pull Request`.
