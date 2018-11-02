import walkscore_frontend
import json

city = "Atlanta"
state = "GA"

data = walkscore_frontend.data_for_city( city, state)

with open('city_scores.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)