#encoding:utf-8

from main.models import Pelicula, Genero
from datetime import datetime

def populate(peliculas, generos):
    """
    Popula la base de datos con las listas de películas y géneros.
    """
    # Para que no haya duplicados
    Pelicula.objects.all().delete()
    Genero.objects.all().delete()

    for pelicula in peliculas:
        nueva_pelicula = Pelicula.objects.create(
            titulo=pelicula['titulo'],
            sinopsis=pelicula['sinopsis'],
            director=pelicula['director'],
            productor=pelicula['productor'],
            guionista=pelicula['guionista'],
            edad=pelicula['edad'],
            fecha=datetime.strptime(pelicula['fecha'], "%b %d, %Y") if pelicula['fecha'] else None,
            duracion=pelicula['duracion'],
            calificacion_critica=pelicula['calificacion_c'],
            calificacion_publico=pelicula['calificacion_u'],
            foto=pelicula['foto']
        )

    for genero in generos:
        pelicula = Pelicula.objects.get(titulo=genero['titulo_pelicula'])
        Genero.objects.create(
            genero=genero['genero'],
            pelicula=pelicula
        )
