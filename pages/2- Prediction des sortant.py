import time
import streamlit as st
import pandas as pd
import numpy as np
# import geopandas as gpd
import pickle
import xgboost as xgb
from sklearn.preprocessing import StandardScaler,MinMaxScaler
model = pickle.load(open('models/sortant/XGBoost Regression.pkl', 'rb'))
model = pickle.load(open('models/sortant/XGBoost Regression.pkl', 'rb'))
# model = xgb.XGBRegressor()  # init model
# model.load_model('models/sortant.bin')  # load data
ssc=StandardScaler()

st.title("Prédiction des sortants")
#st.header("Prédiction des sortants")
n=lambda d: 0 if d<0 else np.ceil(d)
def relu(d,col):
    d[col]=[n(a) for a in d[col]]
    return d


population = st.number_input('La taille de la population d’une province',min_value=1)
densite = st.number_input('La densité de la population',min_value=0.0,step=0.01)
masculinite = st.number_input('Le taux de masculinité de la population',min_value=0.0,step=0.01)
urbaine = st.number_input('La taille de la population urbaine',min_value=0.0,step=0.1)
rurale = st.number_input('La taille de la population rurale',min_value=0.0,step=0.1)
urbanisation = st.number_input('Le taux d\'urbanisation de la province',min_value=0.0,step=0.01)
rente = st.number_input('La superficie cultivé des cultures de rente',min_value=0)
cereal = st.number_input('La superficie cultivé des céréales',min_value=0)
tmin = st.number_input('La température minimale de la province',min_value=0.0,step=0.1)
pluie = st.number_input('La pluviométrie au niveau de la province',min_value=0.0,step=0.1)

# if 'pluie' not in st.session_state:
#     st.session_state['pluie'] = '

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
if st.button('Prédire'):
    df=pd.DataFrame(df)
    result = model.predict(df)
    st.subheader('Le nombre de personnes partant de cette province est : {}'.format(int(result)))