# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
get_ipython().run_line_magic('matplotlib', 'inline')


# %%
TAGS = ['salesforce-lightning', 'lwc', 'lightning', 'salesforce-communities',
        'salesforce-chatter', 'salesforce-service-cloud', 'aura-framework', 'appian',
        'outsystems', 'google-app-maker', 'zoho', 'mendix', 'powerapps', 'powerapps-formula',
        'powerapps-selected-items', 'powerapps-collection', 'powerapps-canvas', 'quickbase', 'vinyl']

PLATFORMS = {
    'Salesforce' : ['salesforce-lightning', 'lwc', 'lightning', 'salesforce-communities',
        'salesforce-chatter', 'salesforce-service-cloud', 'aura-framework'],
    'Appian' : ['appian'],
    'Outsystems' : ['outsystems'],
    'AppMaker' : ['google-app-maker'],
    'Zoho' : ['zoho'],
    'Mendix' : ['mendix'],
    'PowerApps' : ['powerapps', 'powerapps-formula',
        'powerapps-selected-items', 'powerapps-collection', 'powerapps-canvas'],
    'QuickBase' : ['quickbase'],
    'Vinyl' : ['vinyl']
} 


# %%
so_df = pd.read_csv('so_data.csv')
so_df.CreationDate = so_df.CreationDate.apply(pd.to_datetime)
so_df.AcceptedAnswerCreationDate = so_df.AcceptedAnswerCreationDate.apply(pd.to_datetime)
so_df.dtypes


# %%
so_ans_df = so_df = pd.read_csv('AllAnswers.csv')
so_ans_df.CreationDate = so_ans_df.CreationDate.apply(pd.to_datetime)
so_ans_df.dtypes


# %%
print(so_df.sort_values(by='CreationDate').iloc[0].CreationDate)
so_df.sort_values(by='CreationDate').head(5)

# %% [markdown]
# # Stats per tag

# %%
sum = 0
no_of_questions = []
avg_view_count = []
avg_fav_count = []
for tag in TAGS:
    indicesToRemove = []
    for i in range(len(so_df)):
        qtags = so_df.iloc[i]['Tags'][1:-1].replace('><', ' ').split()
        f = True
        for qtag in qtags:
            if qtag == tag:
                f = False
                break
        if f:
            indicesToRemove.append(i)
    temp_df = so_df.drop(index=indicesToRemove)
    no_of_questions.append(len(temp_df))
    avg_view_count.append(temp_df.ViewCount.mean())
    avg_fav_count.append(temp_df.FavoriteCount.mean())
    sum += len(temp_df)
print(sum)
df = pd.DataFrame()
df['Tag_Name'] = TAGS
df['Num_of_Questions'] = no_of_questions
df['Avg_View_Count'] = avg_view_count
df['Avg_Fav_Count'] = avg_fav_count
df.to_csv('StatsPerTag.csv', index= False)
df

# %% [markdown]
# # Stats per platform

# %%
sum = 0
no_of_questions = []
no_of_accepted_answers = []
avg_view_count = []
avg_fav_count = []
avg_score = []
for platform in PLATFORMS:
    indicesToRemove = []
    for i in range(len(so_df)):
        qtags = so_df.iloc[i]['Tags'][1:-1].replace('><', ' ').split()
        f = True
        for qtag in qtags:
            for ptag in PLATFORMS[platform]:
                if qtag == ptag:
                    f = False
                    break
        if f:
            indicesToRemove.append(i)
    temp_df = so_df.drop(index=indicesToRemove)
    no_of_questions.append(len(temp_df))
    no_of_accepted_answers.append(temp_df.AcceptedAnswer.count())
    avg_view_count.append(temp_df.ViewCount.mean())
    avg_fav_count.append(temp_df.FavoriteCount.mean())
    avg_score.append(temp_df.Score.mean())
    sum += len(temp_df)
print(sum)
df = pd.DataFrame()
df['Platform'] = PLATFORMS.keys()
df['Num_of_Questions'] = no_of_questions
df['Num_of_Accepted_Answers'] = no_of_accepted_answers
df['Avg_View_Count'] = avg_view_count
df['Avg_Fav_Count'] = avg_fav_count
df['Avg_Score'] = avg_score
df.to_csv('StatsPerPlatform.csv', index= False)
df

# %% [markdown]
# # Platform related figures

# %%
SAMPLING = '3M'
DUMMY_DATE = pd.to_datetime('2008-11-27 18:18:37.777')

final_df = so_df.resample(SAMPLING, on="CreationDate").count()[['Id']]
final_df.columns = ['Total']
for platform in PLATFORMS:
    indicesToRemove = []
    for i in range(len(so_df)):
        # if so_df.iloc[i]['CreationDate'] == DUMMY_DATE:
        #     continue
        qtags = so_df.iloc[i]['Tags'][1:-1].replace('><', ' ').split()
        f = True
        for qtag in qtags:
            for ptag in PLATFORMS[platform]:
                if qtag == ptag:
                    f = False
                    break
        if f:
            indicesToRemove.append(i)
    temp_df = so_df.drop(index=indicesToRemove)
    # dummy date for resampling start
    temp_df = temp_df.append(pd.Series(data=[DUMMY_DATE], index = ['CreationDate']), ignore_index=True)
    temp_df = temp_df.resample(SAMPLING, on = "CreationDate").count()[['Id']]
    temp_df.columns = [platform]
    final_df = final_df.merge(temp_df, how='left', on='CreationDate', validate='one_to_one')

final_df.fillna(0, inplace=True)
final_df = final_df.astype('int64')
# final_df.to_csv('trend.csv')

# integrity check
for i in range(len(final_df)):
    sum = 0
    for platform in PLATFORMS:
        sum += final_df.iloc[i][platform]
    if(final_df.iloc[i].Total != sum):
        print('Failed')

print(len(final_df))
final_df


# %%
final_df.drop(columns='Total').plot(figsize=(10,6))
plt.xlabel('Year')
plt.ylabel('# of Questions')
plt.grid()
plt.savefig('platform_Per_Three_Month.png', dpi=1000)
plt.show()


# %%
final_df.plot(figsize=(10,6))
plt.xlabel('Year')
plt.ylabel('# of Questions')
plt.grid()
plt.savefig('platform_Per_Three_Month_With_Total.png', dpi=1000)
plt.show()

# %% [markdown]
# # Topic modeling related figures

# %%
TOPIC_ID_LOW_CATEGORY = {
    0 : 'Data Storage & Migration',
    1 : 'Dynamic Form Controller',
    2 : 'Access Control & Security',
    3 : 'SQL CRUD',
    4 :	'Entity Relationship Management',
    5 : 'UI Adaptation',
    6 :	'External Web Req Processing',
    7 :	'External API & Email Config',
    8 :	'Dynamic Content Binding',
    9 : 'Cloud and On-Prem Conf',
    10 : 'Dynamic Content Display',
    11 : 'Client Server Comm & IO',
    12 : 'Dynamic Event Handling'
}

TOPIC_ID_SUB_CATEGORY = {
    0 : 'Migration',
    1 : 'UI',
    2 : 'Configuration',
    3 : 'Management',
    4 :	'Management',
    5 : 'UI',
    6 :	'',
    7 :	'',
    8 :	'Middleware',
    9 : 'Configuration',
    10 : 'Middleware',
    11 : '',
    12 : 'Middleware'
}

TOPIC_ID_HIGHER_CATEGORY = {
    0 : 'Database',
    1 : 'Customization',
    2 : 'Adoption',
    3 : 'Database',
    4 :	'Database',
    5 : 'Customization',
    6 :	'Integration',
    7 :	'Integration',
    8 :	'Customization',
    9 : 'Adoption',
    10 : 'Customization',
    11 : 'Adoption',
    12 : 'Customization'
}

HIGHER_CAT_TO_TOPIC_ID = {
    'Database' : [0, 3, 4],
    'Customization' : [1, 5, 8, 10, 12],
    'Adoption' : [2, 9, 11],
    'Integration' : [6, 7]
}


# %%
def linkToId(x):
    '''
    Takes a excel styled link and retures the QuestionID
    '''
    return int(x.split('"')[::-1][1])


def make_link(id, type):
    '''
    returns stackoverflow url string of question/answer in hyperlink format for CSV/EXCEL
    id = postid
    type : 'q' for question
           'a' for answer
    '''
    url = f'https://stackoverflow.com/{type}/{id}'
    return f'=HYPERLINK("{url}", "{id}")'


# %%
SAMPLING = '6M'
DUMMY_DATE = pd.to_datetime('2008-11-27 18:18:37.777')

final_df = so_df.resample(SAMPLING, on='CreationDate').count()[['Id']]
final_df.columns = ['Total']
for category in HIGHER_CAT_TO_TOPIC_ID:
    idsToRetain = []
    for topic_id in HIGHER_CAT_TO_TOPIC_ID[category]:
        temp_df = pd.read_csv(f'./TopicToPost/{topic_id}/Questions.csv')
        idsToRetain.extend(temp_df.link.apply(linkToId).tolist())
    temp_df = so_df[so_df['Id'].isin(idsToRetain)]
    # dummy date for resampling start
    temp_df = temp_df.append(pd.Series(data=[DUMMY_DATE], index = ['CreationDate']), ignore_index=True)
    temp_df = temp_df.resample(SAMPLING, on = 'CreationDate').count()[['Id']]
    temp_df.columns = [category]
    final_df = final_df.merge(temp_df, how='left', on='CreationDate', validate='one_to_one')

final_df.fillna(0, inplace=True)
final_df = final_df.astype('int64')
# final_df.to_csv(f'TopicModelingTrend_HighLevel_Sampling({SAMPLING}).csv')

# integrity check
for i in range(len(final_df)):
    sum = 0
    for category in HIGHER_CAT_TO_TOPIC_ID:
        sum += final_df.iloc[i][category]
    if(final_df.iloc[i].Total != sum):
        print('Failed')
        
print(len(final_df))
final_df


# %%
ax = final_df.drop(columns='Total').plot(figsize=(10,6))
plt.xlabel('Year')
plt.ylabel('# of Questions')

ax.set_xticklabels([x.strftime("%Y-%m") for x in final_df.index], rotation=45)
plt.grid()
ax.set_xticklabels(['xyz 2009','xyz 2011','xyz 2013','xyz 2015','xyz 2017','xyz 2019'], rotation=0)
plt.savefig('Topic_Modeling_Higher_Cat_Per_Six_Month.png', dpi=1000)
plt.show()


# %%
final_df.plot(figsize=(10,6))
plt.xlabel('Year')
plt.ylabel('# of Questions')
plt.grid()
plt.savefig('Topic_Modeling_Higher_Cat_Per_Six_Month_With_Total.png', dpi=1000)
plt.show()

# %% [markdown]
# # Topic Modeling Stats
# 
# Gias:   Create   a   table   with   the   followingcolumns:  
# - Topic  Category,  
# - Topic  Name,
# -  Posts  (two  columns):
#     - Number  and  
#     - Percentage  of  Posts
# - Popularity  score  (threecolumns) 
#     - Avg View, 
#     - Avg Favorite,
#     - Avg Score,
# - Difficulty Score
#     - Pct Questions without  an accepted answer
#     - Median hours to get  an  accepted  answer  per  question

# %%



# %%
# total post = total questions + total accepted answers
TOTAL_POSTS = len(so_df) + so_df.AcceptedAnswer.count()

all_view_counts = []
all_fav_counts = []
all_score_count = []

number_of_posts = []
percentage_of_posts = []
avg_view = []
avg_favorite = []
avg_score = []
pct_questions_without_accepted_answer = []
median_hours_to_get_accepted_answer = []
for topic_id in TOPIC_ID_LOW_CATEGORY:
    idsToRetain = []
    temp_df = pd.read_csv(f'./TopicToPost/{topic_id}/Questions.csv')
    idsToRetain.extend(temp_df.link.apply(linkToId).tolist())
    temp_ans_df = pd.read_csv(f'./TopicToPost/{topic_id}/Answers.csv')
    temp_df = so_df[so_df['Id'].isin(idsToRetain)]
    post_cnt = len(temp_df) + len(temp_ans_df)
    number_of_posts.append(post_cnt)
    percentage_of_posts.append(round(((post_cnt/TOTAL_POSTS)*100.0), 2))
    avg_view.append(round(temp_df.ViewCount.mean(), 2))
    all_view_counts.extend(temp_df.ViewCount.to_list())
    avg_favorite.append(round(temp_df.FavoriteCount.mean(), 2))
    all_fav_counts.extend(temp_df.FavoriteCount.to_list())
    avg_score.append(round(temp_df.Score.mean(), 2))
    all_score_count.extend(temp_df.Score.to_list())
    pct_questions_without_accepted_answer.append(
        round((((len(temp_df)-temp_df.AcceptedAnswer.count())/len(temp_df))*100.0), 2))
    # median hours
    temp_median_df = temp_df[temp_df['AcceptedAnswer'].notnull(
    )][['CreationDate', 'AcceptedAnswerCreationDate']]
    temp_median_df['Diff_Hour'] = (
        temp_median_df.AcceptedAnswerCreationDate - temp_median_df.CreationDate) / pd.Timedelta(hours=1)
    median_hours_to_get_accepted_answer.append(
        round(temp_median_df.Diff_Hour.median(), 2))
    # print(len(temp_df), len(questions_with_accepted_answers))

df = pd.DataFrame()
df['Topic_ID'] = TOPIC_ID_LOW_CATEGORY.keys()
df['Topic_Name'] = TOPIC_ID_LOW_CATEGORY.values()
df['Number_of_Posts(Q+A)'] = number_of_posts
df['Percentage_of_Posts'] = percentage_of_posts
df['Averege_View'] = avg_view
df['AVerege_Favorite'] = avg_favorite
df['Averege_Score'] = avg_score
df['Pct_Questions_without_Accepted_Answer'] = pct_questions_without_accepted_answer
df['Median_Hours_To_Get_Accepted_Answer'] = median_hours_to_get_accepted_answer
df.to_csv('Stats_Topic_Modeling_Low_Level.csv', index=False)
df


# %%
import math
# all_fav_counts = [0 if math.isnan(x) else x for x in all_fav_counts]

all_fav_counts =[value for value in all_fav_counts if not math.isnan(value)]

print('acg view')
print(sum(all_view_counts)/len(all_view_counts))

print('avg fav')
print(sum(all_fav_counts)/len(all_fav_counts))

print('avg score')
print(sum(all_score_count)/len(all_score_count))

# %% [markdown]
# # Labelled Data
# 
# ## sheet 1: challenge_id, question_id, challenge_label, challenge_category, sdlc.
# 
# ## Sheet 2: “question_id, challenge id, topic id, topic label, topic category”
# %% [markdown]
# ## Sheet 1: challenge_id,  challenge_label, question_id, sdlc
# ## Sheet 2: question_id, challenge id, challenge_label, topic id, topic label, topic category

# %%
label_df = pd.read_csv('so_labelling_data.csv')
label_df = label_df[label_df.Tag1.notna()]
print(len(label_df))
print(label_df.SDLC.notna().count())
label_df.SDLC= label_df.SDLC.astype(str)
label_df.Tag1= label_df.Tag1.astype(str)
label_df.Tag2= label_df.Tag2.fillna('')
label_df.Tag2= label_df.Tag2.astype(str)
label_df


# %%
from collections import defaultdict

tagFreq = defaultdict(int)
for item in label_df.Tag1.value_counts().iteritems():
    tagFreq[item[0]] += item[1]
for item in label_df.Tag2.value_counts().iteritems():
    tagFreq[item[0]] += item[1]
for item in tagFreq.items():
    print(item)
challengeDict = {}
cnt = 0
for item in tagFreq.items():
    if item[0] != '':
        challengeDict[item[0]] = cnt
        cnt += 1


# %%
questionsUnderTopic = {}
for topic_id in TOPIC_ID_LOW_CATEGORY:
    temp_df = pd.read_csv(f'./TopicToPost/{topic_id}/Questions.csv')
    questionsUnderTopic[topic_id] = set(temp_df.link.apply(linkToId).tolist())


# %%
challenge_ids = [] #DDD
challenge_labels = [] #DDD
question_ids = [] #DDD
sdlcs = [] #DDD
topic_ids = [] #DDD
topic_labels = [] ###
topic_categorys = [] ###
cnt = 0
for i in range(len(label_df)):
    lc = 1
    if label_df.iloc[i].Tag2 != '':
        lc = 2
    for _ in range(lc):
        question_ids.append(label_df.iloc[i].Id)
        sdlcs.append(label_df.iloc[i].SDLC[3:].capitalize())
        topic_id_for_q = -1
        for tid in questionsUnderTopic:
            if label_df.iloc[i].Id in questionsUnderTopic[tid]:
                topic_id_for_q = tid
                break
        topic_ids.append(topic_id_for_q)
        topic_labels.append(TOPIC_ID_LOW_CATEGORY[topic_id_for_q])
        topic_categorys.append(TOPIC_ID_HIGHER_CATEGORY[topic_id_for_q])
    challenge_ids.append(challengeDict[label_df.iloc[i].Tag1])
    challenge_labels.append(label_df.iloc[i].Tag1)
    if lc == 2:
        challenge_ids.append(challengeDict[label_df.iloc[i].Tag2])
        challenge_labels.append(label_df.iloc[i].Tag2)
df = pd.DataFrame()
df['Challenge_Id'] = challenge_ids
df['Challenge_Label'] = challenge_labels
df['Question_id'] = question_ids
df['SDLC'] = sdlcs
df.to_csv('sheet1.csv', index=False)
df

df2 = pd.DataFrame()
df2['Question_id'] = question_ids
df2['Question_id'] = df2['Question_id'].apply(lambda x : make_link(x,'q'))
df2['Challenge_Id'] = challenge_ids
df2['Challenge_Label'] = challenge_labels
df2['Topic_Id'] = topic_ids
df2['Topic_Label'] = topic_labels
df2['Topic_Category'] = topic_categorys
df2.to_csv('sheet2.csv', index=False)
df2


# %%
## Sheet 1: challenge_id,  challenge_label, question_id, sdlc
## Sheet 2: question_id, challenge id, challenge_label, topic id, topic label, topic category


# %%
challengeDict

# %% [markdown]
# # Sheet1: topic, topic category, date, total question, total accepted answer#

# %%
DUMMY_DATE = pd.to_datetime('2008-11-27 18:18:37.777')

result_df = pd.DataFrame()

for high_cat in HIGHER_CAT_TO_TOPIC_ID:
    for topic_id in HIGHER_CAT_TO_TOPIC_ID[high_cat]:
        idsToRetain = []
        temp_df = pd.read_csv(f'./TopicToPost/{topic_id}/Questions.csv')
        idsToRetain.extend(temp_df.link.apply(linkToId).tolist())
        temp_ans_df = pd.read_csv(f'./TopicToPost/{topic_id}/Answers.csv')
        temp_qs_df = so_df[so_df['Id'].isin(idsToRetain)]
        temp_qs_df = temp_qs_df[['Id', 'CreationDate']]
        temp_qs_df = temp_qs_df.append(pd.Series(data=[DUMMY_DATE], index = ['CreationDate']), ignore_index=True)
        final_df = temp_qs_df.resample('MS', on='CreationDate').count()[['Id']]
        final_df.columns = ['Question_Cnt']
        # print(final_df)
        temp_ans_df = so_df[so_df['Id'].isin(temp_ans_df.link.apply(linkToId).tolist())]
        temp_ans_df = temp_ans_df[['AcceptedAnswerId','AcceptedAnswerCreationDate']]
        temp_ans_df.columns = ['Id','CreationDate']
        temp_ans_df = temp_ans_df.append(pd.Series(data=[DUMMY_DATE], index = ['CreationDate']), ignore_index=True)
        final_df_a = temp_ans_df.resample('MS', on='CreationDate').count()[['Id']]
        final_df_a.columns = ['Answer_Cnt']
        final_df = final_df.merge(final_df_a, how='left', on='CreationDate', validate='one_to_one')
        # topic.append(TOPIC_ID_HIGHER_CATEGORY[topic_id])
        # topic_id_col.append(topic_id)
        # topic_name_col.append(TOPIC_ID_LOW_CATEGORY[topic_id])
        # total_ques_col.append()
        final_df['Topic Id'] = topic_id
        final_df['Topic_Name_Low'] = TOPIC_ID_LOW_CATEGORY[topic_id]
        final_df['Topic_Name_High'] = TOPIC_ID_HIGHER_CATEGORY[topic_id]
        result_df = result_df.append(final_df)
    

result_df.fillna(0, inplace=True)
result_df.Question_Cnt = result_df.Answer_Cnt.astype('int64')
result_df.Answer_Cnt = result_df.Answer_Cnt.astype('int64')
result_df.to_csv('SheetXXXX.csv')

# %% [markdown]
# # Sheet 2: platform, date, total question, total accepted answer, total answer

# %%
DUMMY_DATE = pd.to_datetime('2008-11-27 18:18:37.777')


result_df = pd.DataFrame()


for platform in PLATFORMS:
    indicesToRemove = []
    for i in range(len(so_df)):
        qtags = so_df.iloc[i]['Tags'][1:-1].replace('><', ' ').split()
        f = True
        for qtag in qtags:
            for ptag in PLATFORMS[platform]:
                if qtag == ptag:
                    f = False
                    break
        if f:
            indicesToRemove.append(i)
    temp_df_q = so_df.drop(index=indicesToRemove)
    # temp_df_a = so_df[so_df['Id'].isin(temp_df_q.Id.tolist())]
    temp_df_a = temp_df_q[['AcceptedAnswerId','AcceptedAnswerCreationDate']]

    temp_df_q = temp_df_q.append(pd.Series(data=[DUMMY_DATE], index = ['CreationDate']), ignore_index=True)
    final_df = temp_df_q.resample('MS', on='CreationDate').count()[['Id']]
    final_df.columns = ['Question_Cnt']

    # temp_df_q = temp_df_q[['Id','CreationDate']]
    temp_df_a.columns = ['Id','CreationDate']

    temp_df_a = temp_df_a.append(pd.Series(data=[DUMMY_DATE], index = ['CreationDate']), ignore_index=True)
    temp_df_a = temp_df_a.resample('MS', on='CreationDate').count()[['Id']]
    temp_df_a.columns = ['Answer_Cnt']
    final_df = final_df.merge(temp_df_a, how='left', on='CreationDate', validate='one_to_one')
    # temp_df_q = temp_df.resample('MS',on='CreationDate').sum()[['AnswerCount']]
    final_df['Platform_Name'] = platform
    result_df = result_df.append(final_df)
    


# %%
result_df.to_csv('Sheet_Platform_PerMonth.csv')

# %% [markdown]
# # spreadsheet1 below:
# 
# # Post id, post type (1 for Question, 2 for answer), AcceptedAnswerId (null if post is an answer), score, view count, favorite count, question_title (if post is a question), post creation time
# 
# 

# %%
acceptedAnswerIds = so_df.AcceptedAnswerId.dropna().astype('int64').tolist()
so_accepted_df = so_ans_df[so_ans_df['Id'].isin(acceptedAnswerIds)]
final_df = so_df.drop(columns=['AcceptedAnswer','AcceptedAnswerCreationDate']).append(so_accepted_df)
final_df = final_df[['Id','PostTypeId','AcceptedAnswerId','Score','ViewCount','FavoriteCount','Title','CreationDate']]
final_df.columns = ['Post_id','Post_type','AcceptedAnswerId','Score','ViewCount','FavoriteCount','Question_Title','Post_Creation_Date']
final_df.to_csv('spreadsheet1.csv', index= False)
final_df


# %%
final_df.Score.sum()

# %% [markdown]
# # Spreadsheet 2 contains mapping of post information to the generated topics. It should have the following sheets:
# # Sheet1. Topic ID, Topic Label, Topic Category, Month-Year (e.g., for Jan 2020, it would be 01-01-2020), Total questions created in Month-Year, Total accepted answers created in Month-Year, Total answer created in Month-Year, Total view, Total favorite, Total score

# %%
# sheet 1
DUMMY_DATE = pd.to_datetime('2008-11-27 18:18:37.777')
result_df = pd.DataFrame()

for high_cat in HIGHER_CAT_TO_TOPIC_ID:
    for topic_id in HIGHER_CAT_TO_TOPIC_ID[high_cat]:
        temp_df = pd.read_csv(f'./TopicToPost/{topic_id}/Questions.csv')
        idsToRetain = temp_df.link.apply(linkToId).tolist()
        temp_ans_df = pd.read_csv(f'./TopicToPost/{topic_id}/Answers.csv')
        temp_qs_df = so_df[so_df['Id'].isin(idsToRetain)]
        temp_qs_df = temp_qs_df.append(pd.Series(data=[DUMMY_DATE], index = ['CreationDate']), ignore_index=True)
        # print(len(temp_qs_df))
        idsToRetain = temp_ans_df.link.apply(linkToId).tolist()
        temp_df = so_df[so_df['Id'].isin(idsToRetain)]
        idsToRetain = temp_df.AcceptedAnswerId.astype('int64').tolist()
        temp_ans_df = so_ans_df[so_ans_df['Id'].isin(idsToRetain)]
        temp_ans_df = temp_ans_df.append(pd.Series(data=[DUMMY_DATE], index = ['CreationDate']), ignore_index=True)
        # print(len(temp_ans_df))
        # temp_qs_df = temp_qs_df[['Id', 'CreationDate']]
        final_df = temp_qs_df.resample('MS', on='CreationDate').count()[['Id']]
        final_df.columns = ['Question_Cnt']
        # print(final_df.Question_Cnt.sum())
        
        temp_df = temp_ans_df.resample('MS', on='CreationDate').count()[['Id']]
        temp_df.columns = ['Answer_Cnt']
        final_df = final_df.merge(temp_df, how='left', on='CreationDate', validate='one_to_one')

        temp_qs_df.ViewCount.fillna(0, inplace=True)
        temp_qs_df.ViewCount = temp_qs_df.ViewCount.astype('int64')
        temp_df = temp_qs_df.resample('MS', on='CreationDate').sum()['ViewCount']
        temp_df.columns = ['Total_view']
        final_df = final_df.merge(temp_df, how='left', on='CreationDate', validate='one_to_one')

        temp_qs_df.FavoriteCount.fillna(0, inplace=True)
        temp_qs_df.FavoriteCount = temp_qs_df.FavoriteCount.astype('int64')
        temp_df = temp_qs_df.resample('MS', on='CreationDate').sum()['FavoriteCount']
        temp_df.columns = ['Total_favorite']
        final_df = final_df.merge(temp_df, how='left', on='CreationDate', validate='one_to_one')

        temp_qs_df.Score.fillna(0, inplace=True)
        temp_qs_df.Score = temp_qs_df.Score.astype('int64')
        temp_ans_df.Score.fillna(0, inplace=True)
        temp_ans_df.Score = temp_ans_df.Score.astype('int64')
        temp_qs_df = temp_qs_df.append(temp_ans_df)
        temp_df = temp_qs_df.resample('MS', on='CreationDate').sum()['Score']
        temp_df.columns = ['Total_Score']
        final_df = final_df.merge(temp_df, how='left', on='CreationDate', validate='one_to_one')

        final_df['Topic_Id'] = topic_id
        final_df['Topic_Label'] = TOPIC_ID_LOW_CATEGORY[topic_id]
        final_df['Topic_Category'] = TOPIC_ID_HIGHER_CATEGORY[topic_id]
        # print(final_df)
        result_df = result_df.append(final_df)
        # print(result_df)
result_df.to_csv('Spreadsheet2_Topic.csv')


# %%
result_df.Score.sum()

# %% [markdown]
# # Sheet 2. Month-Year, Platform (e.g., Google app maker), total question created in Month-year for Platform, total answer created in Month-year, total accepted answer created in Month-Year, Total view count, Total favorite count, Total score

# %%
DUMMY_DATE = pd.to_datetime('2008-11-27 18:18:37.777')


result_df = pd.DataFrame()


for platform in PLATFORMS:
    indicesToRemove = []
    for i in range(len(so_df)):
        qtags = so_df.iloc[i]['Tags'][1:-1].replace('><', ' ').split()
        f = True
        for qtag in qtags:
            for ptag in PLATFORMS[platform]:
                if qtag == ptag:
                    f = False
                    break
        if f:
            indicesToRemove.append(i)
    temp_qs_df = so_df.drop(index=indicesToRemove)
    temp_qs_df = temp_qs_df.append(pd.Series(data=[DUMMY_DATE], index = ['CreationDate']), ignore_index=True)

    questionIds = temp_qs_df.Id.astype('int64').tolist()
    acceptedAnswerIds = temp_qs_df.AcceptedAnswerId.dropna().astype('int64').tolist()
    # print(len(acceptedAnswerIds))
    # print(len(temp_qs_df))
    temp_ans_df = so_ans_df[so_ans_df['ParentId'].isin(questionIds)]
    temp_acc_ans_df = temp_ans_df[temp_ans_df['Id'].isin(acceptedAnswerIds)]
    # print(len(temp_ans_df))
    # print(len(temp_acc_ans_df))

    final_df = temp_qs_df.resample('MS', on='CreationDate').count()[['Id']]
    final_df.columns = ['Question_Cnt']

    temp_df = temp_ans_df.resample('MS', on='CreationDate').count()[['Id']]
    temp_df.columns = ['Answer_Cnt']
    final_df = final_df.merge(temp_df, how='left', on='CreationDate', validate='one_to_one')

    temp_df = temp_acc_ans_df.resample('MS', on='CreationDate').count()[['Id']]
    temp_df.columns = ['Accepted_Answer_Cnt']
    final_df = final_df.merge(temp_df, how='left', on='CreationDate', validate='one_to_one')

    temp_qs_df.ViewCount.fillna(0, inplace=True)
    temp_qs_df.ViewCount = temp_qs_df.ViewCount.astype('int64')
    temp_df = temp_qs_df.resample('MS', on='CreationDate').sum()['ViewCount']
    temp_df.columns = ['Total_View_Cnt']
    print(temp_df)
    final_df = final_df.merge(temp_df, how='left', on='CreationDate', validate='one_to_one')

    temp_qs_df.FavoriteCount.fillna(0, inplace=True)
    temp_qs_df.FavoriteCount = temp_qs_df.FavoriteCount.astype('int64')
    temp_df = temp_qs_df.resample('MS', on='CreationDate').sum()['FavoriteCount']
    temp_df.columns = ['Total_Favorite_Cnt']
    final_df = final_df.merge(temp_df, how='left', on='CreationDate', validate='one_to_one')

    temp_qs_df.Score.fillna(0, inplace=True)
    temp_qs_df.Score = temp_qs_df.Score.astype('int64')
    temp_ans_df.Score.fillna(0, inplace=True)
    temp_ans_df.Score = temp_ans_df.Score.astype('int64')
    temp_qs_df = temp_qs_df.append(temp_ans_df)
    temp_df = temp_qs_df.resample('MS', on='CreationDate').sum()['Score']
    temp_df.columns = ['Total_Score_Cnt']
    final_df = final_df.merge(temp_df, how='left', on='CreationDate', validate='one_to_one')

    final_df['Platform_Name'] = platform
    result_df = result_df.append(final_df)

result_df.fillna(0, inplace= True)
result_df.Answer_Cnt = result_df.Answer_Cnt.astype('int64')
result_df.Accepted_Answer_Cnt = result_df.Accepted_Answer_Cnt.astype('int64')
result_df.Score = result_df.Score.astype('int64')
result_df.to_csv('Spreadsheet2_Platform.csv')


# %%
result_df


# %%
result_df.Score.sum()


# %%
ttt = so_df[so_df.AnswerCount==0]
ttt.AnswerCount
len(ttt)


# %%



