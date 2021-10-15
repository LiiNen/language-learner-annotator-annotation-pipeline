import csv
import random
import json

def conv(filename):
    with open('./data/%s.csv' % filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        buf = []
        count = 0
        for row in reader:
            book = {
                'id': row['asin'],
                'genre': row['category_name'],
                'title': row['title'],
                'description': row['editorial_review']
            }
            buf.append(book)
            if len(buf) == 5:
                rint = random.randint(1, 100)
                with open('./data/books/%s_%d_%d.json' % (filename, count, rint), 'w') as f:
                    json.dump(buf, f)
                count += 1
                buf = []

def main():
    conv('amt_children_1090')    
    conv('amt_science_1090')    

main()