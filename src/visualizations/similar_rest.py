import pandas as pd
import numpy as np
from scipy import stats
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity

def cos_sim(a, b):
    """Takes 2 vectors a, b and returns the cosine similarity according
    to the definition of the dot product
    """
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)


def similar_restaurants(restaurant_id, n):

    raw_data2 = pd.read_csv('static/data/phoenix_business_ws_rw_ffall_merged2.csv', skipinitialspace=True)

    drop_cols = ['zipcode', 'zipcode.1', 'ffall_category', 'CuisineCombined', 'male', 'female', 'under_18', 'above_18', 'review_count']
    data = raw_data2.drop(columns=drop_cols)

    df = data.set_index('business_id')

    sim_score = defaultdict()
    out = []
    a = df.loc[restaurant_id]
    for biz_id, row in df.iterrows():
        sim_score[biz_id] = cos_sim(a, row)
    sim_list = sorted(sim_score.items(), key=lambda kv: -kv[1])[1:n+1]

    for (x, y) in sim_list:
        out.append(x)
    return out

