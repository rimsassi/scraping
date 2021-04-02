from urllib import request
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import math  

def create_link_ville (ville):
    url = 'https://www.stephaneplazaimmobilier.com/search/buy?target=buy&location[]='+ville+'&sort=&markers=true&limit=50&page=0'
    headers = {
        'cookie': '__cfduid=defa976b65736174bbfe434af697b1f1b1617376418; XSRF-TOKEN=eyJpdiI6ImVTZDV0eTZpMlRiaU5FOEVMV1JjWWc9PSIsInZhbHVlIjoiS1VWYkxuT2JtZVNMakNYc1k3enprZlo1eEJnNndOVVI4aG81RVV0dDlyOVp4cWlRbVRSaEh3alJzYXY1YnNmayIsIm1hYyI6Ijk3NTdkMTYwZWMyZmZiYjlmZmE2MjAyNjdmMWMwYTRkNjUzZjAwYWIwMWEyYTJmMjUzMTliOTdkMTlhNjlkZjMifQ==; stephane_plaza_immobilier_session=eyJpdiI6Ik43cnR2UUZ2XC94YldiRE51VW1nUG9BPT0iLCJ2YWx1ZSI6InFZR2NocU5YekxWaWdoM3cwM0JlK0s1TURjVkNBQTNUMU4rSkhvdWFQRFpwRklDZkxEREVTa1RhdFJpalZ5YmIiLCJtYWMiOiI0YmQxYWZiMWYwMzMwMTdiYTAyZjA3ZTNhNzg4ZTg5Zjk0NzZiNmYzZjZkNzY1YTIyMGU1NGNjYWQ3MjYzZDFhIn0=',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }

    page = requests.get(url, headers=headers)

    if page.ok:
        soup = BeautifulSoup(page.text,'html.parser')
        site_json=json.loads(soup.text)

    return site_json

def formater_annonce(ville):
    site_json = create_link_ville(ville)
    for annonce in site_json:
        annonce['id_annonce'] = str(annonce['id'])
        partie = annonce['title'].split()
        annonce['type_bien'] = str(partie[0])
        annonce['Type_bien_corrige'] = str(partie[0].capitalize())
        annonce['surface'] = int(math.floor(float(partie[3])))
        annonce['nb_pieces'] = int(str(partie[1].replace('/','0')))
        annonce['code_postal'] = int(ville)
        annonce['ville'] = "Paris"
        annonce['longitude'] = annonce['location']['lng']
        annonce['lattitude'] = annonce['location']['lat']
        annonce['prix_bien'] =  int(math.floor(float(annonce['price'].replace(' ',''))))
        del annonce['id']
        del annonce['name']
        del annonce['slug']
        del annonce['thumbnails']
        del annonce['target']
        del annonce['isExclusive']
        del annonce['polygonesArea']
        del annonce['title']
        del annonce['location']
        del annonce['price']

    annonces = json.dumps(site_json)
    with open("annonces_updated.json", "w") as outfile:
        outfile.write(annonces)
        print('Data saved to file')
    

ville = '75112'
formater_annonce(ville)