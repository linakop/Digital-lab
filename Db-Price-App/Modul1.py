import csv
import pandas as pd 
from logging.config import listen
from statistics import mean

#liste1=[]
#with open("Hamburg.csv") as csvdatei:
    #csv_reader_object = csv.reader(csvdatei)
    #for row in csv_reader_object:
        #liste1.append(row)
        #print(liste1)

liste = [15,16,17,200,200]        
durchschnitt = mean(liste)

print("Durchschnitt:", durchschnitt)

pandasserie = pd.Series(liste)

haeufigkeit = pandasserie.value_counts()

print(haeufigkeit)

relative_haeufigkeit = haeufigkeit / len(liste)
print(relative_haeufigkeit)