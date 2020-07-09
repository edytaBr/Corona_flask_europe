#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 21:05:59 2020

@author: edyta
"""


# Import libraries
import pandas as pd
import folium
import os
import pandas as pd
from flask import Flask
from covid import Covid
import json
from countryinfo import CountryInfo
from flask import Flask
app = Flask(__name__)
covid = Covid()
covid.get_data()
@app.route('/')



def index():
    #Extract countries names from geojson
    with open('europe.geojson') as data:
        geo = json.load(data)
    countries = []
    for item in geo['features']:
        countries.append(item['properties']['NAME'])
        
        
    #Create dataset from worldmeters by using countries from geojson
    list1 = []
    for element in countries:
        list1.append((covid.get_status_by_country_name(element))['confirmed'])
        
        
    data = {}
    for keys in countries:
        for num in list1:
            data[keys] = num
            list1.remove(num)
            break
        


    #Population and R rate for co
    cases = []
    for element in countries:
        cases.append((covid.get_status_by_country_name(element))['confirmed'])

    countries = ['Azerbaijan', 'Albania', 'Armenia', 'Bosnia and Herzegovina', 'Bulgaria', 'Cyprus', 'Denmark',
            'Ireland', 'Estonia', 'Austria', 'Czech Republic', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 
            'Croatia', 'Hungary', 'Iceland', 'Israel', 'Italy', 'Latvia', 'Belarus', 'Lithuania', 'Slovakia', 'Liechtenstein', 
                'Malta', 'Belgium', 'Luxembourg', 'Monaco',  'Netherlands', 'Norway', 'Poland', 
            'Portugal', 'Romania', 'Moldova', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'United Kingdom', 'Ukraine', 'San Marino', 'Serbia', 'Russia']

    ##no macedonia, montenegro



    population= []
    for land in countries:
        population.append(CountryInfo(land).population())



    data_cases = {}
    for keys in countries:
        for num in cases:
            data_cases[keys] = num
            cases.remove(num)
            break


    data_population = {}
    for keys in countries:
        for pop in population:
            data_population[keys] = pop
            population.remove(pop)
            break


    ratio = {}
    for key in data_cases:
        for key1 in data_population:
            if key == key1:
                ratio[key] = (data_cases[key1]/ data_population[key])*100




    #Change dictionary with data to csv file and save.     
    df = pd.DataFrame(list(ratio.items()),columns = ['Country','Ratio'])
    korona_ratio = df



    #Change dictionary with data to csv file and save.     
    df = pd.DataFrame(list(data.items()),columns = ['Country','Cases'])
    korona = df


    #Folium map
    europe = os.path.join('/home/edyta/corona/','europe.geojson')
    m = folium.Map(location=[55, 10], zoom_start=4,  tiles='cartodbdark_matter')
    #geojson_layer = folium.GeoJson(europe,name='geojson', show=False).add_to(m)

    m.choropleth(
    geo_data=europe,
    name='Corona',
    data=korona,
    columns=['Country', 'Cases'],
    key_on='properties.NAME',
    fill_color= 'Reds', fill_opacity=0.4, line_opacity=0.9, 
    threshold_scale=[50, 1000, 3000, 5000,15000, 50000,60000, 70000, 1000000]
    )

    return m._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)

