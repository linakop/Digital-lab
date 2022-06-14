import psycopg2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


conn = psycopg2.connect(host ="dpg-cajo73sgqg428kba9ikg-a.frankfurt-postgres.render.com",
                        database="dbticket", 
                        user="dbticket_user", 
                        password="Nhaema5GzFDyW3j0sGHVYjfhRBu0fTvy")




df = pd.read_sql("SELECT * FROM anfragen",conn)


print(df)