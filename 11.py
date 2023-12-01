import streamlit as st
import pickle
import pandas as pd
import os
import numpy as np
import altair as alt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

model = pickle.load(open('model_prediksi_harga_mobil.sav', 'rb'))

@st.cache(suppress_st_warning=True)
def get_fvalue(val):    
    feature_dict = {"No":1,"Yes":2}    
    for key,value in feature_dict.items():        
        if val == key:            
            return value
        
def get_value(val,my_dict):    
    for key,value in my_dict.items():        
        if val == key:            
            return value
        
app_mode = st.sidebar.selectbox('Select Page',['Home','Prediction'])
if app_mode=='Home':
    st.title('CAR DATASET')
    st.image('mobil.jpg')
    st.header('Dataset: ')
    data = pd.read_csv('CarPrice.csv')
    st.write(data)
    st.header('City MPG vs Highway MPG')
    st.bar_chart(data[['citympg','highwaympg']])
    st.header('CAR HORSE POWER')
    st.bar_chart(data[['horsepower']])
elif app_mode == 'Prediction': 
    st.title('CAR PRICE PREDICTION: ')
    # st.radio('Select the Fuel Type',['Gas','Diesel'])
    horsepower = st.number_input('Set Horse Power', 48,288)
    highwaympg = st.number_input('Set Highway MPG', 16,54)
    curbweight = st.number_input('Set Curb Weight', 1488,4066)
    # cylinder = st.slider('Select Cylinder Number', 4,6)


    if st.button('Prediksi'):
        car_prediction = model.predict([[highwaympg, curbweight, horsepower]])

        harga_mobil_str = np.array(car_prediction)
        harga_mobil_float = float(harga_mobil_str[0])

        harga_mobil_formated = "{:.2f}".format(harga_mobil_float)
        if float(harga_mobil_formated) < 0:
            st.write("MOBIL TIDAK DITEMUKAN")
        else:
            st.write("HASIL PREDIKSI HARGA MOBIL: $",harga_mobil_formated)
