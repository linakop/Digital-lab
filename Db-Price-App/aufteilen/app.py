import streamlit as st
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
import pandas
from PIL import Image

def main():
    st.set_page_config(page_title="DB Ticker",layout="wide")

    conn = psycopg2.connect(host ="dpg-cajo73sgqg428kba9ikg-a.frankfurt-postgres.render.com",
                        database="dbticket", 
                        user="dbticket_user", 
                        password="Nhaema5GzFDyW3j0sGHVYjfhRBu0fTvy")

    engine = create_engine('postgresql://dbticket_user:Nhaema5GzFDyW3j0sGHVYjfhRBu0fTvy@dpg-cajo73sgqg428kba9ikg-a.frankfurt-postgres.render.com/dbticket')
    cursor = conn.cursor()

    st.title("DB Price App")
    image=Image.open("website.png")
    c=st.container()
     
        st.image(image,caption="DB Ticker-App")

        st.
 
main()      