import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
from sqlalchemy import create_engine

url = "https://wiki.srb2.org/wiki/SRB2Kart/Levels"
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
html = requests.get(url, headers=header).text #.content.decode('utf-8')
soup = BeautifulSoup(html,'lxml')

try: 
    standard = pd.read_html(html)[0]  # vanilla race
    battle = pd.read_html(html)[1]  #vanilla battle
    hell = pd.read_html(html)[2]  #hell maps
    removed = pd.read_html(html)[3]  #removed maps
except IndexError:
    print("index error, check your tables")

pics = []
mmaps = []
for items in soup.find_all('table', class_='wikitable'):
    for tables in items.find_all('tr')[1::1]:
        data = tables.find_all(['th','td'])
        try:
            image = data[2]
            minimap = data[3]
            map_img = image.find('a').find('img')["src"]
            min_map = minimap.find('a').find('img')["src"]
            pics.append(map_img)
            mmaps.append(min_map)
        except IndexError:
            pass

#drop title indexs
standard_drops = [5,11,17,23,29,35,41,47,53,59,65]
standard.drop(standard_drops,axis=0,inplace=True)
standard.reindex(axis=0)

#add empty silver and gold times to the hell maps
hell['Silver time'] = ''
hell['Gold time'] = ''

# Find the name of the column by index
standard_pics = standard.columns[2]
standard_mmap = standard.columns[3]
battle_pics = battle.columns[2]
battle_mmap = battle.columns[3]
hell_pics = hell.columns[2]
hell_mmap = hell.columns[3]
removed_pics = removed.columns[2]
removed_mmap = removed.columns[3]

# Drop that column
standard.drop(standard_pics, axis = 1, inplace = True)
standard.drop(standard_mmap, axis = 1, inplace = True)
battle.drop(battle_pics, axis = 1, inplace = True)
battle.drop(battle_mmap, axis = 1, inplace = True)
hell.drop(hell_pics, axis=1,inplace=True)
hell.drop(hell_mmap, axis=1,inplace=True)
removed.drop(removed_pics, axis=1,inplace=True)
removed.drop(removed_mmap, axis=1,inplace=True)

# Put whatever series you want in its place
standard[standard_pics] = pics[0:60]
standard[standard_mmap] = mmaps[0:60]
battle[battle_pics] = pics[60:89]
battle[battle_mmap] = mmaps[60:89]
hell[hell_pics] = pics[89:107]
hell[hell_mmap] = mmaps[89:107]
removed[removed_pics] = pics[107:111]
removed[removed_mmap] = mmaps[107:111]

#clear the csv
csv = open("maps.csv", 'w+')
csv.write("")
csv.close()

#write all new stuff to csv
csv = open("maps.csv", "a")
standard.to_csv(csv)
hell.to_csv(csv)
csv.close()