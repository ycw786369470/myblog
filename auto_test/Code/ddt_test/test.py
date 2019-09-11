import os
import csv


def get_data(index):
    with open(os.path.join(os.path.dirname(__file__), 'save.txt'), 'r', encoding='utf-8') as f:
        w = f.readlines()
        print(w[0])
        print(w[1])
        print(w[2])
        # return d[index]


def getCsv():
    rows = []
    with open('input.csv') as f:
        reader = csv.reader(f)
        for iter in reader:
            rows.append(iter)
    print(rows)


getCsv()