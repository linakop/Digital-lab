 
from http.client import CONFLICT
from re import X
from telnetlib import DO
from typing import Collection
import streamlit as st
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
import pandas
from bs4 import BeautifulSoup
import requests
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
import plotly.figure_factory as ff
import numpy as np
from streamlit_option_menu import option_menu 
import yagmail
from dbTable import *
from http.client import CONFLICT
from re import X
from telnetlib import DO
from typing import Collection
import smtplib, ssl
import mysql.connector
import time


def app():
    st.title("Preisvorhersage/Diagramm")

    conn = psycopg2.connect(host ="dpg-cajo73sgqg428kba9ikg-a.frankfurt-postgres.render.com",
                            database="dbticket", 
                            user="dbticket_user", 
                            password="Nhaema5GzFDyW3j0sGHVYjfhRBu0fTvy")

    engine = create_engine('postgresql://dbticket_user:Nhaema5GzFDyW3j0sGHVYjfhRBu0fTvy@dpg-cajo73sgqg428kba9ikg-a.frankfurt-postgres.render.com/dbticket')
    cursor = conn.cursor()

    coll1,coll2=st.columns(2)
    with coll1:
            loginname=st.text_input("Login: ",st.session_state.user)
            loginpassw=st.text_input("Passwort:",type="password")
            anfragenlistebenutzer=[]
                            
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
                richtigentabellen=cursor.execute("Select anfragen.tabelle from anfragen where username=%s", [loginname])
                alleanfragen=cursor.fetchall()
                if alleanfragen==None:
                    st.info("Zu diesem Benutzernamen gibt es noch keine Tabelle") 
                else:
                    if "tabe" not in st.session_state :
                        st.session_state.tabe= True
                    for tabell in alleanfragen:
                        anfragenlistebenutzer.append(tabell[0])
                        boxen=st.selectbox("Tabelle: ", anfragenlistebenutzer)
                    st.write(boxen)
                    
            with coll2:         
                with st.form(key='form10'):
                    st.text_input("Benutzer",loginname)
                    tab=st.form_submit_button(label='Tabellen zeigen')
            if tab:  
                zuordnen(loginname)


    
    data_tabelle = pd.read_sql("SELECT * FROM %s",[tab],conn)
    df_diagramm = pd.DataFrame(data)



    date_list = df_diagramm['anfrage_tag'].unique()

    date = st.sidebar.selectbox("Wähle ein Datum:",date_list)


    fig = px.line(df_diagramm[df_diagramm['anfrage_tag'] == date], 
        x = "anfrage_uhrzeit", y = "preis", title = date)
    st.plotly_chart(fig)



    cursor.execute("SELECT DISTINCT anfrage_tag FROM %s",[tab])

    inhalt = cursor.fetchall()
    mins=[]
    maxs=[]
    dates=[]



    for d in inhalt:
        date=str(d[0])
        cursor.execute(f"SELECT MIN(preis), MAX(preis) FROM {} WHERE anfrage_tag = '{date}'".format(tab)) 
        res=cursor.fetchone()
        mini=res[0]
        maxi=res[1]
        mins.append(mini)
        maxs.append(maxi)
        dates.append(date)

    df=pd.DataFrame({'Datum':dates, 'Maximum': maxs, 'Minimum':mins})
    print(df)


    train_size = int(len(df) * 0.8)
    df_train, df_test = df[:train_size], df[train_size:len(df)]
    train_data = df_train.iloc[:, 1:2].values

    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    train_data_scaled = scaler.fit_transform(train_data)


    x_train = []
    y_train = []

    time_window = 3

    for i in range(time_window, len(train_data_scaled)):
    x_train.append(train_data_scaled[i-time_window:i, 0])
    y_train.append(train_data_scaled[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))



    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, LSTM, Dropout

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, epochs=25, batch_size=32)



    actual_stock_price = df_test.iloc[:, 1:2].values

    total_data = pd.concat((df_train['Minimum'], df_test['Minimum']), axis=0)
    test_data = total_data[len(total_data)-len(df_test)-time_window:].values
    test_data = test_data.reshape(-1, 1)
    test_data = scaler.transform(test_data)



    total_dates = pd.concat((df_train['Datum'], df_test['Datum']), axis=0)
    test_dates = total_dates[len(total_dates)-len(df_test)-time_window:].values
    test_dates = test_dates.reshape(-1, 1)


    x_test = []
    for i in range(time_window, len(test_data)):
    x_test.append(test_data[i-time_window:i, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))



    predicted_stock_price = model.predict(x_test)
    predicted_stock_price = scaler.inverse_transform(predicted_stock_price)




    real_data = [test_data[len(test_data)+1-time_window:len(test_data+1), 0]]
    real_data = np.array(real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

    prediction = model.predict(real_data)
    prediction = scaler.inverse_transform(prediction)


    preis=float(prediction[0][0])
    preis2=str(round(preis, 2))+ ' EUR'
    st.subheader('Der prognostizierte Preis beträgt morgen:  ')
    st.subheader(preis2)
    


   