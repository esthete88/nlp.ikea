'''
Small script that crawls through IKEA catalog and finds title and descriptions of goods
'''

import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


base_url = 'https://www.ikea.com'
url = 'https://www.ikea.com/ru/ru/catalog/productsaz/'

req = requests.get(url)
soup = BeautifulSoup(req.text, 'lxml')

unique_names = [] # list, where all titles are unique
names = []
titles = []

for i in tqdm(range(30)):
    req = requests.get(url + str(i))
    soup = BeautifulSoup(req.text, 'lxml')
    collections_links = [obj.find('a')['href'] for obj in soup.findAll('li', attrs={'class': "productsAzLink"})]
    for link in collections_links:
        req = requests.get(base_url + link)
        soup = BeautifulSoup(req.text, 'lxml')
        objects = soup.findAll('h3', attrs={'class': "noBold"})
        for obj in objects:
            data = obj.findAll('span')
            title = data[0].text
            description = data[1].text
            # Check if latin characters are in the title or the description
            if bool(re.search('[a-zA-Z]', title)) or bool(re.search('[a-zA-Z]', description)):
                continue
            names.append('{} {}'.format(title, description))
            if title not in titles:
                titles.append(title)
                unique_names.append('{} {}'.format(title, description))

with open('unique_names.txt', 'w', encoding="utf-8") as file:
    file.write('\n'.join(unique_names))

with open('names.txt', 'w', encoding="utf-8") as file:
    file.write('\n'.join(list(set(names))))
