from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
from gensim.summarization import summarize
from gensim.summarization import keywords
import pandas as pd
import numpy as np

import pandas as pd
import numpy as np
from scipy import stats
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity



def clean(doc):
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

def format_topics_sentences(ldamodel, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)

def getReviewForTopic(ldamodel,corpus,texts):
    df_topic_sents_keywords=format_topics_sentences(ldamodel=ldamodel, corpus=corpus, texts=texts)
    sent_topics_sorteddf_mallet = pd.DataFrame()
    sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')
    for i, grp in sent_topics_outdf_grpd:
        sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet,
                                                 grp.sort_values(['Perc_Contribution'], ascending=[0]).head(1)],
                                                axis=0)
    # Reset Index
    sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)
    # Format
    sent_topics_sorteddf_mallet.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Text"]
    return sent_topics_sorteddf_mallet

def getTopics(restuarant_reviews,n):
    reviews=[rev for rev in restuarant_reviews['text']]
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    reviews_clean = [clean(review).split() for review in reviews]
    dictionary = corpora.Dictionary(reviews_clean)
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    review_term_matrix = [dictionary.doc2bow(review) for review in reviews_clean]
    Lda = gensim.models.ldamodel.LdaModel
    ldamodel = Lda(review_term_matrix, num_topics=n, id2word = dictionary, passes=50)
    topics=[]
    if ldamodel.num_topics-1<n:
        n=ldamodel.num_topics-1

    for i in range(0, n):
        topics.append(ldamodel.print_topic(i))
    #also return summary of relevant reviews for each topic
    topic_reviews=getReviewForTopic(ldamodel=ldamodel,corpus=review_term_matrix,texts=reviews)
    topic_reviews_text=list(topic_reviews['Text'])
    review_summary=[]
    for rev in topic_reviews_text:
        review_summary.append(summarize(rev, word_count = 20))
    return topics,review_summary

def getRestuarantTopics(business_id,n=5):
    reviews_df=pd.read_csv('review_arizon.csv')
    positive_reviews=reviews_df[reviews_df.business_id==business_id][reviews_df.stars_y>=3]
    negative_reviews=reviews_df[reviews_df.business_id==business_id][ reviews_df.stars_y<3]
    positive_topics,pos_reviews=getTopics(positive_reviews,n)
    negative_topics,neg_reviews=getTopics(negative_reviews,n)
    return positive_topics,pos_reviews,negative_topics,neg_reviews

def cos_sim(a, b):
    """Takes 2 vectors a, b and returns the cosine similarity according
    to the definition of the dot product
    """
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

def similar_restaurants(df,restaurant_id, n):
    sim_score = defaultdict()
    out = []
    a = df.loc[restaurant_id]
    for biz_id, row in df.iterrows():
        sim_score[biz_id] = cos_sim(a, row)
    sim_list = sorted(sim_score.items(), key=lambda kv: -kv[1])[1:n+1]

    for (x, y) in sim_list:
        out.append(x)
    return out

def getReviews(restuarant_id,n):
    raw_data2 = pd.read_csv('phoenix_business_ws_rw_ffall_merged2.csv', skipinitialspace=True)
    drop_cols = ['zipcode', 'zipcode.1', 'ffall_category', 'CuisineCombined', 'male', 'female', 'under_18', 'above_18', 'review_count']
    data = raw_data2.drop(columns=drop_cols)
    data = data.set_index('business_id')
    df = data
    sim_restuarants=similar_restaurants(df,restuarant_id,n)
    topics_reviews=[]
    for restaurant in sim_restuarants:
        topics_reviews.append(getRestuarantTopics(restaurant,n))
    return topics_reviews

print(getReviews('8NMf2dCmEGGKYR3SbMcnNA',3))
