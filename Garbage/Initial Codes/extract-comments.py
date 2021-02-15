import xml.etree.ElementTree as ET
import pandas as pd
import csv

FILE = 'Comments.xml'
TAGS = ['google-app-maker', 'appian', 'outsystems', 'zoho', 'mendix',
        'powerapps', 'quickbase', 'vinyl', 'salesforce-lightning']
COLS = ['Id', 'PostId', 'Score', 'Text', 'CreationDate','UserId','ContentLicense']
#CHANGED_COLS=['ansId', 'PostId', 'ansScore', 'Text', 'ansCreationDate','UserId','ansContentLicense']

data = pd.read_csv('output.csv') # skip header row
df = pd.DataFrame(data)
x=df.iloc[:,0].dropna()
queIdLst=set(x)
print(len(queIdLst))
# print(ansIdLst)

context = ET.iterparse(FILE, events=("start", "end"),
                       parser=ET.XMLParser(encoding='utf-8'))

with open('outputComment.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(COLS)
    _, root = next(context)
    for event, elem in context:
        if event == "end" and elem.tag == "row":
            queId = elem.attrib.get('PostId', 'None')
            # searching for candidate comment who has PostId same as Id of post.xml(output.csv)
            if int(queId) in queIdLst:    
                data = []
                for col in COLS:
                    data.append(elem.attrib.get(col, ''))
                csvwriter.writerow(data)
            # progress
            if int(elem.attrib['Id']) % 100000 == 0:
                print('done', elem.attrib['Id'])
            elem.clear()
            root.clear()