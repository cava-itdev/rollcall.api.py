from rollcall import app, members, altIds
from os import path, getcwd, makedirs
from glob import glob
from csv import DictReader
import datetime as dt


def setupDirs():
    dataDir = path.join(getcwd(), 'data')
    app.config['DATA'] = dataDir
    makedirs(dataDir, exist_ok=True)
    makedirs(path.join(dataDir, 'faces'), exist_ok=True)
    return dataDir


def getAllMembers():
    '''Reads all members into a global dictionary
    Output:
        - dictionary of all members, keyed by member ID
        - dictionary of member IDs, keyed by altId
    '''
    global members, altIds
    for file in glob(path.join(app.config['DATA'], '*.csv')):
        with open(path.join(app.config['DATA'], file)) as f:
            reader = DictReader(f, quotechar='"')
            for row in reader:
                id = row['Mem No'].replace('\t', '')
                id = f'{int(id):06d}'
                altId = row['SA Identity No'].replace('\t', '')
                language = row['Language'].replace('\t', '')
                language = language[0:1] if len(language) > 1 else 'A'
                member = {
                    'id': id,
                    'altId': altId,
                    'name': row['Preferred Name'].replace('\t', ''),
                    'surname': row['Surname'].replace('\t', ''),
                    'language': language
                }
                if not id in members.keys(): members[id] = member
                if not altId in altIds.keys(): altIds[altId] = id


def findMember(member):
    '''Finds a member by id or altId
    Input: a dictionary containing the id or altId
    Output: the member from the global list, if found
    '''
    global members, altIds
    altId = member.get('altId') # If the altId is provided...
    id = altIds.get(altId) if altId else member.get('id') # ...lookup the id or get directly
    if not id: return None
    id = f'{int(id):06}'
    m = members.get(id)
    return members.get(id)
