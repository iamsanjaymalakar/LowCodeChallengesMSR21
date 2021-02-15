import pandas as pd


def make_link(id, type):
    '''
    returns stackoverflow url string of question/answer in hyperlink format for CSV/EXCEL
    id = postid
    type : 'q' for question
           'a' for answer
    '''
    url = f'https://stackoverflow.com/{type}/{id}'
    return f'=HYPERLINK("{url}", "{id}")'


new_df = pd.read_csv('Ver_4__Questions_removed_duplicates.csv')
new_df = new_df[['Id', 'Title', 'FavoriteCount', 'ViewCount']]
print('new_df len : ', len(new_df))
print('NaN in new_df \'Id\' : ', new_df.Id.isnull().sum())

old_df = pd.read_csv('oldLabelling.csv')
old_df = old_df[['Id', 'tag1', 'Tag2', 'Tag3', 'Tag4', 'isProblematic']]
print('\nold_df len : ', len(old_df))
print('NaN in old_df \'Id\' : ', old_df.Id.isnull().sum())
print('duplicate in old_df \'Id\' : ', len(
    old_df['Id'])-len(old_df['Id'].drop_duplicates()))
old_df.drop_duplicates('Id', inplace=True)
print('old_df len after removing duplicates: ', len(old_df))

merged_df = pd.merge(new_df, old_df, how='left',
                     on='Id', validate='one_to_one')
print('\nmerged df len ', len(merged_df))
merged_df['Id'] = merged_df['Id'].apply(lambda x: make_link(x,'q'))
merged_df.to_csv('QuestionsForLabelling.csv',index=False)
