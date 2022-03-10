from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os
import pathlib import Path

url = "https://bulbapedia.bulbagarden.net"
pokedex = "/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
result = requests.get(url + pokedex)
pokedex_html = BeautifulSoup(result.text, "html.parser")
generations = pokedex_html.find_all("span", {"id": re.compile("^(Generation_)")})
generations = generations[:-1]
generations_tables = [span.parent.find_next('table') for span in generations]
all_pokemos = []

if(not Path('./assets').exists()):
    os.mkdir('./assets')

def getting_attributes(url, url_pokemon):
    poke_request = requests.get(url + url_pokemon)
    pokemon_html = BeautifulSoup(poke_request.text, "html.parser")
    #poke_img = pokemon_html.find('img', alt
    span_color = pokemon_html.find('span', string='Pokédex color').parent.parent
    color = span_color.find_next('table').text.strip().split("Other forms may have other colors.")[0]
    ability1 = 0
    ability2 = 0
    try:
        abilities_span = pokemon_html.find('span', string='Abilities').parent.parent
        abilities = abilities_span.find_next('table').find('td').text.split('\xa0or')
        if(len(abilities) > 1):
            ability1 = abilities[0].strip()
            ability2 = abilities[1].strip()
        else:
            ability1 = abilities[0].strip()
    except:
        ability1 = 0
        ability2 = 0

    hidden_ability_span = 0 
    try:
        hidden_ability_span = pokemon_html.find('small', string=re.compile('(Hidden Ability)')).parent.text.split('Hidden Ability')[0]
    except:
        hidden_ability_span = 0

    span_height = pokemon_html.find('span', string='Height').parent.parent
    height = span_height.find_next('table').find('tr').find_all('td')[1].text.strip()

    span_weight = pokemon_html.find('span', string='Weight').parent.parent
    weight = span_weight.find_next('table').find('tr').find_all('td')[1].text.strip()

    hp_span = pokemon_html.find('span', string='HP').parent.parent
    hp = hp_span.find_next('div').text
    
    attack_span = pokemon_html.find('span', string='Attack').parent.parent
    attack = attack_span.find_next('div').text

    defense_span = pokemon_html.find('span', string='Defense').parent.parent
    defense = defense_span.find_next('div').text

    sp_attack_span = pokemon_html.find('span', string='Sp. Atk').parent.parent
    sp_attack = sp_attack_span.find_next('div').text

    sp_defense_span = pokemon_html.find('span', string='Sp. Def').parent.parent
    sp_defense = sp_defense_span.find_next('div').text

    speed_span = pokemon_html.find('span', string='Speed').parent.parent
    speed = speed_span.find_next('div').text

    total_span = pokemon_html.find('div', string='Total:')
    total = total_span.find_next('div').text
    
    attributes = (
            color,
            ability1,
            ability2,
            hidden_ability_span,
            height,
            weight,
            hp,
            attack,
            defense,
            sp_attack,
            sp_defense,
            speed,
            total
            )

    return attributes


for table in generations_tables:
    rows = table.find_all('tr')
    for data in rows[1:]:
        pokemon = {}
        tdata = data.find_all('td')
        pokemon['CODE'] = tdata[0].string.strip()
        pokemon['SERIAL'] = tdata[1].string.strip()
        pokemon['NAME'] = tdata[2].findChild().text
        pokemon['TYPE1'] = tdata[3].findChild().text
        try:
            pokemon['TYPE2'] = tdata[4].findChild().text
        except:
            pokemon['TYPE2'] = 0
        
        url_pokemon = tdata[2].findChild()['href']
        attributes = getting_attributes(url, url_pokemon)

        pokemon['COLOR'] = attributes[0]
        pokemon['ABILITY1'] = attributes[1]
        pokemon['ABILITY2'] = attributes[2]
        pokemon['ABILITY HIDDEN'] = attributes[3]
        pokemon['GENERATION'] = generations_tables.index(table) + 1
        pokemon['HEIGHT'] = float(attributes[4].split(' m')[0])
        pokemon['WEIGHT'] = float(attributes[5].split(' kg')[0])
        pokemon['HP'] = int(attributes[6])
        pokemon['ATK'] = int(attributes[7])
        pokemon['DEF'] = int(attributes[8])
        pokemon['SP_ATK'] = int(attributes[9])
        pokemon['SP_DEF'] = int(attributes[10])
        pokemon['SPD'] = int(attributes[11])
        pokemon['TOTAL'] = int(attributes[12])
        print(pokemon)
        all_pokemos.append(pokemon)

pd.DataFrame(all_pokemos).to_csv('pokemons.csv', header=True, index=True, sep=',')
