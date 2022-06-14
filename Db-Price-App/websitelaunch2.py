import streamlit as st

from bs4 import BeautifulSoup
import requests
import csv
import time 
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import plotly.express as px 
import plotly
from matplotlib import dates as mpl_dates
from cProfile import label
from distutils.cmd import Command
import datetime 
from streamlit.cli import main  
from streamlit.proto.RootContainer_pb2 import RootContainer
import pandas as pd 
import streamlit as st
import plotly.figure_factory as ff
import numpy as np
from streamlit_option_menu import option_menu 
import yagmail
from dbTable import *
from http.client import CONFLICT
from re import X
from telnetlib import DO
from typing import Collection
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
import pandas   



st.set_page_config(page_title="DB Ticker",layout="wide")


st.title("DB Ticker App")
optionen2 = option_menu(menu_title=None,
                       options=["Home","Diagramm","Preisantizipation","Email-Benachrichtigung", "Kontakt","Konto-Erstellung"],
                       icons=["house","graph-up","clock","alarm","person","person"],
                       menu_icon="cast",
                       default_index=0,
                       orientation="horizontal",
                       )
if optionen2=="Home":
    
    optionliste = ["",'Darmstadt Hbf',
    "Wiesbaden Hbf",
    "Hanau Hbf",
    "Frankenthal Hbf",
    "Kaiserslautern Hbf",
    "Pirmasens Hbf",
    "Speyer Hbf",
    "Zweibrücken Hbf",
    "Kassel Hbf",
    "Boppard Hbf",
    "Koblenz Hbf",
    "Wittlich Hbf",
    "Mainz Hbf",
    "Worms Hbf",
    "Saarbrücken Hbf",
    "Saarlouis Hbf",
    "Trier Hbf",
    "Braunschweig Hbf",
    "Hildesheim Hbf",
    "Wolfsburg Hbf",
    "Bremen Hbf",
    "Bremerhaven Hbf",
    "Emden Hbf",
    "Osnabrück Hbf",
    "Hamburg Hbf",
    "Hannover Hbf",
    "Kiel Hbf",
    "Lübeck Hbf",
    "Cottbus Hbf",
    "Brandenburg Hbf",
    "Eberswalde Hbf",
    "Potsdam Hbf",
    "Neustrelitz Hbf",
    "Rostock Hbf",
    "Stralsund Hbf",
    "Schwerin Hbf",
    "Augsburg Hbf",
    "Lindau Hbf",
    "Bayreuth Hbf",
    "Hof Hbf",
    "München Hbf",
    "Nürnberg Hbf",
    "Deggendorf Hbf",
    "Passau Hbf",
    "Regensburg Hbf",
    "Berchtesgaden Hbf",
    "Ingolstadt Hbf",
    "Aschaffenburg Hbf",
    "Schweinfurt Hbf",
    "Würzburg Hbf",
    "Chemnitz Hbf",
    "Gera Hbf",
    "Dresden Hbf",
    "Arnstadt Hbf",
    "Erfurt Hbf",
    "Merseburg Hbf",
    "Döbeln Hbf",
    "Leipzig Hbf",
    "Bernburg Hbf",
    "Dessau Hbf",
    "Magdeburg Hbf",
    "Stendal Hbf",
    "Thale Hbf",
    "Wernigerode Hbf",
    "Lörrach Hbf",
    "Reutlingen Hbf",
    "Tübingen Hbf",
    "Freudenstadt Hbf",
    "Karlsruhe Hbf",
    "Pforzheim Hbf",
    "Bad Friedrichshall Hbf",
    "Heidelberg Hbf",
    "Heilbronn Hbf",
    "Mannheim Hbf",
    "Öhringen Hbf",
    "Stuttgart Hbf",
    "Aalen Hbf",
    "Ulm Hbf",
    "Bielefeld Hbf",
    "Gütersloh Hbf",
    "Paderborn Hbf",
    "Dortmund Hbf",
    "Lünen Hbf",
    "Bottrop Hbf",
    "Duisburg Hbf",
    "Krefeld Hbf",
    "Oberhausen Hbf",
    "Aachen Hbf",
    "Düsseldorf Hbf",
    "Eschweiler Hbf",
    "Gevelsberg Hbf",
    "Mönchengladbach Hbf",
    "Neuss Hbf",
    "Remscheid Hbf",
    "Rheydt Hbf",
    "Solingen Hbf",
    "Wuppertal Hbf",
    "Bochum Hbf",
    "Castrop-Rauxel Hbf",
    "Essen Hbf",
    "Gelsenkirchen Hbf",
    "Wanne-Eickel Hbf",
    "Witten Hbf",
    "Hagen Hbf",
    "Siegen Hbf",
    "Bonn Hbf",
    "Köln Hbf",
    "Recklinghausen Hbf"
    ]
    
    st.header("Homepage")
    col1,col2,col3=st.columns(3)
    
    bahnkarteliste=["","25","50","Nein"]
    optionliste.sort()
    
    with col1:
      st.subheader("Bahnhof")
      option = st.selectbox('Startbahnhof auswählen', optionliste)
      st.write('Ihr ausgewählter Startbahnhof:', option)
      zielbahn=st.selectbox("Zielbahnhof auswählen", optionliste)
      st.write("Ihr Zielbahnhof ist:", zielbahn)
    with col2:
      st.subheader("Abfahrt")
      losdatum=st.date_input('Datum', value= pd.to_datetime("today"))
      st.write("Datum:", losdatum.strftime("%d.%m.%Y"))
            
      uhrzeit_stunde1=st.number_input("Stunde: ", min_value=1,value=12,max_value=24,step=1)
      st.write("Stunde: ", uhrzeit_stunde1)


      uhrzeit_minuten1=st.number_input("Minute: ",min_value=00,max_value=59,step=1) 
      st.write("Minute: ", uhrzeit_minuten1)

    with col3:
      st.subheader("Alter & Bahnkarte")
      alter_1=st.number_input("Alter: ",min_value=1,value=18,max_value=110,step=1) 
      st.write("Alter: ", alter_1)

      bahnkarteneu=st.selectbox("Bahnkarte:", bahnkarteliste)
      st.write("Bahnkarte:", bahnkarteneu)
      
    with st.form(key='form1'):
      submit_button = st.form_submit_button(label='Bestätigen')
    
    if submit_button:
      start=option
      ziel=zielbahn
      datum=losdatum.strftime("%d.%m.%Y") 
      uhrzeit_stunde=str(uhrzeit_stunde1)
      uhrzeit_minuten=str(uhrzeit_minuten1)

      uhrzeit_minuten=str(uhrzeit_minuten1)
      if alter_1 in range(15,5,-1):
            alter="f"
      else: 
        if alter_1 in range(26,13,-1): 
                 alter="y"
        else:
                if alter_1 in range(64,26,-1):
                    alter="e"
                else: 
                    alter="s" 


      if bahnkarteneu=="50":
        bahnkarte="4"
      else: 
        if bahnkarteneu=="25":
                bahnkarte="2"
        else: 
                bahnkarte="0"
      while True:

        url='https://reiseauskunft.bahn.de/bin/query.exe/dn?revia=yes&existOptimizePrice-deactivated=1&country=DEU&dbkanal_007=L01_S01_D001_qf-bahn-svb-kl2_lz03&start=1&protocol=https%3A&REQ0JourneyStopsS0A=1&S='+start+'&REQ0JourneyStopsSID=A%3D1%40O%3DM%C3%BCnchen+Hbf%40X%3D11558339%40Y%3D48140229%40U%3D80%40L%3D008000261%40B%3D1%40p%3D1652295202%40&REQ0JourneyStopsZ0A=1&Z='+ziel+'&REQ0JourneyStopsZID=A%3D1%40O%3DAachen+Hbf%40X%3D6091495%40Y%3D50767803%40U%3D80%40L%3D008000001%40B%3D1%40p%3D1652295202%40&date=Fr%2C+'+datum+'&time='+uhrzeit_stunde+'%3A'+uhrzeit_minuten+'&timesel=depart&returnDate=&returnTime=&returnTimesel=depart&optimize=0&auskunft_travelers_number=1&tariffTravellerType.1='+alter+'&tariffTravellerReductionClass.1='+bahnkarte+'&tariffClass=2&rtMode=DB-HYBRID&externRequest=yes&HWAI=JS%21js%3Dyes%21ajax%3Dyes%21&externRequest=yes&HWAI=JS%21js%3Dyes%21ajax%3Dyes%21#hfsseq1|gl.0263982.1652621988'
        source=requests.get(url)
        soup = BeautifulSoup(source.text,"html.parser")

        zugverbindungen=soup.find("div",class_="resultContentHolder")
        zugverbindung1= zugverbindungen.find("div", class_="connectionData")
        stationen_zugverbindung1=zugverbindung1.find("div", class_="connectionStations").get_text(strip=True)
        uhrzeit_zv1= zugverbindung1.find("div", class_= "connectionTime")
        abfahrt_zv1=uhrzeit_zv1.find("div", class_="time timeDep").get_text(strip=True)
        ankunft_zv1=uhrzeit_zv1.find("div", class_="time timeArr").get_text(strip=True)
        art_zug_zv1=soup.find("div", class_="products").get_text(strip=True)
        preis_zv1=soup.find("div", class_="overviewConnection")
        sparpreis_zv1=preis_zv1.find("div", class_="connectionPrice").get_text(strip=True)
        sparpreis2_zv1=sparpreis_zv1.replace("ab","")

        if "THA" in art_zug_zv1:

            print("Diese Zugverbindung wird nicht von uns unterstüzt. Bitte wählen Sie eine Verbindung der Züge von der DB.")
            break

        else:
            if "VRS-Tarif" in sparpreis_zv1:

                print ("Hier ist kein Vergleich notwendig, da diese Verbindung zu VRS-Tarifen angeboten wird.")
                break 

            else: 

                anfrage= time.strftime("%d.%m. %H:%M")
                print(anfrage)
                print("Stationen: ",stationen_zugverbindung1)
                print("Fahrzeit: ",abfahrt_zv1,ankunft_zv1)
                print("Art des Zuges/der Züge: ",art_zug_zv1)
                print("Die Verbindung kostet: ",sparpreis_zv1)
                
               

               


else:
    if optionen2=="Diagramm":
        with st.sidebar:
            optionenside= option_menu(menu_title=None,
            options=["Liniendiagramm","Säulendiagramm"],
            icons=["graph-up","bar-chart-line"],
            menu_icon="",
            default_index=0,
            orientation="vertical",
        )
            
        if optionenside=="Liniendiagramm":
            st.write("Hier kommt ein Liniendiagramm hin")
            with st.form(key='form1'):
                submit_button2 = st.form_submit_button(label='Graph ansehen')
                if submit_button2:
                    st.write("Knopf gedrückt")
                    
        else:
            
            st.write("Hier kommt ein Säulendiagramm hin")
            with st.form(key='form1'):
                submit_button1 = st.form_submit_button(label='Graph ansehen')
                if submit_button1:
                    st.write("Säulendiagramm angezeigt")  
                    
    if optionen2=="Preisantizipation":
        st.write("Preisantizipation")
        
    if optionen2=="Email-Benachrichtigung":
        st.subheader("Benachrichtigung anfordern")
        emailteil1=st.text_input("Emailnamen eingeben")
        emaildomains=["@gmail.com","@gmx.de","@web.de"]

        option = st.selectbox('Email Domain auswählen', emaildomains)
        ganzeemail=emailteil1+option

        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        yag = yagmail.SMTP("dbtickeralert@gmail.com","ujbdfkbgqwbjemrh")
        contents = [
        "Ein neuer Preis ihrer Verbindung ist verfuegbar."
        "\n"
        "Kaufen Sie sich ein Ticket."
        "\n"

        "Freundlicher Gruss"
        "\n"
        "\n"
        "DBTickeralert"
        ]
        liste=[1,2,3,4,5,6,7,8,9,10]

                
        preisangabe = st.slider("Ihr gewünschter Höchstpreis:")
        with st.form(key='form1'):
                submit_buttonpreis = st.form_submit_button(label='Benachrichtige mich')    
                if submit_buttonpreis:
                    st.write("Sie erhalten eine Email Benachrichtigung wenn sich der Preis unter",preisangabe ,"€ befindet") 
                    for i in range(len(liste)):
                      if liste[i]<=preisangabe:
                        yag.send(to=ganzeemail,
                        subject='Neuer Preis',
                        contents=contents)
                      else:
                        if preisangabe>liste[i]:
                          st.write("Ihre Kaufbereitschaft ist sehr hoch")   
    if optionen2=="Kontakt":
      st.subheader("Digital Lab Gruppe 4")
    if optionen2=="Konto-Erstellung":
      conn = psycopg2.connect(host ="dpg-cajo73sgqg428kba9ikg-a.frankfurt-postgres.render.com",
                        database="dbticket", 
                        user="dbticket_user", 
                        password="Nhaema5GzFDyW3j0sGHVYjfhRBu0fTvy")

      engine = create_engine('postgresql://dbticket_user:Nhaema5GzFDyW3j0sGHVYjfhRBu0fTvy@dpg-cajo73sgqg428kba9ikg-a.frankfurt-postgres.render.com/dbticket')
      cursor = conn.cursor()
      eingabe=st.text_input("Username:")
      passw=st.text_input("Passwort:",type="password")
      wunsch=st.text_input("Wunsch: ")
      zahlen=st.number_input("Zahl: ",min_value=1,value=18,max_value=110,step=1)
        
      def add_userdata(eingabe,passw):
          result=pandas.DataFrame(columns=["zahlen"])   
          result.loc[len(result)]=[zahlen]
          result.to_sql(name="zahlentest", con=engine, if_exists="append")
          result=result[0:0]

      with st.form(key='form1'):
        submit_button3 = st.form_submit_button(label='Registrieren')
      if submit_button3:
        add_userdata(zahlen)   