from streamlit_option_menu import option_menu
import pages.home
import pages.diagramm
import pages.registrieren
import pages.mail_nachricht
import pages.kontakt
import pages.websiteaufruf
import pages.log
import pages.auslog
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import streamlit as st
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
import pandas
import streamlit


st.set_page_config("DB","house",layout="wide")

PAGES = {
    "Willkommen":pages.websiteaufruf,
    "Registrierung": pages.registrieren,
    "Anfragen": pages.home,
    "Diagramm": pages.diagramm,
    "Email-Benachrichtigung":pages.mail_nachricht,
    "Kontakt":pages.kontakt,
    "Login":pages.log,
    "Abmelden":pages.auslog
    
}
conn = psycopg2.connect(host ="dpg-cajo73sgqg428kba9ikg-a.frankfurt-postgres.render.com",
                        database="dbticket", 
                        user="dbticket_user", 
                        password="Nhaema5GzFDyW3j0sGHVYjfhRBu0fTvy")

engine = create_engine('postgresql://dbticket_user:Nhaema5GzFDyW3j0sGHVYjfhRBu0fTvy@dpg-cajo73sgqg428kba9ikg-a.frankfurt-postgres.render.com/dbticket')
cursor = conn.cursor()
def app():
    selected3 = option_menu("DB Price App",options=list(PAGES.keys()), 
        icons=['house', 'cloud-upload', "list-task", 'gear'], 
        menu_icon="", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "red", "font-size": "12px"}, 
            "nav-link": {"font-size": "12px", "text-align": "left", "margin":"10px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "red"}

        }
    )
    if selected3=="Willkommen":
        pages.websiteaufruf.app()
        

       

        # Create a button which will increment the counter
        #increment = st.button('Increment')
        #if increment:
            #st.write(st.session_state.name)

        # A button to decrement the counter

        st.write('Count = ', st.session_state.user)
    if selected3=="Registrierung":
        pages.registrieren.app()
    if selected3=="Anfragen":
        pages.home.app()
    if selected3=="Diagramm":
        pages.diagramm.app()
    if selected3=="Email-Benachrichtigung":
        pages.mail_nachricht.app()
    if selected3=="Kontakt":
        pages.kontakt.app()
    if selected3=="Login":
        pages.log.app()
    if selected3=="Abmelden":
        pages.auslog.app()
 
st.title('Counter Example')

    # Streamlit runs from top to bottom on every iteraction so
    # we check if `count` has already been initialized in st.session_state.

    # If no, then initialize count to 0
    # If count is already initialized, don't do anything
with st.form("log"):
        loginn=st.text_input("Benutzername: ")
        loginp=st.text_input("Passwort: ")
        
        best=st.form_submit_button("Bestätigen")
def Login(loginn,loginp):
    abfrage = cursor.execute("SELECT login.username FROM login WHERE username=%s", [loginn])
    if not cursor.fetchone():  # An empty result evaluates to False.
        st.info("Kein Benutzer mit diesem Benutzernamen")
    else:
        abfragep = cursor.execute("""SELECT login.passwort FROM login WHERE passwort=%s""", [loginp])
        if not cursor.fetchone():  # An empty result evaluates to False.
            st.warning("Falsches Passwort")
        else:
            st.success("Sie haben sich erfolgreich eingeloggt")
            app()
        if 'user' not in st.session_state:
            st.session_state.user =loginn
            
            

if best:
    Login(loginn,loginp)     


