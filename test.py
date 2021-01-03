import geocoder
import requests
import json
import pandas as pd

df = pd.read_excel('Locations.xlsx')

locations = df['Places'].tolist()
g = geocoder.mapquest(location=locations, method='batch', key='j0paRAfw1XI6k0MpkGG1okNyVPQoqjfR')
latitudes = []
longitudes = []

for result in g:
    latitudes.append(result.lat)
    longitudes.append(result.lng)

df['Latitude'] = latitudes
df['Longitude'] = longitudes

print(df)

df.to_excel('Output.xlsx', index=False, header=True)




# print(g.json)
# print(g.json['lat'])
# print(g.json['lng']) 






# parameters = {
#     "key": "j0paRAfw1XI6k0MpkGG1okNyVPQoqjfR",
#     "location": 'Kakching, Manipur, India, 795103'
# }

# response = requests.get("http://www.mapquestapi.com/geocoding/v1/address", params=parameters)
# print(response)
# data = response.text
# dataJ = json.loads(data)['results']
# lat = (dataJ[0]['locations'][0]['latLng']['lat'])
# lng = (dataJ[0]['locations'][0]['latLng']['lng'])

# print(lat, lng)