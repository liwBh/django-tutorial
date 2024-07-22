from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question
#from django.template import loader
#from django.http import Http404
from django.urls import reverse
from django.db.models import F
from django.views import generic

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)
    # template = loader.get_template("polls/index.html")
    # context = {
    #     "latest_question_list": latest_question_list,
    # }
    #return HttpResponse(template.render(context, request))
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    #return HttpResponse("You're looking at question %s." % question_id)
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})



def results(request, question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

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
    #return HttpResponse("You're voting on question %s." % question_id)
    # obtenemos el registro
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Recuperamos la opción seleccionada del formulario
        selected_choice = question.choice_set.get(pk=request.POST["choice"])

        #validamos que la opción seleccionada sea válida
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
        # Actualizamos la cantidad de votos de la opción seleccionada
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Redireccionamos a la página de resultados
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
