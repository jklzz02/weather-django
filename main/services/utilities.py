from datetime import datetime
from django.conf import settings
from googletrans import Translator
import re

# function to call in re.sub
def make_link(match:re.Match[str]) -> str:
    url = match.group(0)
    return f'<a href="{url}" target="_blank">{url}</a>'

'''
converts a unix timestamp in the desired human-readable format
it takes as an argument the timestamp to be converted and the format you want it to
be returned in. You can simply pass in date_format="date".
'''
def unix_timestamp_converter(timestamp:int, date_format:str='') -> str:
     dt_object = datetime.fromtimestamp(timestamp)

     if date_format == "date":
          readable_date = dt_object.strftime("%A %d/%m/%Y")
     else:
         readable_date = dt_object.strftime("%H:%M")

     return readable_date

'''
takes as arguments a translator object from googletrans, 
the text to be translated and the lang for which you want the text to be returned in
you can get the user language dinamically by simly importing it from the settings file
'''
def translate(translator:Translator, text:str, lang:str=settings.USER_INFO['language']) -> str:
     translation = translator.translate(text, dest=lang)
     return translation.text