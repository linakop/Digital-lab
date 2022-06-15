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
 @@ -29,16 +38,28 @@
 import psycopg2
 import psycopg2.extras
 from sqlalchemy import create_engine
 import pandas   
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
                        options=["Home","Diagramm","Preisantizipation","Email-Benachrichtigung", "Kontakt","Konto-Erstellung"],
                        options=["Home","Diagramm","Preisantizipation","Email-Benachrichtigung","Registrierung","Kontakt"],
                        icons=["house","graph-up","clock","alarm","person","person"],
                        menu_icon="cast",
                        default_index=0,
 @@ -163,11 +184,24 @@
     optionliste.sort()

     with col1:
       st.subheader("Bahnhof")
       option = st.selectbox('Startbahnhof auswählen', optionliste)
       st.write('Ihr ausgewählter Startbahnhof:', option)
       zielbahn=st.selectbox("Zielbahnhof auswählen", optionliste)
       st.write("Ihr Zielbahnhof ist:", zielbahn)
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
 @@ -187,11 +221,19 @@

       bahnkarteneu=st.selectbox("Bahnkarte:", bahnkarteliste)
       st.write("Bahnkarte:", bahnkarteneu)

     with st.form(key='form1'):
       submit_button = st.form_submit_button(label='Bestätigen')
     wunsch=st.text_input("Anfrage speichern in :")

     with st.form(key='form'):
       submit_buttonhome = st.form_submit_button(label='Bestätigen')
     def mehrereanfragen(user,wunsch):
         result=pandas.DataFrame(columns=["username","tabellenwunsch"])   
         result.loc[len(result)]=[user,wunsch]
         result.to_sql(name="anfragen", con=engine, if_exists="append")
         result=result[0:0]


     if submit_button:
     if submit_buttonhome:
       mehrereanfragen(user,wunsch)  
       start=option
       ziel=zielbahn
       datum=losdatum.strftime("%d.%m.%Y") 
 @@ -212,7 +254,7 @@


       if bahnkarteneu=="50":
         bahnkarte="4"
          bahnkarte="4"
       else: 
         if bahnkarteneu=="25":
                 bahnkarte="2"
 @@ -254,53 +296,130 @@
                 print("Fahrzeit: ",abfahrt_zv1,ankunft_zv1)
                 print("Art des Zuges/der Züge: ",art_zug_zv1)
                 print("Die Verbindung kostet: ",sparpreis_zv1)








 if optionen2=="Registrierung":
     eingabe=st.text_input("Username:")
     passw1=st.text_input("Passwort:",type="password")
     with st.form(key='form1'):
         register = st.form_submit_button(label='Registrieren')


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

     def add_userdata(eingabe,passw):
         result=pandas.DataFrame(columns=["username","passwort"])   
         result.loc[len(result)]=[eingabe,passw1]
         result.to_sql(name="login", con=engine, if_exists="append")
         result=result[0:0]
     if register:   
         add_userdata(eingabe,passw1)
         st.info("Erfolgreich registriert")

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

     if optionen2=="Preisantizipation":
         st.write("Preisantizipation")
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
         yag = yagmail.SMTP("dbtickeralert@gmail.com","ujbdfkbgqwbjemrh")
         contents = [
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
 @@ -311,46 +430,62 @@
         "\n"
         "DBTickeralert"
         ]
         liste=[1,2,3,4,5,6,7,8,9,10]
     liste=[1,2,3,4,5,6,7,8,9,10]


         preisangabe = st.slider("Ihr gewünschter Höchstpreis:")
         with st.form(key='form1'):
                 submit_buttonpreis = st.form_submit_button(label='Benachrichtige mich')    
                 if submit_buttonpreis:
                     st.write("Sie erhalten eine Email Benachrichtigung wenn sich der Preis unter",preisangabe ,"€ befindet") 
                     for i in range(len(liste)):
                       if liste[i]<=preisangabe:
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
                             st.write("Ihre Kaufbereitschaft ist sehr hoch") 


 def tabelleerstellen():
     result=pandas.DataFrame(columns=["Anfrage", "Alter", "Bahnkarte", "Startbahnhof", "Zielbahnhof", "Datum", "Abfahrtszeit", "Ankunftszeit", "Zugart",
                         "Preis"])  
     result.loc[len(result)]=[str(anfrage), alter_1, bahnkarteneu, start, ziel, datum, abfahrt_zv1, ankunft_zv1, art_zug_zv1,
                         sparpreis2_zv1]
     result.to_sql(name="tabelle1", con=engine, if_exists="append" )
     result=result[0:0]
     sleep(18)

       engine = create_engine('postgresql://dbticket_user:Nhaema5GzFDyW3j0sGHVYjfhRBu0fTvy@dpg-cajo73sgqg428kba9ikg-a.frankfurt-postgres.render.com/dbticket')
       cursor = conn.cursor()
       eingabe=st.text_input("Username:")
       passw=st.text_input("Passwort:",type="password")
       wunsch=st.text_input("Wunsch: ")

       def add_userdata(eingabe,passw):
           result=pandas.DataFrame(columns=["username","passwort"])   
           result.loc[len(result)]=[eingabe,passw]
           result.to_sql(name=wunsch, con=engine, if_exists="append")
           result=result[0:0]
       with st.form(key='form1'):
         submit_button3 = st.form_submit_button(label='Registrieren')
       if submit_button3:
         add_userdata(eingabe,passw)   





     #def create_usertable(wunsch):
         #cursor.execute("CREATE TABLE IF NOT EXISTS",wunsch+"(username varchar(45) NOT NULL,passwort varchar(450),PRIMARY KEY (username)")
