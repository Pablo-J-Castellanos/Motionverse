#encoding:utf-8

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Pelicula(models.Model):
    idPelicula = models.AutoField(primary_key=True)
    titulo = models.TextField(verbose_name='Título', null=False)
    sinopsis = models.TextField(verbose_name='Sinopsis', null=True, blank=True)
    director = models.TextField(verbose_name='Director', null=True, blank=True)
    productor = models.TextField(verbose_name='Productor', null=True, blank=True)
    guionista = models.TextField(verbose_name='Guionista', null=True, blank=True)
    edad = models.TextField(verbose_name='Edad recomendada', null=True, blank=True)
    fecha = models.DateField(verbose_name='Fecha de Estreno', null=True, blank=True)
    duracion = models.IntegerField(verbose_name='Duración (en minutos)', null=True, blank=True)
    calificacion_critica = models.IntegerField(
        verbose_name='Calificación Crítica',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    calificacion_publico = models.IntegerField(
        verbose_name='Calificación Público',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    foto = models.URLField(verbose_name='foto', null=True, blank=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = []

class Genero(models.Model):
    idGenero = models.AutoField(primary_key=True)
    genero = models.TextField(verbose_name='Género', null=False)
    pelicula = models.ForeignKey(
        Pelicula, 
        on_delete=models.CASCADE, 
        related_name='generos'
    )

    def __str__(self):
        return self.genero
    
    class Meta:
        ordering = []
