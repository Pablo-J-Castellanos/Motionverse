#encoding:utf-8
from main.models import Pelicula, Genero
from main.populateDB import populate
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.shortcuts import render
from main.whoosh.woosh import almacenar_datos
from whoosh.index import open_dir
from main.beautiful_soup.bs import almacenar_bd
from django.shortcuts import redirect
from datetime import datetime
from whoosh.writing import AsyncWriter
from whoosh.qparser import QueryParser, OrGroup, plugins, MultifieldParser


def index(request):
    return render(request, 'index.html',{'STATIC_URL':settings.STATIC_URL})

##############################  PELÍCULAS  ##############################

def cargar_datos_peliculas(request):
    pel = []  
    gen = []
    mensaje = None  

    try:
        peliculas, generos = almacenar_bd()

        populate(peliculas, generos)

        pel = Pelicula.objects.all()  
        gen = Genero.objects.all()  
        
        total_peliculas = pel.count()
        
        mensaje = "Datos cargados exitosamente."
    except Exception as e:
        mensaje = f"Error al cargar datos: {str(e)}"
        print("Error:", mensaje)
    
    return render(request, 'peliculas.html', {
        'mensaje': mensaje,
        'peliculas': pel,
        'generos': gen,
        'total_peliculas': total_peliculas,        
        'STATIC_URL': settings.STATIC_URL,
    })

def mostrar_peliculas(request):
    
    pel = Pelicula.objects.all()
    gen = Genero.objects.all()
    
    total_peliculas = pel.count()
    
    return render(request, 'peliculas.html', {
        'peliculas': pel,
        'generos': gen,
        'total_peliculas': total_peliculas,
        'STATIC_URL': settings.STATIC_URL,
    })

def ver_pelicula(request, titulo):
    pelicula = get_object_or_404(Pelicula, titulo=titulo)
    generos = Genero.objects.filter(pelicula=pelicula)

    return render(request, 'ver_pelicula.html', {
        'pelicula': pelicula,
        'generos': generos,
        'STATIC_URL': settings.STATIC_URL,
    })

def buscar_pelicula_por_titulo(request):
    resultados = None 
    query = request.GET.get('query', '')

    if query:
        resultados = Pelicula.objects.filter(titulo__icontains=query)

    return render(request, 'buscar_pelicula_por_titulo.html', {
        'resultados': resultados,
        'query': query,
        'STATIC_URL': settings.STATIC_URL
    })
    
def buscar_peliculas_por_fecha(request):
    resultados = []
    mensaje = None

    if request.method == "POST":
        fecha_str = request.POST.get("fecha")
        try:
            fecha = datetime.strptime(fecha_str, "%b %d, %Y")

            resultados = Pelicula.objects.filter(fecha__gt=fecha).order_by('fecha')
        except ValueError:
            mensaje = "Formato de fecha inválido. Por favor, usa el formato: Mes Dia, Año"

    return render(request, 'buscar_peliculas_por_fecha.html', {
        'resultados': resultados,
        'mensaje': mensaje,
        'STATIC_URL': settings.STATIC_URL
    })
    
def buscar_peliculas_por_genero(request):
    resultados = []
    generos = Genero.objects.values_list('genero', flat=True).distinct()
    mensaje = None

    if request.method == "POST":
        genero_seleccionado = request.POST.get("genero")
        try:
            
            resultados = Pelicula.objects.filter(generos__genero=genero_seleccionado).distinct()
        except Exception as e:
            mensaje = f"Error al buscar películas: {str(e)}"

    return render(request, 'buscar_peliculas_por_genero.html', {
        'resultados': resultados,
        'generos': generos,
        'mensaje': mensaje,
        'STATIC_URL': settings.STATIC_URL
    })
    
def buscar_buscar_mejores_peliculas_por_año(request):
    resultados = []
    mensaje = None

    if request.method == "POST":
        año = request.POST.get("año")
        try:
            año = int(año)
            
            resultados = Pelicula.objects.filter(fecha__year=año).order_by('-calificacion_publico')[:5]
        except ValueError:
            mensaje = "Por favor, introduce un año válido."
        except Exception as e:
            mensaje = f"Error al buscar películas: {str(e)}"

    return render(request, 'buscar_mejores_peliculas_por_año.html', {
        'resultados': resultados,
        'mensaje': mensaje,
        'STATIC_URL': settings.STATIC_URL
    })
    
def buscar_peliculas_por_rango_años(request):
    resultados = []
    mensaje = None

    if request.method == "POST":
        año_inicio = request.POST.get("año_inicio")
        año_fin = request.POST.get("año_fin")
        try:
            año_inicio = int(año_inicio)
            año_fin = int(año_fin)

            if año_inicio > año_fin:
                mensaje = "El año de inicio debe ser menor o igual al año final."
            else:
                resultados = Pelicula.objects.filter(fecha__year__gte=año_inicio, fecha__year__lte=año_fin).order_by('fecha')
        except ValueError:
            mensaje = "Por favor, introduce años válidos."
        except Exception as e:
            mensaje = f"Error al buscar películas: {str(e)}"

    return render(request, 'buscar_peliculas_por_rango_años.html', {
        'resultados': resultados,
        'mensaje': mensaje,
        'STATIC_URL': settings.STATIC_URL
    })

def buscar_peliculas_por_duracion(request):
    resultados = None
    mensaje = None

    if request.method == "POST":
        duracion = request.POST.get("duracion")
        try:
            
            duracion = int(duracion)
            
            resultados = Pelicula.objects.filter(duracion__lte=duracion).order_by('duracion')
            if not resultados.exists():
                mensaje = "No se encontraron resultados para la búsqueda."
        except ValueError:
            mensaje = "Por favor, introduce una duración válida (en minutos)."
        except Exception as e:
            mensaje = f"Error al buscar películas: {str(e)}"

    return render(request, 'buscar_peliculas_por_duracion.html', {
        'resultados': resultados,
        'mensaje': mensaje,
        'STATIC_URL': settings.STATIC_URL,
    })
    
    
################################  SERIES  ##############################

def cargar_datos_series(request):
    datos = []
    mensaje = None
    total_series = 0

    try:
        datos = almacenar_datos()
        total_series = len(datos)
        mensaje = "Datos cargados exitosamente."
    except Exception as e:
        mensaje = f"Error al cargar datos: {str(e)}"
    
    print(mensaje)

    return render(request, 'series.html', {
        'mensaje': mensaje,
        'datos': datos,
        'total_series': total_series,
        'STATIC_URL': settings.STATIC_URL,
    })

def mostrar_datos_series(request):
    datos = []
    mensaje = None
    total_series = 0

    try:
        ix = open_dir("Index")
        
        with ix.searcher() as searcher:
            results = searcher.documents()

            for result in results:
                datos.append({k: result.get(k) for k in ['titulo', 'sinopsis', 'director', 'creator', 'screenwriter', 'producer', 'network', 'rating', 'language', 'fecha', 'calificacion', 'genero', 'foto']})
            total_series = len(datos)
            
            datos = sorted(datos, key=lambda x: int(x['calificacion']) if x['calificacion'] else 0, reverse=True)

        mensaje = "Series mostradas exitosamente."
    except Exception as e:
        mensaje = f"Error al mostrar series: {str(e)}"
    
    print(mensaje)

    return render(request, 'series.html', {
        'mensaje': mensaje,
        'datos': datos,
        'total_series': total_series,
        'STATIC_URL': settings.STATIC_URL,
    })
    
def ver_serie(request, titulo):
    serie = None
    mensaje = None

    try:
        ix = open_dir("Index")

        with ix.searcher() as searcher:
            parser = QueryParser("titulo", ix.schema)
            query = parser.parse(f'"{titulo}"')

            results = searcher.search(query, limit=1)
            if results:
                serie = {k: results[0].get(k) for k in results[0].fields()}
            else:
                mensaje = f"No se encontró la serie con el título: {titulo}"
    except Exception as e:
        mensaje = f"Error al buscar la serie: {str(e)}"

    return render(request, 'ver_serie.html', {
        'serie': serie,
        'mensaje': mensaje,
        'STATIC_URL': settings.STATIC_URL,
    })

def buscar_series_por_titulo(request):
    resultados = []
    mensaje = None

    titulo_busqueda = request.GET.get('titulo')
    if titulo_busqueda:
            try:
                ix = open_dir("Index")
                with ix.searcher() as searcher:
                    
                    query = QueryParser("titulo", ix.schema).parse(titulo_busqueda)
                    
                    results = searcher.search(query)
                    
                    resultados = [
                        {k: result.get(k) for k in [
                            'titulo', 'sinopsis', 'director', 'creator',
                            'screenwriter', 'producer', 'network', 'rating',
                            'language', 'fecha', 'calificacion', 'genero', 'foto'
                        ]}
                        for result in results
                    ]

                if not resultados:
                    mensaje = f"No se encontraron series que coincidan con '{titulo_busqueda}'."
            except Exception as e:
                mensaje = f"Error al buscar series: {str(e)}"
    else:
            mensaje = "Por favor, ingresa un título para buscar."

    return render(request, 'buscar_series_por_titulo.html', {
        'resultados': resultados,
        'mensaje': mensaje,
        'STATIC_URL': settings.STATIC_URL,
    })
    
def buscar_series_por_genero(request):
    resultados = []
    mensaje = None
    generos_disponibles = set()

    try:

        ix = open_dir("Index")
        with ix.searcher() as searcher:
            for result in searcher.documents():
                if result.get('genero'):
                    generos = result['genero'].split(',')
                    generos_disponibles.update(genero.strip() for genero in generos)

        generos_disponibles = sorted(list(generos_disponibles))

        if request.method == "POST":
            genero_seleccionado = request.POST.get("genero", "").strip()
            if genero_seleccionado:
                try:
                    with ix.searcher() as searcher:
                        parser = QueryParser("genero", ix.schema)
                        query = parser.parse(f'"{genero_seleccionado}"')

                        resultados = [{k: result.get(k) for k in ['titulo', 'sinopsis', 'director', 'creator', 'screenwriter', 'producer', 'network', 'rating', 'language', 'fecha', 'calificacion', 'genero', 'foto']} for result in searcher.search(query, limit=None)]
                    if not resultados:
                        mensaje = f"No se encontraron series para el género '{genero_seleccionado}'."
                except Exception as e:
                    mensaje = f"Error al buscar series: {str(e)}"
            else:
                mensaje = "Por favor, selecciona un género para buscar."
    except Exception as e:
        mensaje = f"Error al cargar los géneros: {str(e)}"

    return render(request, 'buscar_series_por_genero.html', {
        'resultados': resultados,
        'mensaje': mensaje,
        'generos': generos_disponibles,
        'STATIC_URL': settings.STATIC_URL,
    })


def buscar_series_por_sinopsis(request):
    resultados = []
    mensaje = None

    sinopsis_busqueda = request.GET.get('sinopsis')
    if sinopsis_busqueda:
            try:

                ix = open_dir("Index")
                with ix.searcher() as searcher:
                    
                    query = QueryParser("sinopsis", ix.schema).parse(sinopsis_busqueda)
                    
                    results = searcher.search(query)

                    resultados = [
                        {k: result.get(k) for k in ['titulo', 'sinopsis', 'director', 'creator','screenwriter', 'producer', 'network', 'rating','language', 'fecha', 'calificacion', 'genero', 'foto']}
                        for result in results
                    ]
                if not resultados:
                    mensaje = f"No se encontraron series con '{sinopsis_busqueda}' en la sinopsis."
            except Exception as e:
                mensaje = f"Error al buscar series: {str(e)}"
    else:
            mensaje = "Por favor, ingresa un texto para buscar."
    
    return render(request, 'buscar_series_por_sinopsis.html', {
        'resultados': resultados,
        'mensaje': mensaje,
        'STATIC_URL': settings.STATIC_URL,
    })


def editar_fecha_serie(request):
    resultados = []
    mensaje = None

    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        nueva_fecha = request.POST.get("fecha", "").strip()

        if titulo and nueva_fecha:
            try:
                fecha_formateada = datetime.strptime(nueva_fecha, "%b %d, %Y")

                ix = open_dir("Index")
                with ix.searcher() as searcher:
                    parser = QueryParser("titulo", ix.schema)
                    query = parser.parse(f'"{titulo}"') 

                    resultados = [
                        {k: result.get(k) for k in [
                            'id', 'titulo', 'sinopsis', 'director', 'creator',
                            'screenwriter', 'producer', 'network', 'rating',
                            'language', 'fecha', 'calificacion', 'genero', 'foto'
                        ]}
                        for result in searcher.search(query, limit=1)
                    ]

                    if resultados:
                        documento = resultados[0]
                        documento_id = documento['id']

                        with AsyncWriter(ix) as writer:
                            writer.update_document(id=documento_id, titulo=documento['titulo'], sinopsis=documento['sinopsis'], director=documento['director'], creator=documento['creator'], screenwriter=documento['screenwriter'], producer=documento['producer'], network=documento['network'], rating=documento['rating'], language=documento['language'], fecha=fecha_formateada, calificacion=documento['calificacion'], genero=documento['genero'], foto=documento['foto'])

                        with ix.searcher() as new_searcher:
                            updated_results = [{**{k: result.get(k) for k in ['titulo', 'sinopsis', 'director', 'creator', 'screenwriter', 'producer', 'network', 'rating', 'language', 'calificacion', 'genero', 'foto']}, 'fecha': result['fecha'].strftime("%b %d, %Y") if result['fecha'] else None} for result in new_searcher.search(query, limit=1)]

                        resultados = updated_results
                        mensaje = f"La fecha de estreno de '{titulo}' se actualizó correctamente."
                    else:
                        mensaje = f"No se encontró una serie con el título exacto '{titulo}'."
            except ValueError:
                mensaje = "Por favor, ingresa una fecha válida en el formato 'Nov 6, 2021'."
            except Exception as e:
                mensaje = f"Error al editar la serie: {str(e)}"
        else:
            mensaje = "Por favor, ingresa un título y una fecha válida."

    return render(request, 'editar_fecha_serie.html', {
        'resultados': resultados,
        'mensaje': mensaje,
        'STATIC_URL': settings.STATIC_URL,
    })

def eliminar_series_por_calificacion(request):
    mensaje = None
    series_eliminadas = []
    calificacion_minima = request.POST.get("calificacion", "").strip()

    if calificacion_minima.isdigit():
        calificacion_minima = int(calificacion_minima)
        try:
            ix = open_dir("Index")
            with ix.searcher() as searcher:
                results = searcher.documents()
                series_eliminadas = [
                    {k: result.get(k) for k in [
                        'id', 'titulo', 'sinopsis', 'director', 'creator',
                        'screenwriter', 'producer', 'network', 'rating',
                        'language', 'fecha', 'calificacion', 'genero', 'foto'
                    ]}
                    for result in results
                    if result.get("calificacion") and int(result["calificacion"]) < calificacion_minima
                ]

            with ix.writer() as writer:
                for serie in series_eliminadas:
                    writer.delete_by_term("id", serie["id"])
            
            if series_eliminadas:
                mensaje = f"Series con calificación menor a {calificacion_minima} eliminadas exitosamente."
            else:
                mensaje = f"No se encontraron series con calificación menor a {calificacion_minima}."
        except Exception as e:
            mensaje = f"Error al eliminar series: {str(e)}"
    else:
        mensaje = "Por favor, ingresa una calificación válida."

    return render(request, 'eliminar_series_por_calificacion.html', {
        'mensaje': mensaje,
        'series_eliminadas': series_eliminadas,
        'STATIC_URL': settings.STATIC_URL
    })
