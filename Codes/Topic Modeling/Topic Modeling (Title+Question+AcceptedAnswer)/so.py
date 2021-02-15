import pandas as pd
import numpy as np

df = pd.read_csv("so_data_with_acceptedanswers.csv")
df['AcceptedAnswer'] = df['AcceptedAnswer'].fillna('')
df['AcceptedAnswer'] = df['AcceptedAnswer'].astype(str)
print(df.head(10)['AcceptedAnswer'])
df = df[['Id', 'Body', 'Title', 'AcceptedAnswer']]
df['titlePlusQuestionPlusAcceptedAnswer'] = df[['Title', 'Body', 'AcceptedAnswer']].apply(
    lambda x: ' '.join(x), axis=1)
df = df.drop(['Title', 'Body', 'AcceptedAnswer'], axis=1)
df.columns = ['id', 'raw']
df.insert(1, 'qa', 'q')
print(len(df))
df.to_csv('so_body.csv', index=False)
