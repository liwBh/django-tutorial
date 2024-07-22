# Django tutorial liwbh

## Parte 1 creando aplicacion en Django

- Instalación de python
- Crear proyecto

```
    django-admin startproject mysite
```
Esto creará un mysite directorio en su directorio actual.
- Crear entorno virtual
```
    python -m venv ./venv
 ```
- Activar el entorno vitual
```
    python -m venv ./venv/bin/activate
```
- Verificar el funcionamiento del servidor
```
    python manage.py runserver
```
- Crear aplicación
```
    python manage.py startapp myapp
```
- Agregar aplicación al pryecto

Directorio: myapp/settings.py
```
    INSTALLED_APPS = [
        ...
        'myapp',
    ]
```

- Crear vista

Directorio: myapp/views.py

```
    from django.http import HttpResponse
    
    def index(request):
        return HttpResponse("Hello, world. You're at the polls index.")
```

- Crear url
```
    from django.urls import path
    
    from . import views
    
    urlpatterns = [
        path("", views.index, name="index"),
    ]
```
- Agregar las url de una app al proyecto

Directorio: mysite/urls.py
```
    from django.contrib import admin
    from django.urls import include, path
    
    urlpatterns = [
        path("polls/", include("polls.urls")),
        path("admin/", admin.site.urls),
    ]
```

- Verificar que se puede acceder a la vista
```
    python manage.py runserver
```

url: http://localhost:8000/polls/

![img.png](static/img/img.png)

## Parte 2 Configuración de base de datos