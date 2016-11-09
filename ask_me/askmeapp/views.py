from django.shortcuts import render
from django.http import HttpResponse
from askmeapp import models
import random



questions = []
for i in xrange (1,31):
    questions.append({
        "title" : "Some Random Question Title?",
        "text" : "Lorem Ipsum is simply dummy text of the printing and typesetting industry.\
            Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,\
            when an unknown printer took a galley of type and scrambled it to make a type\
            specimen book. It has survived not only five centuries, but also the leap into\
            electronic typesetting, remaining essentially unchanged. It was popularised in\
            the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,\
            and more recently with desktop publishing software like Aldus PageMaker\
            including versions of Lorem Ipsum.",
        "id" : i,
        "user_rate" : random.randint(1,100),
	"user_name" : "Random User",
        "question_rate" : random.randint(1,100)
        })

def index(request):
	return render(request, 'index.html', {"questions": questions}, )
    #return render(request, 'index.html', {'articles': models.Article.objects.all()} )



def single_question(request):
	return render(request, 'question.html', {"qq": "text"},)


def ask_question(request):
	return render(request, 'ask.html', {"title": "New"},)
	

