import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime as dt
import timeit
from geopy.geocoders import Nominatim # coordinate library
import re # regex library

geolocator = Nominatim(user_agent="test")

while True:
	print(f"Enter a valid year in range 2018-{dt.now().year}")
    
	start_year = int(input("Starting year: "))
	end_year = int(input("Ending year: "))

	if start_year < 2018: continue
	if start_year > end_year: continue
	if end_year > dt.now().year: continue

	break

print(f'\nTop 100 Clubs {start_year} - {end_year} | DJMag.com\n' + "Please wait... ")

start_time = timeit.default_timer()
clubs = []

for year in range(start_year, end_year + 1):
	url = f"https://djmag.com/top100clubs/{year}"
	r = requests.get(url)
	data = r.text

	soup = BeautifulSoup(data,'html.parser')
	clubTags = soup.findAll('div', { 'class' : 'views-field views-field-field-top100-places' })

	for clubTag in clubTags:
		club = {
			'rank': '',
			'name': '',
			'city': '',
			'country': '',
			'lat': '',
			'lng': '',
			'capacity': '',
			'arrow': '',
			'numpos': '',
			'year': year,
			# 'website': '',
		}
		
		temp = clubTag.a['href'].split("/")
		club['rank'] = temp[3]
		club['name'] = clubTag.a.string.strip()

		try:
			club['arrow'] = str(clubTag.i).split("-")[4].split("\"")[0]
		except:
			club['arrow'] = "Undefined"
		
		club['numpos'] = clubTag.find('div', { 'class' : 'top100dj-movement' }).text.strip()
		clubLink = 'http://djmag.com' + clubTag.a['href'] # club link

		# open individual club page
		
		tempr = requests.get(clubLink)
		clubData = tempr.text
		clubSoup = BeautifulSoup(clubData, 'html.parser')

		clubInfo = clubSoup.findAll('p')
		
		location = clubInfo[0].text.split(':')[1].replace('Capacity', '').strip() # fix for year 2020
		
		# split location

		try:
			club['city'] = location.split(',')[0].strip()
			club['country'] = location.split(',')[1].strip()

			if club['city'] == 'Zrce Beach':
				club['city'] = 'Zr\u0107e Beach'
			if club['city'] == 'Nescastle':
				club['city'] = 'Newcastle'

			if club['country'] == 'Island of Pag':
				club['country'] = 'Croatia'
			if club['country'] == 'Sapin':
				club['country'] = 'Spain'
		except:
			club['city'] = location
			club['country'] = "Unknown"

		if club['country'] != "Unknown":
			floc = str(club['city'] + ', ' + club['country'])
		else:
			floc = str(club['city'])

		temploc = geolocator.geocode(floc)

		try:
			club['lat'] = temploc.latitude
			club['lng'] = temploc.longitude
		except:
			club['lat'] = "Unknown"
			club['lng'] = "Unknown"
		
		try:
			if year != 2020:
				cap = re.sub(r'[^0-9]', '', clubInfo[1].text.split(':')[1].strip())
			else:
				cap = re.sub(r'[^0-9]', '', clubInfo[0].text.split(':')[2].strip())

			try:
				club['capacity'] = int(cap)

				if club['capacity'] > 100000:
					club['capacity'] = "Unknown"
			except:
				club['capacity'] = "Unknown"

			if club['capacity'] == "n/a":
				club['capacity'] = "Unknown"
		except:
			club['capacity'] = "Unknown"
		
		# get club website (not available for all clubs)

		# try:
		# 	club['website'] = clubInfo[2].a['href'].replace("//", "")
		# except:
		# 	tempw = clubInfo[2].text.strip().replace("\n", "") # error rank 47 year 2023, problem rank 32 year 2023
		
		# 	if tempw == "":
		# 		club['website'] = "Undefined"
		# 	else:
		# 		club['website'] = temp

		#todo: get tripadvisor rating

		clubs.append(club)

output_folder = os.path.join(os.path.dirname(__file__), 'Output JSON')
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, 'top_clubs_' + str(start_year) + '_' + str(end_year) + '.json')

with open(output_file, 'w') as fp:
	json.dump(clubs, fp, indent=4)

print('\nDataset saved successfully!')

end_time = timeit.default_timer()
print("Total execution time:", round(end_time - start_time, 2), "s")
