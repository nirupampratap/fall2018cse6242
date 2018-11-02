import walkscore_frontend
import json

zipcodes = [str(i) for i in range(85001, 85710)]


city = "Phoenix"
state = "AZ"

data = []

for zipcode in zipcodes:	
	zipcode_data = walkscore_frontend.data_for_zipcode(zipcode, city, state)

	if zipcode_data:

		print(zipcode + " OK")
		zipcode_data.pop('price_range', None)
		zipcode_data.pop('neighborhoods', None)
		zipcode_data.pop('price_range', None)
		zipcode_data.pop('transit_score', None)
		zipcode_data.pop('bike_score', None)
		zipcode_data.pop('date', None)
		zipcode_data.pop('sort_date', None)
		zipcode_data.pop('lat', None)
		zipcode_data.pop('lng', None)
		data.append(zipcode_data)

	else:
		print(zipcode + " No data")

with open('zipcode_scores.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)