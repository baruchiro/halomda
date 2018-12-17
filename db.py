import os
import csv

file = 'db.csv'
data = {}

if os.path.isfile(file):
    with open(file) as f:
        reader = csv.reader(f)
        data = {l[0]: l[1:] for l in list(reader)}
        print(f'file {file} exist with {len(data)} rows')

else:
    print(f'file {file} not exist')


def tryGet(question):
    question = question[24:]
    res = data.get(question)
    if res:
        res = res[0]
    return res


def add(question, answer, work, section, task):
    question = question[24:]
    if question not in data or input("The answer exist, are you sure? y/n")[0].lower() == 'y':
        data[question] = [answer, work, section, task]
        save()


def save():
    with open(file, 'w+') as f:
        f.write('\n'.join([k+','+','.join(v) for k, v in data.items()]))
        print(f'{len(data)} lines writed to {file}')
