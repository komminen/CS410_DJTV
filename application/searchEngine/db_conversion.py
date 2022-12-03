import json
import os
import shutil

f = open('movie_reviews_dataset.json')

data = json.load(f)
if os.path.isfile(os.getcwd() + '\movies.dat'):
    os.remove(os.getcwd() + '\movies.dat')

if os.path.isfile(os.getcwd() + '\movies_whole.dat'):
    os.remove(os.getcwd() + '\movies_whole.dat')

if os.path.isfile(os.getcwd() + '\movies_ids.dat'):
    os.remove(os.getcwd() + '\movies_ids.dat')

with open('movies.dat', 'a') as write_file:
    for id in data:
        # print(id, data[id])
        write_file.write(data[id]['localized_title'].strip().lower() + '\n')

with open('movies_whole.dat', 'a', encoding='utf-8') as write_file:
    for id in data:
        info = data[id]['localized_title'].strip().lower()
        for c in data[id]['cast']:
            info += ' ' + c.strip().lower()
        for g in data[id]['genres']:
            info += ' ' + g.strip().lower()
        for p in data[id]['producer']:
            info += ' ' + p.strip().lower()
        for d in data[id]['director']:
            info += ' ' + d.strip().lower()
        info += ' ' + str(data[id]['year'])
        write_file.write(info + '\n')

with open('movies_ids.dat', 'a') as write_file:
    for id in data:
        write_file.write(id + '\n')

source = os.getcwd() + '\movies.dat'
destination = os.getcwd() + '\movies\movies.dat'
try:
    shutil.move(source,destination)
except FileNotFoundError:
    print(source + " was not found")

source = os.getcwd() + '\movies_whole.dat'
destination = os.getcwd() + '\movies_whole\movies_whole.dat'
try:
    shutil.move(source,destination)
except FileNotFoundError:
    print(source + " was not found")

f.close()