from geopy.geocoders import Nominatim # coordinate library
geolocator = Nominatim(user_agent="test")

# fill var for tests
city = 'Pordenone'
country = 'Italy'

loc = city + ', ' + country
print('loc: ' + loc)

coordinates = geolocator.geocode(loc)
print('Result: ' + str(coordinates))
