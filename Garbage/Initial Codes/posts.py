import xml.etree.ElementTree as ET
import csv

FILE = 'Posts.xml'
TAGS = ['google-app-maker', 'appian', 'outsystems', 'zoho', 'mendix',
        'powerapps', 'quickbase', 'vinyl', 'salesforce-lightning']
COLS = ['Id', 'PostTypeId', 'AcceptedAnswerId', 'CreationDate', 'Score', 'ViewCount', 'Body', 'OwnerUserId', 'LastEditorUserId',
        'LastEditorDisplayName', 'LastEditDate', 'LastActivityDate', 'Title', 'Tags', 'AnswerCount', 'CommentCount', 'FavoriteCount', 'ContentLicense']

context = ET.iterparse(FILE, events=("start", "end"),
                       parser=ET.XMLParser(encoding='utf-8'))

with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(COLS)
    _, root = next(context)
    for event, elem in context:
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
