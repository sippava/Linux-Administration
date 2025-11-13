import mysql.connector
import pandas as pd

st.title("Tervetuloa!")

conn = mysql.connector.connect(
    host="localhost",
    user="exambleuser",
    password="",
    database="mydata"
)

cur = conn.cursor()
cur.execute("SELECT id, name, email, role FROM streamlit;")
rows = cur.fetchall()

df = pd.DataFrame(rows, columns=["ID", "Nimi", "Sähköposti", "Rooli"])

st.write("Tietokanta: mydata")
st.dataframe(df)

cur.close()
conn.close()
