import time
import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import pickle

def charger():
    if data_file.name.split('.')[-1] in ['xlsx','xls']:
        data=pd.read_excel(data_file.read())
    else:
        data=pd.read_csv(data_file.read())
    provinces=data["Province"]
    data.head()
    d=data[cols] 
    st.success('Données chargées avec succes!')
    return d,provinces 

def predict(data):
    model = pickle.load(open('models/XGBoost Regression.pkl', 'rb'))
    return model.predict(data)

cols=['Population','Densité', 'Masculinité', 'Urbain', 'Rural', 'Cereale', 'Rente', 'Tmin', 'Pluie']
df=gpd.read_file('geo/provinces.geojson')

st.title("Migraware web App")
st.header("Chargement des données")
st.header("Vous devez avoir les colonnes :")
st.markdown("".join(['- '+i+'\n' for i in cols]))
data_file=st.file_uploader("Veuiller charger un fichier Excel ou CSV",
                      type=['csv','xlsx','xls'],label_visibility="visible"
)
data,provinces=charger()
result=predict(data)
pd.DataFrame(data=result,index=provinces,columns=['Sortie'])
    
hour=st.slider('Hour',0,24,1)
st.subheader("Checkbox Test")
st.checkbox("qsx")

st.balloons()

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")