from requests import get
import json

#список и описание астероидов, пролетавших в указанный период
api_key='iuCdE8es7d2DuclaVnHviPHbWC8fRT21VfnAykJT'
start_date='2024-02-09'
end_date='2024-02-10'
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
for num in range(len(file)):
    print(file[num]['title'])


