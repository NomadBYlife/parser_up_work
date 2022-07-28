
"""Fast parser for vacancies from https://www.gov.pl/ for IT specialists"""


import requests
import fake_useragent
from bs4 import BeautifulSoup
import json


user = fake_useragent.UserAgent().random
header = {'user-agent': user}

link = "https://www.gov.pl/web/poland-businessharbour-en/itspecialist"
response = requests.get(link, headers=header).text


soup = BeautifulSoup(response, 'lxml')

block = soup.find('article')
details = block.find_all("div", class_="editor-content")
info = details[1].find_all('details')
all_data = {}
list_data = []
for i in info:
    www_list = []
    contact_list = []
    title = i.find('summary').text.replace('\xa0', '')
    tag_p = i.find_all('p')
    for tags in tag_p:
        try:
            for tag in tags.find_all('a'):
                if tag.get('href').find('mailto') != -1:
                    contact_list.append(tag.get('href').replace('mailto:', ''))
                else:
                    www_list.append(tag.get('href').replace('\n', ''))
        except:
            continue
    if len(www_list) > 0:
        data = {title: {"www": www_list, "contact": contact_list}}
    else:
        data = {title: {"contact": contact_list}}
    list_data.append(data)


def create_json_file(parsed_data):
    with open('json_data.json', 'w') as file:
        json.dump(parsed_data, file)


if __name__ == "__main__":
    create_json_file(list_data)
