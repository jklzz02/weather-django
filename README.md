# Weather Application
In this project i aim to create a Web application who can provide current and forecast weather infos through a `API` from [Open Weather](https://openweathermap.org/)

## API Call Example
```
def get_weather(city, key, lang):
        request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={key}&q={city}&units=metric&lang={lang}'
        weather_data = requests.get(request_url).json()
        return weather_data

```
In the provided code Snippet you can see how the API call is made to get current weather informations. 

**3 parameters are required**:
* `city` the name of the city to be geocoded 
* `key` Developer key from [Open Weather](https://openweathermap.org/)
* `lang` the language that you want the response with the infos to be

## Services

There are a series of custom function made for this project in the [services.py](/main/main/services.py).
All of them are documented with comments in the code.

**Services**
`get_weather()`
* makes an API request to retrieve current weather conditions
`get_forecast_weather()`
* makes an API request to retrieve daily forecast conditions for a week
`unix_converter()`
* given a `unix timestamp` date return a human readable date
`get_country()`
* using the `geocoder` library, returns user country code
`translate()`
* requires a `lang` parameter likely obtained via `get_country()` and returns a translated version of a string in the specified language
`make_link()`
* A function to be called in the `re.sub` method of a `regex` object returns the match wrapped in an `<a>` tag with the same match as `href` attribute.

## Libraries & Dependencies

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
