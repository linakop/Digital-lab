from http.client import CONFLICT
from re import X
from telnetlib import DO
from typing import Collection
import streamlit as st
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
import pandas
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
import smtplib, ssl
import requests
import streamlit as st
import time
import yagmail   



st.set_page_config(page_title="DB Ticker",layout="wide")

conn = psycopg2.connect(host ="dpg-cajo73sgqg428kba9ikg-a.frankfurt-postgres.render.com",
                        database="dbticket", 
                        user="dbticket_user", 
                        password="Nhaema5GzFDyW3j0sGHVYjfhRBu0fTvy")

engine = create_engine('postgresql://dbticket_user:Nhaema5GzFDyW3j0sGHVYjfhRBu0fTvy@dpg-cajo73sgqg428kba9ikg-a.frankfurt-postgres.render.com/dbticket')
cursor = conn.cursor()

st.title("DB Ticker App")
optionen2 = option_menu(menu_title=None,
                       options=["Home","Diagramm","Preisantizipation","Email-Benachrichtigung","Registrierung","Kontakt"],
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
        user=st.text_input("Benutzername")
        with st.form(key='form8'):
            userbut = st.form_submit_button(label='Prüfen')
        def benutzerpruef(user):
            benutzer=cursor.execute("Select login.username From login where username=%s",[user])
            if not cursor.fetchone():  # An empty result evaluates to False.
                st.info("Kein Benutzer mit diesem Benutzernamen, bitte erstellen Sie sich einen Account")
            else: 
                st.info("Benutzer gefunden")
                st.text_input("Benutzer",user)
                
        if userbut:
            benutzerpruef(user)  
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
    wunsch=st.text_input("Anfrage speichern in :")
    
    with st.form(key='form'):
      submit_buttonhome = st.form_submit_button(label='Bestätigen')
    def mehrereanfragen(user,wunsch):
        result=pandas.DataFrame(columns=["username","tabellenwunsch"])   
        result.loc[len(result)]=[user,wunsch]
        result.to_sql(name="anfragen", con=engine, if_exists="append")
        result=result[0:0]
        
    
    if submit_buttonhome:
      mehrereanfragen(user,wunsch)  
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

        zugverbindungen=soup.find("div", class_= "overviewConnection")
        zugverbindungen1=zugverbindungen.find("div", class_="connectionRoute")
        station1=zugverbindungen1.find("div", class_="station first").get_text(strip=True)
        station2=zugverbindungen1.find("div", class_="station stationDest").get_text(strip=True)
        uhrzeit_zv1=zugverbindungen.find("div", class_= "connectionTimeSoll")
        zeiten_zv1=uhrzeit_zv1.find("div", class_= "time").get_text(strip=True)
        art_zug_zv1=soup.find("div", class_= "connectionData")
        art_zug_zv2=art_zug_zv1.find("div", class_= "connectionBar").get_text(strip=True)
        preis_zv1=zugverbindungen.find("div",class_="connectionAction").get_text(strip=True)
        sparpreis_zv2=preis_zv1.replace("ab","")
        sparpreis_zv1=sparpreis_zv2.replace("Rückfahrt hinzufügen","")

        

        if "Verbindung liegt in der Vergangenheit" in sparpreis_zv1: 
          print("Diese Verbindung liegt in der Vergangenheit. Wählen Sie eine andere Verbindung")
          break

        else: 
            if "THA" in art_zug_zv2:
        
             print("Diese Zugverbindung wird nicht von uns unterstüzt. Bitte wählen Sie eine Verbindung der Züge von der DB.")
             break

            else: 
                if "VRS-Tarif" in sparpreis_zv1:
              
                   print ("Hier ist kein Vergleich notwendig, da diese Verbindung zu VRS-Tarifen angeboten wird.")
                   break 
            
                else: 
                    anfrage_tage= time.strftime("%d.%m.")
                    anfrage_zeit=time.strftime("%H:%M")
                    result=pandas.DataFrame(columns=["Anfrage Tag","Anfrage Uhrzeit","Startbahnhof", "Zielbahnhof","Fahrzeit","Preis"])
                    result.loc[len(result)]=[anfrage_tage,anfrage_zeit,station1,station2,zeiten_zv1,sparpreis_zv1]
                    result.to_sql(name=wunsch, con=engine, if_exists="append" )
                    result=result[0:0]
                sleep(18) 
        
         

if optionen2=="Registrierung":
    eingabe=st.text_input("Username:")
    passw1=st.text_input("Passwort:",type="password")
    with st.form(key='form1'):
        register = st.form_submit_button(label='Registrieren')
    

 
    def add_userdata(eingabe,passw1):
        anf=cursor.execute("Select login.username From login where username=%s",[eingabe])
        if not cursor.fetchone():
            passw1 = bcrypt.hashpw(passw1.encode("utf-8"), bcrypt.gensalt(5)).decode("utf-8")
            result=pandas.DataFrame(columns=["username","passwort"])
            result.loc[len(result)]=[eingabelog,passw1]
            result.to_sql(name="login", con=engine, if_exists="append")
            result=result[0:0]
            st.info("Erfolgreich registriert")
        else:
            st.warning("Der Benutzername existiert bereits")
    
            
    if register:   
        add_userdata(eingabe,passw1)
        
               
if optionen2=="Diagramm":
    coll1,coll2=st.columns(2)
    with coll1:
        loginname=st.text_input("Login: ")
        loginpassw=st.text_input("Passwort:",type="password")
        anfragenlistebenutzer=[]
        with st.form(key='form3'):
            lo = st.form_submit_button(label='Einloggen')
        
        def Login(loginname,loginpassw):
            abfrage = cursor.execute("SELECT login.username FROM login WHERE username=%s", [loginname])
            if not cursor.fetchone():  # An empty result evaluates to False.
                st.write("Kein Benutzer mit diesem Benutzernamen")
            else:
                abfragep = cursor.execute("""SELECT login.passwort FROM login WHERE passwort=%s""", [loginpassw])
                if not cursor.fetchone():  # An empty result evaluates to False.
                    st.write("Falsches Passwort")
                else:
                    st.write("Sie haben sich erfolgreich eingeloggt")
                    
        def zuordnen(loginname):
            richtigentabellen=cursor.execute("Select anfragen.tabellenwunsch from anfragen where username=%s", [loginname])
            alleanfragen=cursor.fetchall()
            if alleanfragen==None:
                st.info("Zu diesem Benutzernamen gibt es noch keine Tabelle") 
            else:
                for tabell in alleanfragen:
                    anfragenlistebenutzer.append(tabell[0])
                st.selectbox("Tabelle: ", anfragenlistebenutzer)
        if lo:   
            Login(loginname,loginpassw)
    with coll2:         
            with st.form(key='form10'):
                st.text_input("Benutzer",loginname)
                tab=st.form_submit_button(label='Tabellen zeigen')
            if tab:  
                zuordnen(loginname)
        
if optionen2=="Kontakt":
    st.subheader("Hallo!")
    strings= ("Wir sind Artur, Katja, Anna-Maria, Muhammet, Sven und Lina."
            "\n"
            "\n"
            "Wir sind Studierende der FH Aachen und haben im Zuge des Vertiefungsmoduls Digital Lab diese Website ins Leben gerufen.""\n" "\n"
            "\n"
            "Uns ist aufgefallen, dass Zugverbindungen der Deutschen Bahn stark im Preis schwanken."
            "\n" 
            "Je nachdem, wann man eine Anfrage startet - ob Morgens oder Nachmittags, am Wochenende oder unter der Woche - schwankt der Preis für die exakt gleiche Verbindung. "
            "\n"
            "\n"
            "Als Studierende - die tendenziell immer zu wenig Geld in der Tasche haben - hat uns das natürlich stutzig gemacht! "
            "\n"
            "\n"
            "Die Idee zu dieser Website wurde geboren."
            "\n"
            "\n"
            "Mit DB-Price-APP wollen wir es euch als Nutzern ermöglichen eure Wunsch-Verbindung zu tracken und euch ihren Preisverlauf anschaulich anzeigen zu lassen, damit ihr ein Gefühl für die Preisentwicklung bekommt."
            "\n"
            "\n"
            "Außerdem könnt ihr eine Email-Benachrichtigung aktivieren, sodass ihr eine Mail bekommt, sobald der Preis eurer Wunschverbindung unter eure zuvor angegebene Preisgrenze gefallen ist.""\n"
            "\n"
            "\n"
            "Damit soll vermieden werden, dass ihr selbst ständig eure Verbindung aktualisieren müsst." "\n"
            "So spart ihr mit DB-Price-APP  im Idealfall nicht nur Geld sondern auch noch Zeit und Nerven ;-)"  
            "\n" 
            "\n"
            "Kontakt:" 
            "\n"
            "\n"
            "Artur Sichwardt:	artur.sichwardt@alumni.fh-aachen.de"
            "\n"
            "\n"
            "Katja Gröning: 	katja.groening@alumni.fh-aachen.de"
            "\n"
            "\n"
            "Anna-Maria Kremer: 	anna-maria.kremer@alumni.fh-aachen.de"
            "\n"
            "\n"
            "Muhammet Aydogan:	muhammet.aydogan@alumni.fh-aachen.de"
            "\n"
            "\n"
            "Sven Piotrowski:	sven.piotrowski@alumni.fh-aachen.de"
            "\n"
            "\n"
            "Lina Koppany: 	lina.koppany@alumni.fh-Aachen.de""\n"
         )
    st.write(strings)
    
        
        
if optionen2=="Email-Benachrichtigung":
        
    st.subheader("Benachrichtigung anfordern")
    emailteil1=st.text_input("Emailnamen eingeben")
    emaildomains=["@gmail.com","@gmx.de","@web.de"]

    option = st.selectbox('Email Domain auswählen', emaildomains)
    ganzeemail=emailteil1+option

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    yag = yagmail.SMTP("dbaaahn@gmail.com","wmgtfktvxmjsipox")
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
                st.write("Sie erhalten eine Email Benachrichitung wenn sich der Preis unter",preisangabe ,"€ befindet") 
                for i in range(len(liste)):
                    if liste[i]<=preisangabe:
                        yag.send(to=ganzeemail,
                        subject='Neuer Preis',
                        contents=contents)
                    else:
                        if preisangabe>liste[i]:
                            st.write("Ihre Kaufbereitschaft ist sehr hoch") 
        
                
#def tabelleerstellen():
    #result=pandas.DataFrame(columns=["Anfrage", "Alter", "Bahnkarte", "Startbahnhof", "Zielbahnhof", "Datum", "Abfahrtszeit", "Ankunftszeit", "Zugart",
                       # "Preis"])  
    #result.loc[len(result)]=[str(anfrage), alter_1, bahnkarteneu, start, ziel, datum, abfahrt_zv1, ankunft_zv1, art_zug_zv1,
                      #  sparpreis2_zv1]
   # result.to_sql(name="tabelle1", con=engine, if_exists="append" )
    #result=result[0:0]
   # sleep(18)

        


        
    #def create_usertable(wunsch):
        #cursor.execute("CREATE TABLE IF NOT EXISTS",wunsch+"(username varchar(45) NOT NULL,passwort varchar(450),PRIMARY KEY (username)")
                        
  

      

  

    





        












