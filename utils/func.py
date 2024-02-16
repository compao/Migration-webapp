def charger():
    if data_file.name.split('.')[-1] in ['xlsx','xls']:
        data=pd.read_excel(data_file.read())
    else:
        data=pd.read_csv(data_file.read())
    try:
        data[cols] 
        st.succes('Données chargées avec succes!')
    except:
        st.error('Vos données ne correspondent pas')