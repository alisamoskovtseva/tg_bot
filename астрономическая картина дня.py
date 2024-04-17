from requests import get
import json
from PIL import Image
from urllib.request import urlopen

#список и описание астероидов, пролетавших в указанный период
api_key='iuCdE8es7d2DuclaVnHviPHbWC8fRT21VfnAykJT'
start_date='2024-01-11'
end_date='2024-01-16'
url=f'https://api.nasa.gov/planetary/apod?start_date={start_date}&end_date={end_date}&api_key={api_key}'
file=get(url).json()
# print(type(file))
# print(json.dumps(file,indent=4))
# print(*file)
kkeys=['copyright', 'date', 'explanation', 'hdurl', 'media_type',
       'service_version', 'title', 'url'] # 'copyright' - не обязательно

# 'copyright' - автор
# 'date' - дата
# 'explanation' - объяснение
# 'hdurl' - фотка (качество хуже)
# 'media_type' - фото/видео
# 'service_version' - хз
# 'title' - название
# 'url' - фотка
print(file)
#код снизу показывает картинки

if len(file)!=0:
    if len(file)!=1:
        for num in range(len(file)):
            print(file[num])
            if file[num]['url']:

                url = file[num]['url']

                image = Image.open(urlopen(url))
                image.show()
    else:
        print(file)
else:
    print('niche')
