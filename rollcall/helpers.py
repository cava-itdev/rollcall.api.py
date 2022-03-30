from rollcall import app, members
from rollcall.member import Member
from os import path, getcwd, makedirs
from glob import glob
from csv import DictReader
import datetime as dt

def setupDirs():
    dataDir = path.join(getcwd(), 'data')
    app.config['DATA'] = dataDir
    makedirs(dataDir, exist_ok=True)
    makedirs(path.join(dataDir, 'faces'), exist_ok=True)


def createRegister():
    today = dt.datetime.today()
    register = path.join(app.config['DATA'], f'{today.year}-{today.month:02}-{today.day:02}.txt') 
    with open(register, 'w') as f:
        pass


def getMembers():
    global members
    for file in glob(path.join(app.config['DATA'], '*.csv')):
        with open(path.join(app.config['DATA'], file) ) as f:
            reader = DictReader(f, quotechar='"')
            for row in reader:
                memberId = row['Mem No'].replace('\t','')
                memberId = f'{int(memberId):06d}'
                if not memberId in members.keys():
                    member = Member()
                    member.id = memberId
                    member.altId = row['SA Identity No'].replace('\t','')
                    member.name = row['Preferred Name'].replace('\t',''),
                    member.surname = row['Surname'].replace('\t',''),
                    member.language = row['Language'].replace('\t','')[0:1],
                    member.email = row['E-mail address'].replace('\t',''),
                    member.phone = row['Mobile No'].replace('\t','')
                    members[memberId] = member