import xml.etree.ElementTree as ET
import pandas as pd
import csv

FILE = 'Posts.xml'
COLS = ['Id', 'PostTypeId', 'AcceptedAnswerId', 'CreationDate', 'Score', 'ViewCount', 'Body', 'OwnerUserId', 'LastEditorUserId',
        'LastEditorDisplayName', 'LastEditDate', 'LastActivityDate', 'Title', 'Tags', 'AnswerCount', 'CommentCount', 'FavoriteCount', 'ContentLicense','AcceptedAnswer']

def updater(header, data, filename):
        with open (filename, "w", newline = "", encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = header)
            writer.writeheader()
            writer.writerows(data)



# list of acceptedanswerId extraction from targeted questions' file
#The copy of output.csv file is used as output_with_answers.csv to add answers to it
data = pd.read_csv('output_with_answers.csv') # skip header row
df = pd.DataFrame(data)
ansIdLst={}
for index, row in df.iterrows():
    # access data using column names
    temp=row['AcceptedAnswerId']
    # collect only not nan vlues with indexes
    if not (temp != temp) :
        ansIdLst[int(temp)]=index

print(len(ansIdLst))



context = ET.iterparse(FILE, events=("start", "end"),
                       parser=ET.XMLParser(encoding='utf-8'))

with open('output_with_answers.csv', newline='', encoding='utf-8') as file:
    readData = [row for row in csv.DictReader(file)]
    _, root = next(context)
    for event, elem in context:
        if event == "end" and elem.tag == "row":
            # candidate Id for answerpost
            ansId = int(elem.attrib.get('Id', 'None'))
            if ansId in ansIdLst:  
                #readData[index]['AnswerText']=body of answer
                index=ansIdLst[ansId]
                readData[index]['AcceptedAnswer'] =elem.attrib.get("Body", '')
                readHeader = readData[index].keys()
                updater(readHeader, readData, 'output_with_answers.csv') 
            # progress
            if int(elem.attrib['Id']) % 100000 == 0:
                print('done', elem.attrib['Id'])
            elem.clear()
            root.clear()   
    