import xml.etree.ElementTree as ET
import csv
import pandas as pd

POSTSFILE = 'Posts.xml'
TAGSFILE = 'Tags.xml'
COMMNETSFILE = 'Comments.xml'
TAGS = ['google-app-maker', 'appian', 'outsystems', 'zoho', 'mendix',
        'powerapps', 'quickbase', 'vinyl', 'salesforce-lightning']
COLS = ['Id', 'AcceptedAnswerId', 'CreationDate', 'ViewCount', 'Title', 'Body',
        'LastActivityDate', 'Tags', 'AnswerCount', 'AcceptedAnswer']

postsIter = ET.iterparse(POSTSFILE, events=("start", "end"),
                         parser=ET.XMLParser(encoding='utf-8'))
tagsIter = ET.iterparse(TAGSFILE, events=("start", "end"),
                        parser=ET.XMLParser(encoding='utf-8'))
                        
'''
map = {}
_, root = next(tagsIter)
for event, elem in tagsIter:
    if event == "end" and elem.tag == "row":
        tagName = elem.attrib.get('TagName', 'None')
        count = elem.attrib.get('Count', 'None')
        map[tagName] = int(count)
        elem.clear()
        root.clear()
print('Tags.xml done')

for i in range(3):
    lineCount = 0
    newMap = {}
    currentSet = set()
    _, root = next(postsIter)
    for event, elem in postsIter:
        if event == 'end' and elem.tag == 'row':
            tags = elem.attrib.get('Tags', '')
            if len(tags) == 0:
                continue
            tags = tags.replace('<', '')[0:-1].split('>')
            for TAG in TAGS:
                if TAG in tags:
                    for tag in tags:
                        currentSet.add(tag)
                        if tag in newMap:
                            newMap[tag] += 1
                        else:
                            newMap[tag] = 1
                    lineCount = lineCount+1
                continue
            # progress
            if int(elem.attrib['Id']) % 100000 == 0:
                print('done', elem.attrib['Id'])
            elem.clear()
            root.clear()
    postsIter = ET.iterparse(POSTSFILE, events=("start", "end"),
                         parser=ET.XMLParser(encoding='utf-8'))

    for tag in currentSet:
        significance = newMap[tag]/map[tag]
        relevance = newMap[tag]/(lineCount-1)
        if significance < 0.2:
            continue
        if relevance >= 0.015:
            if tag not in TAGS:
                TAGS.append(tag)
        if relevance >= 0.01:
            if tag not in TAGS:
                TAGS.append(tag)
        if relevance >= 0.005:
            if tag not in TAGS:
                TAGS.append(tag)
    print(TAGS)
'''
TAGS = ['google-app-maker', 'appian', 'outsystems', 'zoho', 'mendix', 'powerapps', 'quickbase', 'vinyl', 'salesforce-lightning', 'powerapps-formula', 'lwc', 'lightning', 'powerapps-selected-items', 'powerapps-collection', 'salesforce-communities', 'powerapps-canvas', 'salesforce-chatter', 'salesforce-service-cloud', 'aura-framework']
print(TAGS)


with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(COLS)
    _, root = next(postsIter)
    for event, elem in postsIter:
        if event == "end" and elem.tag == "row":
            tags = elem.attrib.get('Tags', 'None')
            for tag in TAGS:
                if tag in tags:
                    data = []
                    for col in COLS:
                        data.append(elem.attrib.get(col, ''))
                    csvwriter.writerow(data)
                    continue
            # progress
            if int(elem.attrib['Id']) % 100000 == 0:
                print('done', elem.attrib['Id'])
            elem.clear()
            root.clear()


def updater(header, data, filename):
        with open (filename, "w", newline = "", encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = header)
            writer.writeheader()
            writer.writerows(data)


data = pd.read_csv('output.csv')
df = pd.DataFrame(data)
ansIdList={}
for index, row in df.iterrows():
    temp=row['AcceptedAnswerId']
    if not (temp != temp) :
        ansIdList[int(temp)]=index
print(len(ansIdList))


with open('output.csv', newline='', encoding='utf-8') as file:
    readData = [row for row in csv.DictReader(file)]
    _, root = next(postsIter)
    for event, elem in postsIter:
        if event == "end" and elem.tag == "row":
            ansId = int(elem.attrib.get('Id', 'None'))
            if ansId in ansIdList:  
                index=ansIdList[ansId]
                readData[index]['AcceptedAnswer'] =elem.attrib.get("Body", '')
                readHeader = readData[index].keys()
                updater(readHeader, readData, 'output.csv') 
            # progress
            if int(elem.attrib['Id']) % 100000 == 0:
                print('done', elem.attrib['Id'])
            elem.clear()
            root.clear()   