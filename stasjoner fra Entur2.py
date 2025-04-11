# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 17:44:23 2025
@author: KoKe
"""

import requests
import json
import numpy as np
import folium

#Leser data fra et API hos Entur.
url = 'https://api.entur.io/stop-places/v1/read/stop-places?count=1000&skip=0&multimodal=both&transportModes=RAIL'
x = requests.get(url)
#Parser JSON
j = x.json()
stations = json.loads(x.content)

#Sjekker om OK kommer fra APIet
if x.status_code == '200':
  print("feil på import")

# Lager en json.fil med dataene vi har hentet. 
with open('2.json', 'w') as json_file:
    json.dump(stations, json_file, indent=4)
    print("filen 2.json er laget")

# går igjennom listen og finner alle stasjonene. 
antall_stations=len(stations)
#lager en teller
i=0

#definerer en tom array med feltnavn og datatype
loc = np.empty((0, 3), dtype=[("Stasjon", "U90"), ("Latitude", "f4"), ("Longitude", "f4")])
coordinates = np.empty((0, 3), dtype=[("Latitude", "f4"), ("Longitude", "f4")])

#går igjennom alle stasjonen fra tjenesten og fyller variabler.
while i < antall_stations:
  st = (json.dumps(stations[i]['name']['value'], ensure_ascii=False, separators=( "." , " , ")))
  #Stripper Stasjonenavn for " i hver ende
  st = st.strip('"')
  #fyller variablene med lattitude og longitude
  lat = float((json.dumps(stations[i]["centroid"]["location"]['latitude'])))
  long = float((json.dumps(stations[i]["centroid"]["location"]['longitude'])))
  # hvis stasjonen er innen for geografisk område så lagrer vi den i arrayen (Jærbanen) 
  if lat <= 58.966492 and lat>=58.461142 and long <= 6.102341 and long >= 5.532453:
      new_row = np.array([(st, lat, long)], dtype=loc.dtype)
      loc = np.append(loc, new_row)
      #Fyller opp Arrayen for kartdelen her. 
      new_row = np.array([(lat, long)], dtype=coordinates.dtype)
      coordinates = np.append(coordinates, new_row)
  i = i + 1
  
#Sorterer stasjonene fra sør til nord.
loc_sorted_desc = np.sort(loc, order='Latitude')[::-1]

#Printer de utvalgte stasjonene i consoll
print(loc_sorted_desc) 

#lager en liten søkefunksjon på dataene for å plukke ut en stasjon i utvalget
station_name = input("skriv inn en stasjon på Jærbanen (eksempel Øksnavadporten stasjon): ")



def search_station(stations, station_name):
    for station in loc:
        if station['Stasjon'] == station_name:
            print(f"Station: {station['Stasjon']}, Latitude: {station['Latitude']}, Longitude: {station['Longitude']}")


print(search_station(stations,station_name))

#_________________bruke et kartverk for å vise data der________________-
# center på kartet
start = (58.73469 , 5.649535) #

#finner ut hvor mange stasjoner som er i listen
num_tuples = len(coordinates)

i=0

# Opprett et kart sentrert rundt start variabele, og zoomer inn.
m = folium.Map(start, zoom_start=10)

#Looper igjennom arrayen laget den bare som en hardkodet Array, burde laget den dynamisk. 
while i < num_tuples:  
    folium.CircleMarker(coordinates[i]).add_to(m)
    i= i +1

# Lagre kartet som en HTML-fil med markeringer for hvor stasjonene er. 
m.save('footprint.html')
print("Kart med koordinater er lagret")