import xml.etree.ElementTree as ET
import csv
import pandas as pd

TAGSFILE = 'Tags.xml'

# initital tags we started with 
# top 9 low code platforms
TAGS = ['google-app-maker', 'appian', 'outsystems', 'zoho', 'mendix',
        'powerapps', 'quickbase', 'vinyl', 'salesforce-lightning']

tagsIter = ET.iterparse(TAGSFILE, events=("start", "end"),
                        parser=ET.XMLParser(encoding='utf-8'))
                        

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

print(TAGS)