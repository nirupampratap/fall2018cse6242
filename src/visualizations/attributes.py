import pandas as pd
import json
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns; sns.set()

from sklearn.model_selection import train_test_split
import ast
import similar_rest as sr

raw_data = pd.read_csv('static/data/arizona_business_details.csv', skipinitialspace=True)
raw_data['postal_code'] = raw_data['postal_code'].fillna(0)

raw_data['postal_code'] = raw_data['postal_code'].astype(int)


attributes = set()
for each in raw_data['attributes']:
	line = {}
	try:
		each = eval(each)
	except TypeError:
		continue
	for k in each.keys():
		attributes.add(k)

attributes = list(attributes)


def get_attributes(zipcode):

	attribute_count = defaultdict(int)
	data = raw_data[raw_data['postal_code'] == zipcode]
	n = data.shape[0]
	for each in data['attributes']:
		try:
			for attribute in attributes:
				if attribute in each:
					attribute_count[attribute] += 1
		except TypeError:
			continue
	count_df = pd.DataFrame.from_dict(attribute_count, orient='index', columns= ['count'])
	count_df['percent_of_total'] = count_df['count']/n
	count_df = count_df.sort_values(by = 'percent_of_total', inplace=False, ascending=False)

	return count_df

features = ['BusinessAcceptsCreditCards',
 'RestaurantsTakeOut',
 'RestaurantsGoodForGroups',
 'GoodForKids',
 'RestaurantsDelivery',
 'RestaurantsReservations',
 'OutdoorSeating',
 'Alcohol',
 'RestaurantsTableService',
 'HasTV',
 'WiFi',
 'BikeParking',
 'Caters',
 'WheelchairAccessible']

check = ['False', 'False', 'False', 'False', 'False', 'False', 'False', 'none', 'False', 'False', 'no', 
		 'False', 'False', 'False']

nest_features = ['Ambience', 'GoodForMeal', 'BusinessParking']
add_features = {}
add_features['Ambience'] = ['romantic', 'intimate', 'classy', 'hipster', 'divey', 'touristy', 'trendy', 'upscale', 'casual']
add_features['GoodForMeal'] = ['dessert', 'latenight', 'lunch', 'dinner', 'breakfast', 'brunch']
add_features['BusinessParking'] = ['garage', 'street', 'validated', 'lot', 'valet']
all_features = features + nest_features
def attribute_check(attribute, restaurant, check):
	if attribute in restaurant:
		if restaurant[attribute] == check:
			return 0
		else:
			return 1
	else:
		return 0


def create_dataframe(zipcode):
	attributes_zip = get_attributes(zipcode)
	attributes = attributes_zip[attributes_zip['percent_of_total'] > 0.45].index.values.tolist()
	
	if 'RestaurantsPriceRange2' in attributes:
		attributes.remove('RestaurantsPriceRange2')
	data = raw_data[raw_data['postal_code'] == zipcode]
	dframe = pd.DataFrame()
	for index, row in data.iterrows():

		try:
			each = eval(row['attributes'])
			line = {}
			line['rating'] = row['stars']
			line['biz_id'] = row['business_id']
			for i in range(len(features)):
				line[features[i]] = attribute_check(features[i], each, check[i])

			# adding the nest features 
			for feature in nest_features:
				if feature in each: 
					for cat in add_features[feature]:
						if ast.literal_eval(each[feature])[cat] == True:
							line[feature + '_' + cat] = 1
						else:
							line[feature + '_' + cat] = 0
				else:
					for cat in add_features[feature]:
							line[feature + '_' + cat] = 0

			# converting the dict as df 
			temp_df = pd.DataFrame([line])
			dframe = dframe.append(temp_df, ignore_index=True, sort=False)

		except TypeError:
			continue
	return dframe


def is_the_attribute_present(biz_id, attribute):
	zipcode = raw_data[raw_data['business_id'] == biz_id]['postal_code'].iloc[0]
	zip_df = create_dataframe(zipcode)
	restaurant = zip_df[zip_df['biz_id'] == biz_id]
	val = restaurant[attribute].iloc[0]
	return val

def restaurant_case(biz_id):
	zipcode = raw_data[raw_data['business_id'] == biz_id]['postal_code'].iloc[0]
	df = create_dataframe(zipcode)
	restaurant = df[df['biz_id'] == biz_id]
	
	#imp_attributes = zipcode_attributes[zipcode]
	data = pd.read_csv('static/data/zipcode_attributes.csv')
	data = data[["Attributes", str(zipcode)]]
	
	imp_attributes = {}
	for index, row in data.iterrows():
		if not np.isnan(row[str(zipcode)]):
			imp_attributes[row["Attributes"]] = row[str(zipcode)]

	imp_attributes_list = list(imp_attributes.keys())
	sug_restaurants = sr.similar_restaurants(biz_id, 5)
	
	existing_attributes = []
	for attr in list(restaurant.columns):
		if (restaurant[attr].iloc[0] == 1) :
			existing_attributes.append(attr)

	
	req_attributes = set(imp_attributes_list) - set(existing_attributes)
	
	values = list(imp_attributes.values())
	range_ = max(values) - min(values);
	min_ = min(values)

	final_attr = defaultdict(dict)
	sim_rests = defaultdict(dict)

	for attribute in list(req_attributes):
		importance = imp_attributes[attribute]
		importance = (importance - min_)/range_
		importance = np.round((importance * 4) + 1)
		
		ind = list(req_attributes).index(attribute)
		final_attr[ind]['attribute'] = attribute
		final_attr[ind]['importance'] = importance
		final_attr[ind]['percentage'] = np.round(imp_attributes[attribute] * 100)
		i = 0
		for restaurant in sug_restaurants:
			rest_details = defaultdict(dict)
			if is_the_attribute_present(restaurant, attribute) == 1:
				rest_details['name'] = restaurant
				rest_details['location'] = raw_data[raw_data['business_id'] == restaurant]['postal_code'].iloc[0]
				rest_details['rating'] = raw_data[raw_data['business_id'] == restaurant]['stars'].iloc[0]
				rest_details['review_count'] = raw_data[raw_data['business_id'] == restaurant]['review_count'].iloc[0]
				rest_details['url'] = 'https://www.yelp.com/biz/'+ restaurant
				sim_rests[attribute][i] = rest_details
				i += 1
		
		
	if len(final_attr) > 0:
		final_attr = final_attr
	else:
		final_attr = "hey, seems like you are doing pretty good! kepp it up!!"
	
		

	return final_attr, sim_rests
