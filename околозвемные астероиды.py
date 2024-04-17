from requests import get
import json
api_key='iuCdE8es7d2DuclaVnHviPHbWC8fRT21VfnAykJT'
start_date='2024-02-09'
end_date='2024-02-10'
url=f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}'
file=get(url).json()
# print(type(file))
# print(json.dumps(file,indent=4))
print(file.keys())
#print(file['links']) - не надо
#print(file['element_count']) - кол-во выведенных элементов

kkeys=['links', 'id', 'neo_reference_id', 'name', 'nasa_jpl_url', 'absolute_magnitude_h',
       'estimated_diameter', 'is_potentially_hazardous_asteroid', 'close_approach_data',
       'is_sentry_object']

for date in file['near_earth_objects']:
    print(file['near_earth_objects'][date][0][f'{kkeys[3]}']) #последнее значение - конечный ключ

