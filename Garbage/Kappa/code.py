import csv
from collections import Counter
from sklearn.metrics import confusion_matrix, cohen_kappa_score

dictionary = {
    'empty': 0,
    'database': 1,
    'ui customization': 2,
    'integration': 3,
    'remote database connection': 4,
    'permission': 5,
    'deployment': 6,
    'limitation': 7,
    'concurrency': 8,
    'testing': 9,
    'dynamic': 10,
    'lack of features': 11,
    'data binding': 12,
    'bug/error': 13,
    'browser compatibility': 14,
    'embedding': 15
}

def get_key(val):
    for key, value in dictionary.items():
        if val == value:
            return key

NAMES = ['sanjay', 'tameem', 'sadia']
mat = [[], [], []]
for idx, name in enumerate(NAMES):
    print('*'*50 + name + '*'*50)
    with open(name+'.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        cnt = 0
        for row in csv_reader:
            if cnt == 0:
                cnt += 1
                continue
            mat[idx].append(dictionary[row['class'].strip().lower()])
            cnt += 1
        print('Total', cnt)
        print(mat[idx])
        counter = Counter()
        counter.update(mat[idx])
        for k, f in counter.most_common():
            print(get_key(k), f)
    print('*'*105)
    

for idx1, c1 in enumerate(NAMES):
    for idx2, c2 in enumerate(NAMES):
        if idx1 != idx2:
            confusion_matrix(mat[idx1], mat[idx2])
            print(c1, c2, cohen_kappa_score(mat[idx1], mat[idx2]))
