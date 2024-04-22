# Weather Application
In this project i aim to create a Web application who can provide current and forecast weather infos through a `Rest API` from [Open Weather](https://openweathermap.org/)

## API Call Example
```
def get_weather(city, key, lang):
        request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={key}&q={city}&units=metric&lang={lang}'
        weather_data = requests.get(request_url).json()
        return weather_data

```
In the provided code Snippet youn can see how the API call is made to get current weather informations. 

3 parameters are required `1 city` the name of the city to be geocoded `2 key` Developer key from [Open Weather](https://openweathermap.org/) and `3 lang` the language that you want the response with the infos to be
