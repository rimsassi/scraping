from urllib import request
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import math  

def create_link_ville (ville):
    url = 'https://www.stephaneplazaimmobilier.com/search/buy?target=buy&location[]='+ville+'&sort=&markers=true&limit=50&page=0'
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    site_json=json.loads(soup.text)
    return site_json

def formater_annonce(ville):
    #page
    site_json = create_link_ville(ville)
    for annonce in site_json:
        annonce['id_annonce'] = str(annonce['id'])
        partie = annonce['title'].split()
        annonce['type_bien'] = str(partie[0])
        annonce['Type_bien_corrige'] = str(partie[0].capitalize())
        annonce['surface'] = int(math.floor(float(partie[3])))
        annonce['longitude'] = annonce['location']['lng']
        annonce['lattitude'] = annonce['location']['lat']
        annonce['prix_bien'] =  int(math.floor(float(annonce['price'].replace(' ','.'))))
    for element in site_json:
        del element['id']
        del element['name']
        del element['slug']
        del element['thumbnails']
        del element['target']
        del element['isExclusive']
        del element['polygonesArea']
        del element['title']
        del element['location']
        del element['price']

    annonces = json.dumps(site_json)
    with open("annonces.json", "w") as outfile:
        outfile.write(annonces)
        print('Data saved to file')
    

ville = '75112'
formater_annonce(ville)