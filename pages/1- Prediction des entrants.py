import time
import streamlit as st
import pandas as pd
import numpy as np
# import geopandas as gpd
import pickle
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
ssc=StandardScaler()
# model= pickle.load(open('models/entrant/XGBoost Regression.pkl', 'rb'))
model = xgb.XGBRegressor()  # init model
model.load_model('models/entrant.bin')  # load data
ssc=StandardScaler()
def relu(d,col):
    d[col]=[n(a) for a in d[col]]
    return d
def predict_entrant(data):
    d=ssc.fit_transform(data)
    result = model.predict(d)
    #result = data.join(pd.DataFrame(data=result,index=data.index,columns=['Sortie']))
    if(result>0):
        return result
    else:
        return 0

st.title("Prédiction des entrants")
#st.header("Prédiction des entrants")

population = st.number_input('La taille de la population d’une province',min_value=1)
densite = st.number_input('La densité de la population',min_value=0.0,step=0.1)
masculinite = st.number_input('Le taux de masculinité de la population',min_value=0.0,step=0.1)
urbaine = st.number_input('La taille de la population urbaine',min_value=0,step=1)
rurale = st.number_input('La taille de la population rurale',min_value=0,step=1)
urbanisation = st.number_input('Le taux d\'urbanisation de la province',min_value=0.0,step=0.1)
rente = st.number_input('La superficie cultivé des cultures de rente',min_value=0)
cereal = st.number_input('La superficie cultivé des céréales',min_value=0)
tmin = st.number_input('La température minimale de la province',min_value=0.0,step=0.1)
pluie = st.number_input('La pluviométrie au niveau de la province',min_value=0.0,step=0.1)

df={
'Population':[population],
'Densité':[densite],
'Masculinité':[masculinite],
'Urbain':[urbaine],
'Rural':[rurale],
'Taux Urbanisation':[urbanisation],
'Cereale':[cereal/population],
'Rente':[rente/population],
'Tmin':[tmin],
'Pluie':[pluie],
}
df=pd.DataFrame(df)
if st.button('Predire'):
    result = model.predict(df)
    #result=predict_entrant(df)
    st.subheader('Le nombre de personnes entrant cette province est : {}'.format(int(result)))







