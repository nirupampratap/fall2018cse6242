import walkscore_frontend
import json

city = "Phoenix"
state = "AZ"

data = walkscore_frontend.data_for_city( city, state)

with open('phoenix_scores.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)