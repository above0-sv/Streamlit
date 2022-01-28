# Importamos 
import streamlit as st
import pandas as pd
import numpy as np
import spacy

import matplotlib.pyplot as plt
import seaborn as sns
from intertools import combinations
from wordcloud import WordCloud
from textblob import TextBlob 

# TAKE WEIGHT INPUT in kgs

# give a title to our app
st.title('Above Zero Sentimental Analysis')

st.subheader("Enter your text to verify the comment")
tweet  = st.text_input(" ", "please type here...")

# compare status value
x=TextBlob(tweet)
sentiment_polarity=x.sentiment.polarity

# check if the button is pressed or not
if(st.button('Submit')):
    
    #result = x.title()
    
    if(sentiment_polarity < 0):
        st.error("The given tweet looks Negative")
    elif(sentiment_polarity ==0):
        st.warning("The given tweet looks Neutral")
    elif(sentiment_polarity > 0 ):
        st.success("The given tweet looks Positive ")

# Para obtener la lista de "stopwords" y asi descartarlas
import nltk
from nltk.corpus import stopwords

#Generación de lista de signos de puntuación
import string  

def limpiar_puntuacion_stopwords(texto):
  """
  Funcion para limpiar el string

  #Modificado de la siguiente fuente: https://antonio-fernandez-troyano.medium.com/nube-de-palabras-word-cloud-con-python-a-partir-de-varias-webs-111e94220822

  Parameters 
  ---------------
  texto (str)       -> Texto a limpiar

  Returns
  ---------------
  texto_limpio (str) -> Texto limpio luego de sacarle signos de puntuacion y stopwords

  """
  puntuacion = []
  for s in string.punctuation:
      puntuacion.append(str(s))
  sp_puntuacion = ["¿", "¡", "“", "”", "…", ":", "–", "»", "«", "?", "!"]    

  puntuacion += sp_puntuacion

  #Reemplazamos signos de puntuación por "":
  for p in puntuacion:
      texto_limpio = texto.lower().replace(p,"")

  for p in puntuacion:
      texto_limpio = texto_limpio.replace(p,"")

  #Reemplazamos stop_words por "":    
  for stop in stop_words:
      texto_limpio_lista = texto_limpio.split()
      texto_limpio_lista = [i.strip() for i in texto_limpio_lista]
      try:
          while stop in texto_limpio_lista: texto_limpio_lista.remove(stop)
      except:
          print("Error")
          pass
      texto_limpio= " ".join(texto_limpio_lista)

  return texto_limpio


def generar_nube_de_palabras(input, uploded_file = None):  
  """
  Funcion para hacer la nube de palabras en base a un .csv especifico que tenga una columna "ShareCommentary" como se encuentra
  en el archivo Share.csv que nos proporciona LinkedIn
  
  Parameters
  ------------------
  input        -> Para decidir si se usa el 'template' o se toma el archivo cargandolo ('file')
  uploded_file -> Informacion el csv cargado
  
  
  Returns
  ------------------
  None
  """
  if input == 'file':
    df_shares = pd.read_csv(uploded_file)
  elif input == 'template':
    url = 'https://raw.githubusercontent.com/napo178/Above/main/analisis_comments_tiktok.csv'
    df_shares = pd.read_csv(url)
    
  texto_de_publicaciones = df_shares['comment']
  texto_de_publicaciones = [i for i in texto_de_publicaciones if type(i) == str]

  # Uso set para borrar repetidos
  texto = [i for i in set(texto_de_publicaciones) if type(i) == str]

  texto = ''.join(texto)

  # Limpiamos
  clean_texto = limpiar_puntuacion_stopwords(texto)

  # Hacemos el wordcloud
  word_cloud = WordCloud(height=800, width=800, background_color='white',max_words=100, min_font_size=5).generate(clean_texto)
  fig, ax = plt.subplots()

  # Sacamos los ticks de los ejes 
  ax.axis('off')

  ax.imshow(word_cloud)
  title_alignment = """
  <style> #the-title { 
  text-align: center
  }
  </style>"""

  st.markdown(title_alignment, unsafe_allow_html=True)

  st.title("Wordcloud 😀")
  fig  # 👈 Draw a Matplotlib chart
  
  fig.savefig("nube.png")
  

# Obtengo la lista de stopwords (conectores, preposiciones, etc) en espanol gracias a nltk
nltk.download('stopwords')
stop_words = stopwords.words('spanish')


if __name__ == "__main__": 

  st.title('☁️ Nube de palabras Chegg ☁️')
  st.markdown("Creado por Above Zero")

  st.markdown('## Presioná el botón **Browse files** y luego seleccioná tu archivo *Shares.csv*')
  st.markdown("Visualizar datos ya cargados, presioná el siguiente botón")      
  pressed = st.button('Ver ejemplo')

  # Cargamos template
  if pressed:
     generar_nube_de_palabras('template')
  
  # Subir archivo
  uploaded_file = st.file_uploader("Seleccioná el archivo")

  # Cargamos desde archivo
  if uploaded_file is not None:
    generar_nube_de_palabras('file', uploaded_file)


import spacy
import streamlit as st 
from itertools import combinations 
import pandas as pd 


st.title('Similarity app')

col1, col2, col3 = st.beta_columns(3)
with col1:
    word_1 = st.text_input('word 1', 'shirt')
with col2:
    word_2 = st.text_input('word 2', 'jeans')
with col3:
    word_3 = st.text_input('word 3', 'apple')

nlp = spacy.load("en_core_web_md")
tokens = nlp(f"{word_1} {word_2} {word_3}")

# get combination of tokens
comb = combinations(tokens, 2)

most_similar = 0
match_tokens = None
compared_tokens = []
similarities = []
for token in list(comb):
    similarity = token[0].similarity(token[1])
    compared_tokens.append(token)
    similarities.append(similarity)
    if similarity > most_similar:

        most_similar = similarity
        match_tokens = token

st.write(f'{match_tokens[0]} and {match_tokens[1]} are the most similar with a similarity of {round(most_similar*100, 2)}%')
st.write('## Results')

df = pd.DataFrame({
  'Tokens': compared_tokens,
  'Similarity': similarities
}).sort_values(by='Similarity', ascending=False)

df




   
