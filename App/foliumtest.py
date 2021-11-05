import folium
from IPython.display import display

lat_lst = [31.65,38.99,45.30]
lon_lst = [-104,-105.60,-108.4]

map = folium.Map(location=[35, -104], min_lat=31.33, max_lat=37.00,min_lon=-109.05,max_lon=-103.00)

for lat,lon in zip(lat_lst,lon_lst):

    loc = [lat,lon]

    folium.Marker(location=loc).add_to(map)

display(map)

