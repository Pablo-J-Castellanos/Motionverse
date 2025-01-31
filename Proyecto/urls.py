from django.contrib import admin
from django.urls import path
from main import views, populateDB

urlpatterns = [
    path('',views.index),
    # Peliculas
    path('peliculas/', views.cargar_datos_peliculas, name='peliculas'),
    path('mostrar_peliculas/', views.mostrar_peliculas, name='mostrar_peliculas'),
    path('ver_pelicula/<str:titulo>/', views.ver_pelicula, name='ver_pelicula'),
    
    path('buscar_pelicula_por_titulo/', views.buscar_pelicula_por_titulo, name='buscar_pelicula_por_titulo'),
    path('buscar_peliculas_por_fecha/', views.buscar_peliculas_por_fecha, name='buscar_peliculas_por_fecha'),
    path('buscar_peliculas_por_genero/', views.buscar_peliculas_por_genero, name='buscar_peliculas_por_genero'),
    path('buscar_mejores_peliculas_por_año/', views.buscar_buscar_mejores_peliculas_por_año, name='buscar_mejores_peliculas_por_año'),
    path('buscar_peliculas_por_rango_años/', views.buscar_peliculas_por_rango_años, name='buscar_peliculas_por_rango_años'),
    path('buscar_peliculas_por_duracion/', views.buscar_peliculas_por_duracion, name='buscar_peliculas_por_duracion'),
    
    # Series
    path('series/', views.cargar_datos_series, name='series'),
    path('mostrar_series/', views.mostrar_datos_series, name='mostrar_series'),
    path('serie/<str:titulo>/', views.ver_serie, name='ver_serie'),
    
    path('buscar_series_por_titulo/', views.buscar_series_por_titulo, name='buscar_series_por_titulo'),
    path('buscar_series_por_genero/', views.buscar_series_por_genero, name='buscar_series_por_genero'),
    path('buscar_series_por_sinopsis/', views.buscar_series_por_sinopsis, name='buscar_series_por_sinopsis'),
    path('editar_fecha_serie/', views.editar_fecha_serie, name='editar_fecha_serie'),
    path('eliminar_series/', views.eliminar_series_por_calificacion, name='eliminar_series'),

    ]
