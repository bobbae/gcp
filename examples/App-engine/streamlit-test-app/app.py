#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 16:33:16 2021

@author: praneeth
"""

import streamlit as st
import pandas as pd

import plotly.express as px





st.title("Iris Streamlit App")
st.markdown("This is a demo Streamlit app.")

@st.cache(persist=True)
def load_data():
    df = pd.read_csv("https://datahub.io/machine-learning/iris/r/iris.csv")
    return(df)



def run():
    st.subheader("Iris Data Loaded into a Pandas Dataframe.")
    
    df = load_data()
    
    
    
    disp_head = st.sidebar.radio('Select DataFrame Display Option:',('Head', 'All'),index=0)
   
    
   
    #Multi-Select
    #sel_plot_cols = st.sidebar.multiselect("Select Columns For Scatter Plot",df.columns.to_list()[0:4],df.columns.to_list()[0:2])
    
    #Select Box
    #x_plot = st.sidebar.selectbox("Select X-axis Column For Scatter Plot",df.columns.to_list()[0:4],index=0)
    #y_plot = st.sidebar.selectbox("Select Y-axis Column For Scatter Plot",df.columns.to_list()[0:4],index=1)
    
    
    if disp_head=="Head":
        st.dataframe(df.head())
    else:
        st.dataframe(df)
    #st.table(df)
    #st.write(df)
    
    
    #Scatter Plot
    fig = px.scatter(df, x=df["sepallength"], y=df["sepalwidth"], color="class",
                 size='petallength', hover_data=['petalwidth'])
    
    fig.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
   
    st.write("\n")
    st.subheader("Scatter Plot")
    st.plotly_chart(fig, use_container_width=True)
    
    
    #Add images
    #images = ["<image_url>"]
    #st.image(images, width=600,use_container_width=True, caption=["Iris Flower"])
   
    
   
    
   
if __name__ == '__main__':
    run()    