import xml.etree.ElementTree as ET
import pandas as pd
import csv

FILE = 'Posts.xml'
COLS = ['Id', 'PostTypeId', 'ParentId', 'CreationDate', 'Score', 'Body', 'OwnerUserId', 'LastEditorUserId',
         'LastEditDate', 'LastActivityDate', 'CommentCount', 'ContentLicense']

# list of acceptedanswerId extraction from targeted questions' file
data = pd.read_csv('output.csv') # skip header row
df = pd.DataFrame(data)
x=df.iloc[:,2].dropna()
ansIdLst=set(x)
print(len(ansIdLst))


context = ET.iterparse(FILE, events=("start", "end"),
                       parser=ET.XMLParser(encoding='utf-8'))

with open('outputAnswer.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(COLS)
    _, root = next(context)
    for event, elem in context:
        if event == "end" and elem.tag == "row":
            # candidate Id for answerpost
            ansId = elem.attrib.get('Id', 'None')
            if int(ansId) in ansIdLst:    
                data = []
                for col in COLS:
                    data.append(elem.attrib.get(col, ''))
                csvwriter.writerow(data)
            # progress
            if int(elem.attrib['Id']) % 100000 == 0:
                print('done', elem.attrib['Id'])
            elem.clear()
            root.clear()