import geocoder
import csv

place_list = ['ドイツ', 'スロバキア', 'ポーランド']
for i in place_list:
  ret = geocoder.osm(i, timeout=5.0)
  print(i, ret.latlng)


