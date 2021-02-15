import pandas as pd
import numpy as np

df = pd.read_csv("so_data.csv")
df = df[['Id', 'Body', 'Title']]
df['titlePlusQuestion'] = df[['Title', 'Body']].apply(
    lambda x: ' '.join(x), axis=1)
df = df.drop(['Title', 'Body'], axis=1)
df.columns = ['id', 'raw']
df.insert(1, 'qa', 'q')
df.to_csv('so_body.csv', index=False)
