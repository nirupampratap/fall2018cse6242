import pandas as pd
import numpy as np
import math
import random
import warnings

#Ignore warnings 
warnings.simplefilter("ignore", category=DeprecationWarning)

def load_zipdata():
    # Load Data
    raw_data = pd.read_csv('static/data/phoenix_business_ws_rw_ffall_merged2.csv', skipinitialspace=True)

    # Processing Data
    dframe = raw_data
    dframe['totalStars'] = dframe['review_count'] * dframe['stars']
    dframe['adjwhp'] = dframe['white_pop'] * dframe['stars']
    dframe['adjpafp'] = dframe['afam_pop'] * dframe['stars']
    dframe['adjindp'] = dframe['amindian_pop'] * dframe['stars']
    dframe['adjasp'] = dframe['asian_pop'] * dframe['stars']
    dframe['adjhwp'] = dframe['hawaiian_pop'] * dframe['stars']
    dframe['adjorp'] = dframe['other_race'] * dframe['stars']

    zip_means_df = dframe.groupby(['zipcode']).agg([np.mean])
    zip_avg_ffall_revC_list = []
    rowitem = []

    for ind, row in zip_means_df.iterrows():
        zip_avg_ffall_revC_list.append([ind, row.iloc[65], row.iloc[63], row[66]])
    
    zip_avg_ffall_revC_df = pd.DataFrame(zip_avg_ffall_revC_list, columns=['zipcode','avgrc','avgffall', 'avgffc'])
    zip_avg_ffall_revC_df.drop_duplicates(inplace = True)

    pop_data = pd.read_csv('static/data/arizon.csv', skipinitialspace=True)

    selected_pop = pop_data[['zipcode', 'PCT0050002', 'PCT0050003', 'PCT0050004', 'PCT0050005', 'PCT0050006',
           'PCT0050007', 'PCT0050008', 'PCT0050009', 'PCT0050010', 'PCT0050011',
           'PCT0050012', 'PCT0050013', 'PCT0050014', 'PCT0050015', 'PCT0050016',
           'PCT0050017', 'PCT0050018', 'PCT0050019', 'PCT0050020', 'PCT0050021',
           'PCT0050022']]

    joined_data = dframe.merge(selected_pop, left_on="zipcode", right_on="zipcode", how="inner", suffixes = ("_a","_b"))

    final_data = joined_data.merge(zip_avg_ffall_revC_df, left_on="zipcode", right_on="zipcode", how="inner", 
                                suffixes = ("_a","_b"))
    # Select columns
    X = final_data.drop(columns=['business_id', 'CuisineCombined',
                                  'male','female','under_18','above_18','occupied_housing_units', 'review_count', 
                                  'ffall', 'zipcode.1', 'median_age', 'zipcode.1','avgrc', 'ffall_category', 
                                  'median_income', 'adjwhp','adjpafp','adjindp','adjasp','adjhwp','adjorp',
                                  'totalStars', 'ffall', 'Mexican', 'American (Traditional)', 'Pizza', 
                                  'American (New)', 'Burgers', 'Italian', 'Chinese', 'Salad', 'Sports Bars', 'Seafood', 
                                  'Japanese', 'Barbeque', 'Mediterranean', 'Sushi Bars', 'Asian Fusion', 'Steakhouses', 
                                  'Greek', 'Tex-Mex', 'Thai', 'Vietnamese', 'Indian', 'Middle Eastern', 'Southern', 'Latin American',
                                  'Hawaiian', 'Korean', 'French', 'Caribbean', 'Pakistani', 'Ramen', 'New Mexican Cuisine', 'Modern European', 
                                  'Spanish', 'African', 'Cantonese', 'Persian/Iranian', 'Filipino', 'Cuban', 'Mongolian',
                                  'Lebanese', 'Polish', 'Taiwanese', 'German', 'Turkish', 'Ethiopian','Brazilian', 'Afghan','stars'])

    X.drop_duplicates(inplace=True)

    return X

def load_zip_res_density():
    # Load Data
    raw_data = pd.read_csv('static/data/phoenix_business_ws_rw_ffall_merged2.csv', skipinitialspace=True)

    zip_pop_data = raw_data[['zipcode', 'total_pop']]
    zip_pop_data.drop_duplicates(inplace=True)

    dframe = raw_data[['zipcode', 'Mexican', 'American (Traditional)', 'Pizza', 'American (New)',
       'Burgers', 'Italian', 'Chinese', 'Salad', 'Sports Bars', 'Seafood',
       'Japanese', 'Barbeque', 'Mediterranean', 'Sushi Bars', 'Asian Fusion',
       'Steakhouses', 'Greek', 'Tex-Mex', 'Thai', 'Vietnamese', 'Indian',
       'Middle Eastern', 'Southern', 'Latin American', 'Hawaiian', 'Korean',
       'French', 'Caribbean', 'Pakistani', 'Ramen', 'New Mexican Cuisine',
       'Modern European', 'Spanish', 'African', 'Cantonese', 'Persian/Iranian',
       'Filipino', 'Cuban', 'Mongolian', 'Lebanese', 'Polish', 'Taiwanese',
       'German', 'Turkish', 'Ethiopian', 'Brazilian', 'Afghan']]

    zip_agg_sum = dframe.groupby(['zipcode']).agg([np.sum]).reset_index()
    zip_agg_sum.columns = ['zipcode', 'Mexican', 'American (Traditional)', 'Pizza', 'American (New)',
       'Burgers', 'Italian', 'Chinese', 'Salad', 'Sports Bars', 'Seafood',
       'Japanese', 'Barbeque', 'Mediterranean', 'Sushi Bars', 'Asian Fusion',
       'Steakhouses', 'Greek', 'Tex-Mex', 'Thai', 'Vietnamese', 'Indian',
       'Middle Eastern', 'Southern', 'Latin American', 'Hawaiian', 'Korean',
       'French', 'Caribbean', 'Pakistani', 'Ramen', 'New Mexican Cuisine',
       'Modern European', 'Spanish', 'African', 'Cantonese', 'Persian/Iranian',
       'Filipino', 'Cuban', 'Mongolian', 'Lebanese', 'Polish', 'Taiwanese',
       'German', 'Turkish', 'Ethiopian', 'Brazilian', 'Afghan']

    joined_data = zip_agg_sum.merge(zip_pop_data, left_on="zipcode", right_on="zipcode", how="inner", suffixes = ("_a","_b"))

    zip_pop_cu_agg = joined_data[['zipcode', 'Mexican', 'American (Traditional)', 'Pizza', 'American (New)',
       'Burgers', 'Italian', 'Chinese', 'Salad', 'Sports Bars', 'Seafood',
       'Japanese', 'Barbeque', 'Mediterranean', 'Sushi Bars', 'Asian Fusion',
       'Steakhouses', 'Greek', 'Tex-Mex', 'Thai', 'Vietnamese', 'Indian',
       'Middle Eastern', 'Southern', 'Latin American', 'Hawaiian', 'Korean',
       'French', 'Caribbean', 'Pakistani', 'Ramen', 'New Mexican Cuisine',
       'Modern European', 'Spanish', 'African', 'Cantonese', 'Persian/Iranian',
       'Filipino', 'Cuban', 'Mongolian', 'Lebanese', 'Polish', 'Taiwanese',
       'German', 'Turkish', 'Ethiopian', 'Brazilian', 'Afghan', 'total_pop']]


    col_list = [ 'Mexican', 'American (Traditional)', 'Pizza', 'American (New)',
       'Burgers', 'Italian', 'Chinese', 'Salad', 'Sports Bars', 'Seafood',
       'Japanese', 'Barbeque', 'Mediterranean', 'Sushi Bars', 'Asian Fusion',
       'Steakhouses', 'Greek', 'Tex-Mex', 'Thai', 'Vietnamese', 'Indian',
       'Middle Eastern', 'Southern', 'Latin American', 'Hawaiian', 'Korean',
       'French', 'Caribbean', 'Pakistani', 'Ramen', 'New Mexican Cuisine',
       'Modern European', 'Spanish', 'African', 'Cantonese', 'Persian/Iranian',
       'Filipino', 'Cuban', 'Mongolian', 'Lebanese', 'Polish', 'Taiwanese',
       'German', 'Turkish', 'Ethiopian', 'Brazilian', 'Afghan']

    for col in col_list:
        zip_pop_cu_agg[col] = zip_pop_cu_agg[col] * 1000 / zip_pop_cu_agg['total_pop']


    # For now have a random value set in place
    zip_pop_cu_agg['popgrowth'] = zip_pop_cu_agg['zipcode'].apply(lambda x: random.uniform(0,1))


    return zip_pop_cu_agg
