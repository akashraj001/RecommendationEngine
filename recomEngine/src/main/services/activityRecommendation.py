def recommend():
    userid='5f732fa0b6a715000181f528'
    import pandas as pd
    from pymongo import MongoClient
    import time
    import numpy as np
    from bson.objectid import ObjectId
    mongo_client = MongoClient(
        'mongodb://root:pqeBqx8qgV@20.193.137.123:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')

    db = mongo_client.bighaat
    col = db.profile_recommendation

    cursor = col.find({'userId': ObjectId(user_id)})
    print("total docs in collection:", col.count_documents({}))
    user = list(cursor)
    print(user)

    db = mongo_client.bighaat
    col = db.posts
    cursor = col.find()
    print("total docs in collection:", col.count_documents({}))
    mongo_docs = list(cursor)

    start_time = time.time()
    posts = pd.DataFrame(columns=[])
    for num, doc in enumerate(mongo_docs):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series(doc, name=doc_id)
        # append the MongoDB Series obj to the DataFrame obj
        posts = posts.append(series_obj)
        # get document _id from dict
        doc_id = doc["_id"]
    print("--- %s seconds ---" % (time.time() - start_time))

    col = db.crops
    cursor = col.find()
    print("total docs in collection:", col.count_documents({}))
    mongo_docs = list(cursor)

    crops = pd.DataFrame(columns=[])
    start_time = time.time()
    for num, doc in enumerate(mongo_docs):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series(doc, name=doc_id)
        # append the MongoDB Series obj to the DataFrame obj
        crops = crops.append(series_obj)
        # get document _id from dict
        doc_id = doc["_id"]
    print("--- %s seconds ---" % (time.time() - start_time))

    import pandas as pd
    from scipy.spatial import distance

    vec_user = np.array(list(user[0].values())[4:])

    posts.columns
    posts.reset_index(drop=True, inplace=True)
    posts = posts[['_id', 'userId', 'title', 'upvotes', 'locale', 'viewedUsers', 'postContext']]
    posts = posts.rename(columns={'_id': 'postId'})

    posts['x'] = posts['locale'].apply(lambda x: x['location']['coordinates'][0])
    posts['y'] = posts['locale'].apply(lambda x: x['location']['coordinates'][1])

    posts['language'] = posts['locale'].apply(lambda x: x['language'])
    posts = pd.concat([posts, pd.get_dummies(posts['language'])], axis=1)
    posts.drop('locale', axis=1, inplace=True)

    posts['cropId'] = posts['postContext'].apply(lambda x: str(x['cropId']))
    posts.drop('postContext', axis=1, inplace=True)

    crop_dict = dict(zip(crops['_id'], crops['cropName']))

    posts[list(crop_dict.values())] = 0

    for row in posts.itertuples():
        pass
        posts.loc[row[0], crop_dict[row[12]]] = 1

    user_cols = list(user[0].keys())
    #    return user_cols
    user_cols = list(user_cols[4:])

    post_cols = posts.columns
    post_cols = [i for i in post_cols if
                 i not in ['language', 'postId', 'userId', 'title', 'upvotes', 'viewedUsers', 'x', 'y', 'cropId']]

    #    return user_cols==post_cols,user_cols,post_cols

    posts[post_cols] = posts[post_cols][posts[post_cols] == 0]
    posts = posts.fillna(7)

    # vector_posts=s_user.transform(posts[cols_non_xy])
    vector_posts = posts[post_cols]

    score = []
    for i in range(len(vector_posts)):
        dst = distance.euclidean(vector_posts.iloc[i, :], vec_user)
        score.append(dst)
    post_res = posts[['x', 'y', 'postId', 'title']]
    post_res['score'] = score
    post_res.sort_values(by='score', inplace=True)
    # res=pd.DataFrame(posts[['x','y','postId','title']].values,score)
    # res.sort_index(inplace=True)
    # res.columns=['Title']
    # res.index.name='Score'
    post_res = post_res.iloc[:20, :]
    print(post_res.iloc[:20, 2:].set_index('score'))

    vector_posts_xy = post_res.iloc[:20, :][['x', 'y']]
    user_xy = np.array(list(user[0].values())[2:4])

    score_xy = []
    for i in range(len(vector_posts_xy)):
        dst = distance.euclidean(vector_posts_xy.iloc[i, :], user_xy)
        score_xy.append(dst)

    post_res['score_xy'] = score_xy
    post_res.sort_values(by='score_xy', inplace=True)
    print(post_res.iloc[:20, 2:-1].set_index('score'))

    return post_res['postId'].tolist()