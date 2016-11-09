from django.shortcuts import render
from django.http import HttpResponse
from askmeapp import models
import random



questions = []
answers = []
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
	answers.append({
		"text" : "Lorem, ipsum orci nam diam porta justo porttitor ornare massa - elementum,\
			sit a at. Sem, ligula sem pellentesque leo, sodales sed fusce molestie massa a\
			 commodo ligula tempus  ipsum, in sapien amet ornare rutrum amet tempus ligula\
			 curabitur - pellentesque. Justo ut arcu adipiscing eros vitae, diam, sit gravida,\
			 massa a ornare rutrum sem eget duis quisque vivamus. Nec pellentesque ligula, nibh\
			 ipsum quisque sit leo duis sapien ut. Eros leo sit diam eros quam massa diam congue\
			 lectus eros. Maecenas lorem nulla integer risus mattis odio sodales sem congue magna\
			 at duis sem sit mauris, justo, nam lorem lectus. ",
		"user_name" : "Loki",
		"user_rate" : random.randint(1,100),
		"answer_rate" : random.randint(1,100)
		})

		


def index(request):
	user = { "user_is_logged" : False}	
	return render(request, 'index.html', {"questions": questions, "user" : user}, )
    #return render(request, 'index.html', {'articles': models.Article.objects.all()} )



def single_question(request):
	user = { "user_is_logged" : True}	
	return render(request, 'question.html', {"question": questions[0], "answers" : answers, "user" : user},)


def ask_question(request):
	user = { "user_is_logged" : True}	
	return render(request, 'ask.html', {"user" : user},)

def login(request):
	user = { "user_is_logged" : False}
	return render(request, 'login.html', {"user" : user},)

def register(request):
	user = { "user_is_logged" : False}
	return render(request, 'register.html', {"user" : user},)
	
	

