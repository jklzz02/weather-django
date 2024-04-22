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
