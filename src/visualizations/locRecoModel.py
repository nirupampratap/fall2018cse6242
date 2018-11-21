import pandas as pd
import numpy as np
import math
import xgboost as xgb
import warnings
from sklearn.metrics import mean_squared_error, r2_score
#Ignore warnings 
warnings.simplefilter("ignore", category=DeprecationWarning)

def load_model_data():
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
    final_data['stars_avgffc'] = final_data['stars'] * final_data['avgffall']
    final_data['stars_avgrc'] = final_data['stars'] * final_data['avgffall'] * final_data['total_pop']

    # Select columns
    X_train = final_data.drop(columns=['zipcode','business_id', 'CuisineCombined','total_pop',
                                  'male','female','under_18','above_18','occupied_housing_units', 'review_count', 
                                  'ffall', 'zipcode.1', 'median_age', 'zipcode.1', 
                                  'asian_pop', 'avgrc', 'ffall_category', 'white_pop', 'afam_pop', 'amindian_pop', 
                                  'hawaiian_pop', 'other_race', 'median_income', 'totalStars', 'stars_avgffc', 'ffall'])
    #dframe[['white_pop', 'afam_pop', 'amindian_pop', 'hawaiian_pop', 'other_race']]
    y_train = final_data['ffall']

    return X_train, y_train

def build_xgboost_model(X_train, y_train):
    xg_reg = xgb.XGBRegressor(objective ='reg:linear', colsample_bytree = 0.6, learning_rate = 0.1,
                    max_depth = 5, alpha = 10, n_estimators = 50)

    xg_reg.fit(X_train, np.log(y_train))

    return xg_reg

def get_model():
    x,y = load_model_data()
    model = build_xgboost_model(x, y)
    #print("R-Square on Training set", r2_score(np.log(y), model.predict(x)))
    return model
