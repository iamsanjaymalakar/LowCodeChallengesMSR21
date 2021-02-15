import pandas as pd

def make_link(id,type):
    '''
    id = postid
    type : 'q' for question
           'a' for answer
    '''
    url = f'https://stackoverflow.com/{type}/{id}'
    return f'=HYPERLINK("{url}", "{id}")'

df = pd.read_csv('Questions_removed_duplicates.csv')
df = df[['Id','Title','FavoriteCount','ViewCount']]
df['Id'] = df['Id'].apply(lambda x: make_link(x,'q'))
df.to_csv('QuestionsForLabelling.csv',index=False)