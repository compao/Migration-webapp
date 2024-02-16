import time
import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import pickle
import xgboost as xgb
# import folium
# from streamlit_folium import folium_static
# from shapely.geometry import LineString

from sklearn.preprocessing import StandardScaler

MODEL_DE_SORTIE    = pickle.load(open('models/sortant/XGBoost Regression.pkl', 'rb'))
# MODEL_DE_DISTRIBUTION  = pickle.load(open('models/distribution/XGBoost Regression.pkl', 'rb'))
MODEL_DE_DISTRIBUTION = xgb.XGBRegressor()  # init model
MODEL_DE_DISTRIBUTION.load_model('models/distribution.bin')  # load data
def charger():
    if data_file!=None:
        if data_file.name.split('.')[-1] in ['xlsx','xls']:
            data=pd.read_excel(data_file.read(),index_col="Province")
        else:
            data=pd.read_csv(data_file.read(),index_col="Province")
        # data=data[data['Annee']==1996]
        # st.success('Données chargées avec succes!')
        return data 
    return None
def predict_sortie(data):
    d=StandardScaler().fit_transform(data)
    result = MODEL_DE_SORTIE.predict(d)
    result = data.join(pd.DataFrame(data=result,index=data.index,columns=['Sortie']))
    return relu(result,'Sortie')
def predict_distribution(data):
    d=StandardScaler().fit_transform(data)
    result = MODEL_DE_DISTRIBUTION.predict(d)
    result_dist= data.join(pd.DataFrame(data=result,index=data.index,columns=['Flux']))
    return pd.DataFrame(data=result,index=data.index,columns=['Flux']), relu(result_dist,'Flux').unstack()["Flux"]

def get_dist_data(d):
    d=result.reset_index()
    wtl=d.join(d,how='cross',lsuffix='_o',rsuffix='_d')
    return wtl[wtl["Province_o"]!=wtl["Province_d"]].set_index(['Province_o','Province_d'])
def sigmoid(d):
    return 1/(1+np.exp(-d))
n=lambda d: 0 if d<0 else np.ceil(d)
def relu(d,col):
    d[col]=[n(a) for a in d[col]]
    return d
# """def plot_map():
#     # Load your GeoDataFrame
#     gdf = gpd.read_file("../geo/provinces.geojson")

#     # Create a folium map
#     m = folium.Map(location=[gdf["geometry"].centroid.y.mean(), gdf["geometry"].centroid.x.mean()], zoom_start=5)

#     # Iterate through each row in the GeoDataFrame
#     for index, row in gdf.iterrows():
#         # Convert the GeoDataFrame geometry to a GeoJSON format for folium
#         geojson_data = folium.GeoJson(row["geometry"])
        
#         # Customize line width based on an attribute (e.g., "line_thickness")
#         line_width = row["line_thickness"]
#         geojson_data.style_function = lambda x: {'fillColor': 'blue', 'color': 'blue', 'weight': line_width}
        
#         # Create lines from polygon vertices and add them to the map
#         vertices = list(row["geometry"].exterior.coords)
#         lines = LineString(vertices)
#         folium.PolyLine(locations=lines.coords, color='red', weight=2).add_to(m)
        
#         # Add the GeoJSON data to the map
#         geojson_data.add_to(m)

#     # Display the folium map in Streamlit
#     st.title("Map with Polygons and Lines")
#     folium_static(m)
# """
cols=['Population','Densité', 'Masculinité', 'Urbain','Taux Urbanisation', 'Rural', 'Cereale', 'Rente', 'Tmin', 'Pluie']
wtl_cols=['Population_o','Population_d','Densité_o','Densité_d','Masculinité_o','Masculinité_d','Sortie_o','Cereale_o','Cereale_d','Rente_o','Rente_d','Distance','Tmin_o','Tmin_d','Pluie_o','Pluie_d','Taux Urbanisation_o','Taux Urbanisation_d']
#df=gpd.read_file('geo/provinces.geojson')

st.title("Distribution des flux migratoires")
st.info('Votre jeu de données doit contenir les colonnes suivantes:')
colonnes=pd.DataFrame(columns=cols)
colonnes
data_file=st.file_uploader("Veuiller charger un fichier Excel ou CSV",type=['csv','xlsx','xls'],label_visibility="visible")
try:
    data=charger()
    if(data[cols].isna().sum().max()==0):
        st.success('Données chargées avec succes!')
    else:
        st.error('Les données contiennent des valeurs nulles!')
    st.subheader("Prédiction des sorties par province.")
    # data[cols]
    result=predict_sortie(data[cols])
    #cd = result.sort_values(by='Sortie',ascending=True)
    st.bar_chart(result,y="Sortie")
    st.subheader("Distribution des sorties des provinces.")
    #Transformation des données entrées pour le modele de distribution
    wtl=get_dist_data(result)
    #Récupération des distances entre provinces
    distances=pd.read_excel("../data/processed_data/wtlDistance.xlsx",index_col=[0,1])
    #Jointure des données avec les distances
    wtl=wtl.join(distances)
    # wtl
    #Prédiction des flux migratoire entre provinces
    wtol,result_dist=predict_distribution(wtl[wtl_cols])
    #st.subheader("Matrice de distribution des sorties des provinces.")
    result_dist
    # st.balloons()
except:
    st.error("Veuiller charger les données")
