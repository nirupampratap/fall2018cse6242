from dataLoad import load_zipdata, load_zip_res_density
from locRecoModel import get_model
import json
import pandas as pd
import numpy as np

testDict = [{'Mexican' : 0, 'American (Traditional)': 0, 'Pizza': 0, 'American (New)': 0, 'Burgers': 0, 'Italian': 0, 
'Chinese': 1, 'Salad': 0, 'Sports Bars': 0, 'Seafood': 0, 'Japanese': 0, 'Barbeque': 0, 'Mediterranean': 0, 
'Sushi Bars': 0, 'Asian Fusion': 0, 'Steakhouses': 0, 'Greek': 0, 'Tex-Mex': 0, 'Thai': 0, 'Vietnamese': 0, 
'Indian': 1, 'Middle Eastern': 0, 'Southern': 0, 'Latin American': 0, 'Hawaiian': 0, 'Korean': 0, 'French': 0, 
'Caribbean': 0, 'Pakistani': 0, 'Ramen': 0, 'New Mexican Cuisine': 0, 'Modern European': 0, 'Spanish': 0, 
'African': 0, 'Cantonese': 0, 'Persian/Iranian': 0, 'Filipino': 0, 'Cuban': 0, 'Mongolian': 0, 'Lebanese': 0, 
'Polish': 0, 'Taiwanese': 0, 'German': 0, 'Turkish': 0, 'Ethiopian': 0,'Brazilian': 0, 'Afghan': 0}]

def get_density_zip_cu(zipcode, cuvecdict, zip_pop_cu_density_df):

    row = zip_pop_cu_density_df[zip_pop_cu_density_df.zipcode == zipcode]
    max_d = -1
    pop_g = row['popgrowth'].iloc[0]

    for key, val in cuvecdict.items():
        if(val == 1 and max_d <= row[key].iloc[0]):
            max_d = row[key].iloc[0]

    if(max_d == 0):
        max_d = -1

    return max_d, pop_g


def get_locations(cuvecjson):
    # Get the model
    model = get_model()

    # Get zip code level data
    zipdata = load_zipdata()
    target_stars = 5.0

    cuvedict = json.loads(cuvecjson)[0]
    zip_ffall = []

    for ind, row in zipdata.iterrows():
        df = pd.DataFrame(row)
        df2 = df.T
        for key, val in cuvedict.items():
            df2[key] = cuvedict[key]

        df2['adjwhp'] = df2['white_pop'] * target_stars
        df2['adjpafp'] = df2['afam_pop'] * target_stars
        df2['adjindp'] = df2['amindian_pop'] * target_stars
        df2['adjasp'] = df2['asian_pop'] * target_stars
        df2['adjhwp'] = df2['hawaiian_pop'] * target_stars
        df2['adjorp'] = df2['other_race'] * target_stars
        df2['stars'] = target_stars
        df2['stars_avgffc'] = target_stars * df2['avgffall']
        df2['stars_avgrc'] = target_stars * df2['avgffall'] * df2['total_pop']

        selected_df = df2[['Mexican', 'American (Traditional)', 'Pizza', 'American (New)',
       'Burgers', 'Italian', 'Chinese', 'Salad', 'Sports Bars', 'Seafood',
       'Japanese', 'Barbeque', 'Mediterranean', 'Sushi Bars', 'Asian Fusion',
       'Steakhouses', 'Greek', 'Tex-Mex', 'Thai', 'Vietnamese', 'Indian',
       'Middle Eastern', 'Southern', 'Latin American', 'Hawaiian', 'Korean',
       'French', 'Caribbean', 'Pakistani', 'Ramen', 'New Mexican Cuisine',
       'Modern European', 'Spanish', 'African', 'Cantonese', 'Persian/Iranian',
       'Filipino', 'Cuban', 'Mongolian', 'Lebanese', 'Polish', 'Taiwanese',
       'German', 'Turkish', 'Ethiopian', 'Brazilian', 'Afghan', 'walkscore',
       'stars', 'adjwhp', 'adjpafp', 'adjindp', 'adjasp', 'adjhwp', 'adjorp',
       'PCT0050002', 'PCT0050003', 'PCT0050004', 'PCT0050005', 'PCT0050006',
       'PCT0050007', 'PCT0050008', 'PCT0050009', 'PCT0050010', 'PCT0050011',
       'PCT0050012', 'PCT0050013', 'PCT0050014', 'PCT0050015', 'PCT0050016',
       'PCT0050017', 'PCT0050018', 'PCT0050019', 'PCT0050020', 'PCT0050021',
       'PCT0050022', 'avgffall', 'avgffc', 'stars_avgrc']]

        results = model.predict(selected_df)
        zip_ffall.append([int(row['zipcode']), np.exp(results[0]), 0])

    zip_ffall_df = pd.DataFrame(zip_ffall, columns=['zipcode','ffall','rank'])
    zip_ffall_df.sort_values(by='ffall', inplace = True, ascending=False)

    zip_res_density_df = load_zip_res_density()
    density = 0

    for ind,row in zip_ffall_df.iterrows():
        density, pop_g = get_density_zip_cu(row['zipcode'], cuvedict, zip_res_density_df)
        zip_ffall_df['rank'].loc[ind] = row['ffall'] * pop_g / density

    zip_ffall_df.sort_values(by='rank', inplace=True, ascending = False)

    return zip_ffall_df


locations = get_locations(json.dumps(testDict))
