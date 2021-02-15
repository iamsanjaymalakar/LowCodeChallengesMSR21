import pandas as pd

df = pd.DataFrame()
so_df = pd.read_csv('so_data.csv')

tid = []
questions_cnt = []
avg_view_cnt = []
avg_fav_cnt = []
answers_cnt = []

def linkToId(x):
    '''
    Takes a excel styled link and retures the QuestionID
    '''
    return int(x.split('"')[::-1][1])


for topic_id in range(13):
    # topic id
    tid.append(topic_id)
    temp_df = pd.read_csv(f'./{topic_id}/Questions.csv')
    # number of questions for particular topic
    questions_cnt.append(len(temp_df))
    # converting excel links to question id
    temp_df.link = temp_df.link.apply(linkToId) 
    # merging with original df for view and fav count
    merged_df = pd.merge(temp_df, so_df, how='left', left_on='link',right_on='Id', validate='one_to_one')
    # calculating avg view count
    avg_view_cnt.append(merged_df.ViewCount.mean())
    # calculating avg favorite count
    avg_fav_cnt.append(merged_df.FavoriteCount.mean())
    # number of answers for particular topic
    answers_cnt.append(len(pd.read_csv(f'./{topic_id}/Answers.csv')))

df['Topic_Id'] = tid
df['Num_of_Questions'] = questions_cnt
df['Avg_View_Count'] = avg_view_cnt
df['Avg_Favourite_Count'] = avg_fav_cnt
df['Num_of_Answers'] = answers_cnt

df.to_csv('Overview.csv', index=False)


