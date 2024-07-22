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

Directorio: mysite/settings.py

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

Directorio: myapp/urls.py

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

Por defecto django tiene integrado la base de datos sqlite
![img.png](static/img/img-1.png)

- Iniciar las tablas por defecto de django admin

```
python manage.py migrate
```

- crear un model para myapp

Directorio: myapp/models.py

```
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

- Crear migraciones implementadas en los models

```
    python manage.py makemigrations myapp
```

Directorio: myapp/migrations/
En el directorio mencionado almacenará las migraciones
![img.png](static/img/img-2.png)

- Ver en consola una migracion

```
    python manage.py sqlmigrate myapp <id_migracion>
```

- Verificar la integridad del proyecto

```
    python manage.py check
```

- Crear tablas segun las migraciones

```
    python manage.py migrate
```

- Ingresar al shell para manipular bd

```
    python manage.py shell
```

    - Indicar las tablas 
    ```
        from polls.models import Choice, Question
    ```
    - Obtner todos los registros de un model asociado a una tabla
     ```
        Question.objects.all()
     ```
    - Establecer zona horaria
    ```
        from django.utils import timezone
    ```
    - crear un registro en bd
    ```
        q = Question(question_text="What's new?", pub_date=timezone.now())
    ```
    - Guardar 
    ```
        q.save()
    ```
    - Obtener el id del registro creado
    ```
        q.id
    ```
    - Acceder a atributos y sus valores
   ```
        q.question_text
        q.pub_date
    ```
    - Actualizar valores
     ```
        q.question_text = "What's up?"
        q.save()
     ```
    - Filtrar por id
    ```
        Question.objects.filter(id=1)
    ```
    - Filtrar por atributos
   ```
    Question.objects.filter(question_text__startswith="What")
   ```
   - Filtrar por pk o llave primaria
   ```
    Question.objects.get(pk=1)
   ```
   - Utilizar metodos personalizados
    ```
    q = Question.objects.get(pk=1)
    q.was_published_recently()    
    ```
    - Ver objetos relacionados
    ```
    q = Question.objects.get(pk=1)
    q.choice_set.all()
    ```
    - Crear registros relacionados a otra tabla
     ```
        q = Question.objects.get(pk=1)
        q.choice_set.create(choice_text="Not much", votes=0)
     ```
    - Mostrar datos relacion inversa
     ```
       c = q.choice_set.create(choice_text="Just hacking again", votes=0)
       c.question
     ```
   - Listar datos de relacion de forma inversa
    ```
       c = q.choice_set.create(choice_text="Just hacking again", votes=0)
       c.question
       q.choice_set.all()
    ```
   - Mostrar numero de registros
    ```
       q.choice_set.count()
    ```
   - Eliminar un registro
    ```
       c = q.choice_set.filter(choice_text__startswith="Just hacking")
        c.delete()
    ```

Nota: salir del shell ctrl + d, si modificamos el model debemos cargar el archivo en shell de nuevo, si hay espacios de mas 
al inicio genera errores. "IndentationError: unexpected indent"

- Definir funcion str para visualizar datos de registros de bd

```
    import datetime
    
    from django.db import models
    from django.utils import timezone
    
    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField("date published")
    
        def __str__(self):
            return self.question_text
    
        def was_published_recently(self):
            return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    
    class Choice(models.Model):
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)
    
        def __str__(self):
            return self.choice_text
```

- Crear un usuario administrador
```
python manage.py createsuperuser
```
Es necesario agregar un user name, correo y contraseña
- Acceder con el usuario administrador creado
URL: http://localhost:8000/admin/

![img.png](static/img/img-3.png)

![img.png](static/img/img-3.png)