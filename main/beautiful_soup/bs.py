#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3
import lxml
from datetime import datetime

# lineas para evitar error SSL
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def almacenar_bd():

    peliculas = []
    generos = []
    
    f = urllib.request.urlopen("https://editorial.rottentomatoes.com/guide/best-computer-animated-movies-of-all-time/")
    s = BeautifulSoup(f, "lxml")
    
    lista_link_peliculas = s.find("div", class_="articleContentBody").find_all("div", class_="row countdown-item")
    
    
    for link_pelicula in lista_link_peliculas:
        
        peli= link_pelicula.find("div", class_="col-sm-6 col-full-xs")
        
        f = urllib.request.urlopen(peli.a['href'])
        s = BeautifulSoup(f, "lxml")
        
        # PARA OBTENER EL TITULO Y LAS DOS CALIFICACIONES
        peli2= link_pelicula.find("div", class_="col-sm-18 col-full-xs countdown-item-content")
        
        # PARA OBTENER LA FOTO
        foto_link = link_pelicula.find("div", class_="col-sm-6 col-full-xs")
        
        foto= foto_link.find("img", class_="article_poster")['src']
        # print(foto)
        
        # PARA OBTENER EL RESTO DE ATRIBUTOS
        datos = s.find("section", class_="media-info")
        
        # PARA IR OBTENIENDO CADA ATRIBUTO NECESARIO
        atributos = datos.find_all("div", class_="category-wrap")
        # print(atributos)
               
        titulo = peli2.find("div",class_="article_movie_title").find("h2").find("a").string.strip()
        #print(titulo)
        
        sinopsis_crudo = datos.find("div", class_="content-wrap").find("div", class_="synopsis-wrap").find_all("rt-text")
        sinopsis = sinopsis_crudo[1].string.strip()
        
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Director":
                rt_links = wrap.find_all("rt-link", {"data-qa": "item-value"})
                director = ", ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                # print("director:", director)
    
        for wrap in atributos:
            # Se busca el primer rt-text, que es en el que pone el nombre del atributo
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Producer":  # Si es el que queremos se buscan los rt-link que es donde está el valor
                rt_links = wrap.find_all("rt-link", {"data-qa": "item-value"})
                productor = ", ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                # print("productor:", productor)

        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Screenwriter":
                rt_links = wrap.find_all("rt-link", {"data-qa": "item-value"})
                guionista = ", ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                # print("guionista:", guionista)
        
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Rating":
                rt_links = wrap.find_all("rt-text", {"data-qa": "item-value"})
                edad = " ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                # print("edad:", edad)
                
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Release Date (Theaters)":
                rt_links = wrap.find_all("rt-text", {"data-qa": "item-value"})
                fecha_crudo = " ".join(rt_link.get_text(strip=True) for rt_link in rt_links).split(",")
                fecha = datetime.strptime(", ".join(fecha_crudo[:2]), "%b %d, %Y")
                fecha_formateada = fecha.strftime("%b %d, %Y")  # PARA TENER SOLO LA FECHA SIN HORA
                # print("fecha:", fecha_formateada)

                
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Runtime":
                rt_links = wrap.find_all("rt-text", {"data-qa": "item-value"})
                duracion_crudo = " ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                duracion = convertir_a_minutos(duracion_crudo)
                # print("duracion:", duracion)
        
        # SACAR LAS DOS CALIFICACIONES
        calificaciones_crudo = peli2.find("div",class_="article_movie_title").find("h2").find_all("span", class_="tMeterScore")
        
        # PARA QUITAR EL % DE LAS CALIFICACIONES Y ASI TRATARLO COMO UN NUMERO
        for i in range(len(calificaciones_crudo)):
            calificaciones_crudo[i] = [cal.string.strip()[:-1] for cal in calificaciones_crudo[i]]
        
        calificaciones_c = calificaciones_crudo[0][0]
        # print(calificaciones_c)
                
        calificaciones_u = calificaciones_crudo[1][0]
        # print(calificaciones_u)
        
        genero = set()
        for wrap in atributos:
            label = wrap.find("rt-text", {"data-qa": "item-label"})
            
            if label and label.get_text(strip=True) == "Genre":
                rt_links = wrap.find_all("rt-link", {"data-qa": "item-value"})
                genero_crudo = ", ".join(rt_link.get_text(strip=True) for rt_link in rt_links)
                
                for genre in genero_crudo.split(","):
                    genero.add(genre.strip())
                #print("generos:", genero)

        peliculas.append({
            'titulo': titulo,
            'sinopsis': sinopsis,
            'director': director,
            'productor': productor,
            'guionista': guionista,
            'edad': edad,
            'fecha': fecha_formateada,
            'duracion': duracion,
            'calificacion_c': calificaciones_c,
            'calificacion_u': calificaciones_u,
            'foto': foto
        })

        for gen in list(genero):
            generos.append({
                'genero': gen,
                'titulo_pelicula': titulo
            })

            
    return peliculas, generos



def convertir_a_minutos(duracion_texto):
    try:
        duracion_texto = str(duracion_texto)
        horas = 0
        minutos = 0
        if "h" in duracion_texto:
            horas = int(duracion_texto.split("h")[0].strip())
        if "m" in duracion_texto:
            minutos = int(duracion_texto.split("h")[-1].split("m")[0].strip())
        return horas * 60 + minutos
    except ValueError:
        return 0


