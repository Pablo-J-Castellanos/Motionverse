#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import re, os, shutil
from datetime import datetime
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, KEYWORD, ID, NUMERIC
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
from whoosh.analysis import RegexTokenizer, LowercaseFilter



# lineas para evitar error SSL
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def extraer_series():
    lista_series = []
    lista_pagina = extraer_serie("https://editorial.rottentomatoes.com/guide/best-netflix-shows-and-movies-to-binge-watch-now/")
    lista_series.extend(lista_pagina)

    return lista_series

def extraer_serie(url):
    
    lista =[]
    
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")
    lista_link_series = s.find("div", class_="articleContentBody").find_all("div", class_="row countdown-item")
    if lista_link_series:
        lista_link_series = s.find("div", class_="articleContentBody").find_all("div", class_="row countdown-item")
    else:
        lista_link_series = []
    for link_serie in lista_link_series:
        
        serie= link_serie.find("div", class_="col-sm-6 col-full-xs")
        
        url_detalle = serie.a['href']
        
        f = urllib.request.urlopen("https:"+url_detalle)
        s = BeautifulSoup(f, "lxml")
        
        #PARA OBTENER EL TITULO Y LA CALIFICACION
        tit_cal= link_serie.find("div", class_="col-sm-18 col-full-xs countdown-item-content")
        
        # PARA OBTENER LA FOTO
        foto_link = link_serie.find("div", class_="col-sm-6 col-full-xs")
        
        foto= foto_link.find("img", class_="article_poster")['src']
        # print(foto)
        
        
        titulo = tit_cal.find("div", class_="article_movie_title").find("h2").find("a").string.strip()
        #print(titulo)
        
        calificacion = tit_cal.find("div", class_="article_movie_title").find("span", class_="tMeterScore").string.strip().replace('%', '')
        #print("Calificacion:", calificacion)
        
    
        #PARA OBTENER EL RESTO DE ATRIBUTOS
        datos = s.find("section", class_="media-info")
        atributos = datos.find_all("div", class_="category-wrap")
        
        sinopsis_crudo = datos.find("div", class_="content-wrap").find("div", class_="synopsis-wrap").find_all("rt-text")
        sinopsis = sinopsis_crudo[1].string.strip()
        #print("Sinopsis:", sinopsis)
        
        director = None
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Director":
                rt_links = wrap.find_all("rt-link", {"data-qa": "item-value"})
                if rt_links:
                    director = ", ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                break
            
            # SI LA SERIE NO TIENE DIRECTOR
            else:
                director = "Unavailable"

        #print("Director:", director)
        
        creator = None
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Creator":
                rt_links = wrap.find_all("rt-link", {"data-qa": "item-value"})
                if rt_links:
                    creator = ", ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                break
            
            # SI LA SERIE NO TIENE CREADOR
            else:
                creator = "Unavailable"

        #print("Creator:", creator)
        
        screenwriter = None
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Screenwriter":
                rt_links = wrap.find_all("rt-link", {"data-qa": "item-value"})
                if rt_links:
                    screenwriter = ", ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                break
            
            # SI LA SERIE NO TIENE GUIONISTA
            else:
                screenwriter = "Unavailable"

        #print("Screenwriter:", screenwriter)
        
        producer = None
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Executive Producer":
                rt_links = wrap.find_all("rt-link", {"data-qa": "item-value"})
                if rt_links:
                    producer = ", ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                break
            
            # SI LA SERIE NO TIENE PRODUCTOR
            else:
                producer = "Unavailable"

        #print("Producer:", producer)

        network = None
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Network":
                rt_links = wrap.find_all("rt-text", {"data-qa": "item-value"})
                if rt_links:
                    network = ", ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                break
            
            # SI LA SERIE NO TIENE CANAL DE DISTRIBUCION
            else:
                network = "Unavailable"

        #print("Network:", network)
        
        rating = None
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Rating":
                rt_links = wrap.find_all("rt-text", {"data-qa": "item-value"})
                if rt_links:
                    rating = ", ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                break
            
            # SI LA SERIE NO TIENE CALIFICACION POR EDAD
            else:
                rating = "Sin calificar"

        #print("Rating:", rating)
        
        language = None
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Original Language":
                rt_links = wrap.find_all("rt-text", {"data-qa": "item-value"})
                if rt_links:
                    language = ", ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                break
            
            # SI LA SERIE NO TIENE IDIOMA
            else:
                language = "Unavailable"

        #print("Language:", language)
        
        fecha = None
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})

            if label and label.get_text(strip=True) == "Release Date":
                rt_links = wrap.find("rt-text", {"data-qa": "item-value"})           
                if rt_links:
                    fecha = rt_links.get_text()
                    fecha = datetime.strptime(fecha, "%b %d, %Y")

        #print("Fecha:", fecha)
        
        genero = set()
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Genre":
                rt_links = wrap.find_all("rt-link", {"data-qa": "item-value"})
                genero_crudo = ", ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                
                for genre in genero_crudo.split(","):
                    genero.add(genre.strip())
                    
        genero = ", ".join(genero)
        #print("Genero:", genero)

           
        lista.append((titulo,sinopsis,director,creator,screenwriter,producer,network,rating,language,fecha,calificacion,genero,foto))
        
    return lista


def almacenar_datos():
    case_insensitive_analyzer = RegexTokenizer() | LowercaseFilter()
    
    schem = Schema(id=ID(stored=True, unique=True), titulo=TEXT(stored=True, analyzer=case_insensitive_analyzer), sinopsis=TEXT(stored=True, phrase=False),
                   director=TEXT(stored=True, phrase=True), creator=TEXT(stored=True, phrase=True), screenwriter=TEXT(stored=True, phrase=False),
                   producer=TEXT(stored=True, phrase=False), network=TEXT(stored=True, phrase=True), rating=TEXT(stored=True, phrase=True),
                   language=TEXT(stored=True, phrase=False), fecha=DATETIME(stored=True), calificacion=NUMERIC(stored=True, numtype=int),
                   genero=KEYWORD(stored=True, commas=True), foto=TEXT(stored=True))
    
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    ix = create_in("Index", schema=schem)
    writer = ix.writer()
    
    lista_series = extraer_series()
    datos_almacenados = []
    
    for serie in lista_series:
        id_unico = str(serie[0]).lower().replace(" ", "-")
        serie_dict = {'id': id_unico, 'titulo': str(serie[0]), 'sinopsis': str(serie[1]), 'director': str(serie[2]), 'creator': str(serie[3]), 'screenwriter': str(serie[4]), 'producer': str(serie[5]), 'network': str(serie[6]), 'rating': str(serie[7]), 'language': str(serie[8]), 'fecha': serie[9], 'calificacion': int(serie[10]), 'genero': str(serie[11]), 'foto': str(serie[12])}
        datos_almacenados.append(serie_dict)
        
        writer.add_document(id=serie_dict['id'],titulo=serie_dict['titulo'],sinopsis=serie_dict['sinopsis'],director=serie_dict['director'],creator=serie_dict['creator'],screenwriter=serie_dict['screenwriter'],producer=serie_dict['producer'],network=serie_dict['network'],rating=serie_dict['rating'],language=serie_dict['language'],fecha=serie_dict['fecha'],calificacion=serie_dict['calificacion'],genero=serie_dict['genero'],foto=serie_dict['foto'])

    writer.commit()
    return datos_almacenados

