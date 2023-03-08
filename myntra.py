import requests
from colorama import Fore
import csv
import os

to_csv = [[]]
col_index = {}

def getpaths(d):
    if not isinstance(d, dict):
        yield [d]
    else:
        yield from ([k] + w for k, v in d.items() for w in getpaths(v))

def full_paths(sample_dict, paths=[], parent_keys=[]):
    for key in sample_dict.keys():
        current_val = sample_dict[key]
        if type(current_val) is dict and len(current_val) > 0:
            full_paths(current_val, paths=paths, parent_keys=(parent_keys + [key]))
        else:
            x = parent_keys + [key] + [current_val]
            print('printing....................xxxxxxxxxxxxxxxxx')
            print(x)
            print('printing x donnnnnnnnnnneeeeeeeeeeeee')
            if len(x)>1:
                paths.append(x)
    return paths

def get_prod_id(from_id,to_id):
    products = []
    for i in range(from_id,to_id):
        print(Fore.RED + str(i))
        responce = requests.get('https://developer.myntra.com/style/'+str(i))
        if responce.status_code == 200:
            product = responce.json()
            if product['meta']['code'] == 200:
                print(Fore.GREEN + str(i))
                products.append(product)
    return products

def main():
    products = get_prod_id(3555,3580)
    for product in products:
        row = []
        paths = full_paths(product)
        for path in paths:
            value = path[-1]
            key = '.'.join(path[0:-1])
            key = key.replace(' ','')
            key = key.lower()
            index = 0
            if key in col_index:
                index = col_index[key]
            else:
                index = len(to_csv[0])
                to_csv[0].append(key)
            row.insert(index,value)
        if len(row)!=0:
            to_csv.append(row)    

main()

try:
    os.remove('./scraped_data.csv')
except OSError:
    pass

with open('scraped_data.csv', 'w', newline="") as file:
    my_file = csv.writer(file)
    for row in to_csv:
        my_file.writerow(row)
