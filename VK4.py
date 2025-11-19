// Tässä streamlit koodit, jotka hakevat API:lla tietoa eri tietokannoista
import streamlit as st
import mysql.connector
import pandas as pd

# --- Streamlit otsikko ---
st.title("Sää ja Kullan hinta")

# --- Luo kaksi saraketta ---
col1, col2 = st.columns(2)

# --- Säätiedot vasemmalle ---
with col1:
    st.header("Säätiedot")

    conn_weather = mysql.connector.connect(
        host="localhost",
        user="exampleuser",   # vaihda oikeaksi käyttäjäksi
        password="",  # vaihda oikeaksi salasanaksi
        database="weather_db"
    )
    cur_weather = conn_weather.cursor()
    cur_weather.execute(
        "SELECT id, city, temperature, description, timestamp FROM weather_data ORDER BY timestamp DESC LIMIT 20;"
    )
    rows_weather = cur_weather.fetchall()
    df_weather = pd.DataFrame(rows_weather, columns=["ID", "Kaupunki", "Lämpötila (°C)", "Kuvaus", "Aikaleima"])
    st.write("Tietokanta: weather_db ja Raahen säätiedot")
    st.dataframe(df_weather)
    cur_weather.close()
    conn_weather.close()

# --- Kullan hinta oikealle ---
with col2:
    st.header("Kullan hinta (USD/oz)")

    conn_gold = mysql.connector.connect(
        host="localhost",
        user="exampleuser",   # sama käyttäjä jolla annoit oikeudet
        password="",  # vaihda oikeaksi salasanaksi
        database="kulta_db"
    )
    df_gold = pd.read_sql("SELECT * FROM gold_prices ORDER BY timestamp DESC LIMIT 20", conn_gold)
    conn_gold.close()
    st.write("Tietokanta: kulta_db ja kullan hinnat")
    st.dataframe(df_gold)
