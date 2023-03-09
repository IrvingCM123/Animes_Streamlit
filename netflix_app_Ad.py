import streamlit as st
import pandas as pd
import os
import numpy as np

doc = 'anime.csv'

st.set_page_config(layout="wide", page_title="Semantic Shakespeare",
                   page_icon=":busts_in_silhouette:")
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


@st.cache
def load_data(nrows):
    data = pd.read_csv(doc, index_col=0, encoding='latin-1')
    return data


def load_data_bydirector(name):
    data = pd.read_csv(doc, index_col=0, encoding='latin-1')
    filtered_data_bydirector = data[data["director"].str.contains(director)]
    return filtered_data_bydirector



def load_data_byname(name):
    data = pd.read_csv(doc, index_col=0, encoding='latin-1')
    filtered_data_byname = data[data["name"].str.upper().str.contains(name)]
    return filtered_data_byname


st.title("Netflix App")

data = load_data(500)

# --- LOGO ---#
st.sidebar.image("Credencial.jpg")
st.sidebar.write("Irving Rafael Conde Marin - S20006735")
st.sidebar.markdown("##")

# --- SIDEBAR FILTERS ---#
if st.sidebar.checkbox("Mostras todos los filmes"):
    st.write(data)

buscadorTitulo = st.sidebar.write("Titulo del filme")
buscador = st.sidebar.text_input("Titulo filme")
botonTitulo = st.sidebar.button("Buscar filmes")


director = st.sidebar.selectbox("Selecciona el director",
                                options=data['director'].unique())
botonDirector = st.sidebar.button("Buscar por director")


if botonTitulo:
    filterbyname = load_data_byname(buscador.upper())
    rows = filterbyname.shape[0]
    st.dataframe(filterbyname)

if botonDirector:
    filterbydirector = load_data_bydirector(director)
    rows = filterbydirector.shape[0]
    st.dataframe(filterbydirector)


st.title("Semantic   Shakespeare")
# st.image("images/semantic-shakespeare.png")
st.sidebar.image("Credencial.jpg")
st.sidebar.markdown(
    "Developed by [W.J.B. Mattingly](https://www.wjbmattingly.com) using [Streamlit](https://www.streamlit.io) and [txtAI](https://github.com/neuml/txtai)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.2")
query = st.sidebar.text_input("Query")
num_results = st.sidebar.number_input("Number of Results", 1, 2000, 20)
ignore_search_words = st.sidebar.checkbox("Ignore Search Words")
