import xml.etree.ElementTree as ET
import csv

FILE = 'Tags.xml'

context = ET.iterparse(FILE, events=("start", "end"),
                       parser=ET.XMLParser(encoding='utf-8'))

map = {}
_, root = next(context)
for event, elem in context:
    if event == "end" and elem.tag == "row":
        tagName = elem.attrib.get('TagName', 'None')
        count = elem.attrib.get('Count', 'None')
        map[tagName] = int(count)

lineCount = 0
newMap = {}
currentSet = set()

with open('output.csv', newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        if lineCount == 0:
            lineCount += 1
            continue
        lineCount += 1
        tags = row['Tags']
        if len(tags) == 0:
            continue
        tags = tags.replace('<', '')
        tags = tags[0:len(tags)-1]
        tags = tags.split('>')
        for tag in tags:
            currentSet.add(tag)
            if tag in newMap:
                newMap[tag] += 1
            else:
                newMap[tag] = 1

low = []
med = []
high = []

for tag in currentSet:
    significance = newMap[tag]/map[tag]
    relevance = newMap[tag]/(lineCount-1)
    if significance < 0.2:
        continue
    if relevance >= 0.015:
        high.append(tag)
    if relevance >= 0.01:
        med.append(tag)
    if relevance >= 0.005:
        low.append(tag)

print('(0.2, 0.015)')
s = ' '
print(s.join(high))
print(len(high))

print('(0.2, 0.01)')
print(s.join(med))
print(len(med))

print('(0.2, 0.005)')
print(s.join(low))
print(len(low))