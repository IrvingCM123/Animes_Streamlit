import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import os
import numpy as np
from PIL import Image

image = Image.open('Yohane.jpeg')
doc = 'anime.csv'

st.set_page_config(layout="wide", page_title="Anime List", page_icon=image)
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("Anime List DataSet")


@st.cache
def load_data(nrows):
    data = pd.read_csv(doc, index_col=0, encoding='latin-1', nrows=nrows)
    return data


@st.cache
def load_data_byname(name):
    data = pd.read_csv(doc, index_col=0, encoding='latin-1')
    filtered_data_byname = data[data["name"].str.upper().str.contains(name)]
    return filtered_data_byname


@st.cache
def load_data_bygenere(genero):
    data = pd.read_csv(doc, index_col=0, encoding='latin-1')
    filtered_data_bygenere = data[data["genre"].str.contains(genero, na=False)]
    return filtered_data_bygenere


@st.cache
def load_data_byepisodes(episode):
    data = pd.read_csv(doc, index_col=0, encoding='latin-1')
    filtered_data_byepisodes = data[data["episodes"].astype(
        str).str.upper().str.contains(episode)]
    return filtered_data_byepisodes


############ Almacenar Información#############################
data = load_data(500)
save_data = pd.read_csv(doc, delimiter=',')
save_data = load_data(50)

# --- LOGO ---#
st.sidebar.image("Yohane.jpeg")
st.sidebar.write("Irving Rafael Conde Marin - S20006735")
st.sidebar.markdown("##")

# --- SIDEBAR FILTERS ---#
if st.sidebar.checkbox("Desplegar todos los animes guardados"):
    st.write(data)

buscadorTitulo = st.sidebar.write("Buscar Anime especifico: ")
buscador = st.sidebar.text_input("Nombre")
botonTitulo = st.sidebar.button("Buscar")

Genere = st.sidebar.selectbox("Selecciona un genero",
                              options=data['genre'].unique())
BotonGenere = st.sidebar.button("Buscar por genero")

# Episode = st.sidebar.selectbox("Selecciona cantidad de capitulos",
#                             options=data['episodes'].unique())
Episode = st.sidebar.write("Buscar por capitulos: ")
episode = st.sidebar.text_input("Capitulo")
BotonEpisore = st.sidebar.button("Buscar por cantidad de capitulos")

##### Guardar datos de episodios para el histograma ####################
save_data_forHistrograma = pd.DataFrame(save_data)

save_data_forHistrograma_ep = save_data_forHistrograma['episodes'].astype(
    float)
save_data_forHistrograma_ep = np.array(
    save_data_forHistrograma_ep).astype(float)

limite_Histograma = save_data_forHistrograma_ep.max()
limite_Histograma = int(limite_Histograma)

if st.sidebar.checkbox('Mostrar histograma'):
    mostrar = np.histogram(save_data_forHistrograma_ep, bins=limite_Histograma,
                           range=(save_data_forHistrograma_ep.min(),
                                  save_data_forHistrograma_ep.max()),
                           weights=None,
                           density=False)[0]
    st.write("Histograma acerca de los episodios de los animes registrados")
    st.bar_chart(mostrar)

# Grafica de barras ##############3
save_data_for_Barras = pd.DataFrame(save_data)

save_data_for_Barras_rating = save_data_for_Barras['rating'].astype(
    float)
save_data_for_Barras_name = save_data_for_Barras['name'].astype(
    str)

save_data_for_Barras_rating = np.array(
    save_data_for_Barras_rating)

save_data_for_Barras_name = np.array(
    save_data_for_Barras_name)

if st.sidebar.checkbox('Mostrar grafica de barras'):
    dataframe, axis = plt.subplots()
    axis.bar(save_data_for_Barras_name, save_data_for_Barras_rating, color = 'blue')
    axis.set_xlabel('Nombre')
    axis.set_ylabel('Rating')
    axis.set_title('Rating de animes')
             
    st.write("Grafica de barras, acerca de los animes y su rating de popularidad")
    st.pyplot(dataframe)

##############
save_data_for_Scatter = pd.DataFrame(save_data)
rng = np.random.RandomState(0)

save_data_for_Barras_rating = save_data_for_Barras['rating'].astype(
    float)

save_data_for_Barras_members = save_data_for_Barras['members'].astype(
    float)

if st.sidebar.checkbox('Mostrar grafica de dispersión'):
    dataframe, axis = plt.subplots()
    axis.scatter(save_data_for_Barras_rating,
                save_data_for_Barras_members,
                color='blue',
                alpha=0.4,
                cmap='viridis')

    st.write("Grafica de dispersión acerca de la cantidad de seguidores de los animes en comparación de su rating")
    st.pyplot(dataframe)


if botonTitulo:
    filterbyname = load_data_byname(buscador.upper())
    rows = filterbyname.shape[0]
    st.dataframe(filterbyname)

if BotonGenere:
    filtered_data_bygenere = load_data_bygenere(Genere)
    rows = filtered_data_bygenere.shape[0]
    st.dataframe(filtered_data_bygenere)

if BotonEpisore:
    filtered_data_byepisodes = load_data_byepisodes(episode.upper())
    rows = filtered_data_byepisodes.shape[0]
    st.dataframe(filtered_data_byepisodes)
