from rollcall import app, members
from os import path, getcwd, makedirs
from glob import glob
from csv import DictReader


def setupDirs():
    dataDir = path.join(getcwd(), 'data')
    app.config['DATA'] = dataDir
    makedirs(dataDir, exist_ok=True)
    makedirs(path.join(dataDir, 'faces'), exist_ok=True)


def getMembers():
    global members
    for file in glob(path.join(app.config['DATA'], '*.csv')):
        with open(path.join(app.config['DATA'], file) ) as f:
            reader = DictReader(f, quotechar='"')
            for row in reader:
                memberId = row['Mem No'].replace('\t','')
                memberId = f'{int(memberId):06d}'
                if not memberId in members.keys():
                    members[memberId] = { 
                        'id': memberId,
                        'altid': row['SA Identity No'].replace('\t',''),
                        'name': row['Preferred Name'].replace('\t',''),
                        'surname': row['Surname'].replace('\t',''),
                        'language': row['Language'].replace('\t','')[0:1],
                        'email': row['E-mail address'].replace('\t',''),
                        'phone': row['Mobile No'].replace('\t','')
                        }

