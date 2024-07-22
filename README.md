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

![img.png](static/img/img-4.png)

- Agregar myapp a panel de admin

Directorio: polls/admin.py

```
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

## Parte 3 Vistas y rutas

- Nuevas vistas y parametros en la url

Directorio: polls/views.py
```
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

Directorio: polls/urls.py
```
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```
Nuevas urls:
  - http://localhost:8000/polls/1/
  - http://localhost:8000/polls/1/results/
  - http://localhost:8000/polls/1/vote/

- Modificar la vista principal de polls

Directorio: http://localhost:8000/polls/
En esta vista listaremos las preguntas y las agregaremos a la interfaz

```
from django.http import HttpResponse

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
```

- Crear una plantilla html 

Directorio: /templates/polls/index.html
```
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```
- Implementar la plantilla en la vista

Directorio: polls/views.py
```
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # Obtener template
    template = loader.get_template("polls/index.html")
    # Pasar datos a la vista
    context = {
        "latest_question_list": latest_question_list,
    }
    # Retornar la vista con los datos
    return HttpResponse(template.render(context, request))
```
- Simplificar el codigo con render()

Directorio: polls/views.py
```
from django.shortcuts import render

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)
```

- Modificar vista de detalle y agregar template con excepciones

Directorio: polls/views.py
```
from django.http import Http404
from django.shortcuts import render
from .models import Question


# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})
```
- Simplificar el codigo de pagina detalle 

Directorio: polls/views.py
```
from django.shortcuts import get_object_or_404, render

from .models import Question


# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})
```

- Modificar el template de detalle

Directorio: template/polls/detail.html

Accerder a datos para mostrarlos en la vista
```
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```

- Modificar el template de index cambiar la forma de uso de urls

Directorio: template/polls/index.html

Se utiliza el name unico para identificar la url
```
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
   <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
{% endfor %}
</ul>
```

- Evitar conflitos por nombres de url

Directorio: polls/urls.py
```
from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```
Para ello se agrega un nombre a la app
```
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```

## Parte 4 Implementación de interación con la pagina y datos en bd

- Actualización de la pagina detail

Directorio: template/polls/detail.html
```
<form action="{% url 'polls:vote' question.id %}" method="post">
    {% csrf_token %}
    <fieldset>
        <legend><h1>{{ question.question_text }}</h1></legend>
        {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
        {% for choice in question.choice_set.all %}
            <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
            <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
        {% endfor %}
    </fieldset>
    <input type="submit" value="Vote">
</form>
```

- Actualizar la vista que recibe los datos del form y bd

Directorio: polls/views.py:
```
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question

# ...
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
```

- Actualizar vista de reultados

Directorio: polls/views.py:
```
from django.shortcuts import get_object_or_404, render


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
```

- Crear template de resultados

```
  Directorio: polls/results.html
  
  <h1>{{ question.question_text }}</h1>
  
  <ul>
  {% for choice in question.choice_set.all %}
      <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
  {% endfor %}
  </ul>
  
  <a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```

- Usar vistas genéricas

Primero se modifica el archivo polls/urls.py
```
from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```

Luego se modificar el archivo polls/views.py, para utilizar vistas genericas
```
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    # same as above, no changes needed.
    ...
```

## Parte 5  Pruebas automatizadas