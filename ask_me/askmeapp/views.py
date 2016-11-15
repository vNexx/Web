from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from askmeapp import models
from askmeapp import pagination_function
import random



questions = []
answers = []
tags = []
for i in xrange (1,4):
	tags.append({
		"tag" : "SomeTag"})
for i in xrange (1,300):
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
		"user_rating" : random.randint(-100,100),
		"user_name" : "RandomUser",
		"question_rating" : random.randint(-100,100),
		"tags" : tags
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
		"user_rating" : random.randint(-100,100),
		"answer_rating" : random.randint(-100,100)
		})

		


def index(request, page = '1'):
	user = { "user_is_logged" : False}	
	question_list = pagination_function.pagination(questions, 5, page)
	return render(request, 'index.html', {"questions": question_list, "user" : user}, )
    #return render(request, 'index.html', {'articles': models.Article.objects.all()} )

def hot_questions(request, page = '1'):
	user = { "user_is_logged" : True}
	question_list = pagination_function.pagination(questions, 5, page)
	return render(request, 'hot_questions.html', {"questions": question_list, "user" : user}, )

def profile(request, page = '1'):
	user = ({ 
		"user_is_logged" : True,
		"info" : " Some Random User Information Some Random User Information Some Random User\
		 Information Some Random User Information Some Random User Information Some Random User\
		 Information Some Random User Information Some Random User Information",
		"name" : "Jarvis",	
		"rating" : random.randint(-100,100)
		})
	question_list = pagination_function.pagination(questions, 5, page)
	return render(request, 'profile.html', {"questions": question_list, "user" : user}, )

def tag(request, tag, page = '1'):	
	user = { "user_is_logged" : True}
	question_list = pagination_function.pagination(questions, 5, page)		
	return render(request, 'tag.html', {"questions": question_list, "user" : user, "tag" : tag}, )

def single_question(request, page = '1'):
	user = { "user_is_logged" : True}
	answer_list = pagination_function.pagination(answers, 4, page)
	return render(request, 'question.html', {"question": questions[0], "answers" : answer_list, "user" : user},)

def developing(request):
	user = { "user_is_logged" : True}	
	return render(request, 'developing.html', {"user" : user},)

def ask_question(request):
	user = { "user_is_logged" : True}	
	return render(request, 'ask.html', {"user" : user},)

def login(request):
	user = { "user_is_logged" : False}
	return render(request, 'login.html', {"user" : user},)

def signup(request):
	user = { "user_is_logged" : False}
	return render(request, 'signup.html', {"user" : user},)


@csrf_exempt
def get_post_params(request):
    result = ['Hello, World!<br>']
    result.append('Post test:')
    result.append('<form method="post">')
    result.append('<input type="text" name = "params">')
    result.append('<input type="submit" value="Submit">')
    result.append('</form>')

    if request.method == 'GET':
        if request.GET.urlencode() != '':
            result.append('Get data:')            
            for key, value in request.GET.items():
                keyvalue=key+" = "+value
                result.append(keyvalue)

    if request.method == 'POST':
        result.append(request.POST.urlencode())
    return HttpResponse('<br>'.join(result))

	
	

