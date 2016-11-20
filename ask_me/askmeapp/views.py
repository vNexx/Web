from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from askmeapp.models import *
from askmeapp import pagination_function
import random



# questions = []
# answers = []
# tags = []
# for i in xrange (1,4):
# 	tags.append({
# 		"tag" : "SomeTag"})
# for i in xrange (1,300):
# 	questions.append({
# 		"title" : "Some Random Question Title?",
# 		"text" : "Lorem Ipsum is simply dummy text of the printing and typesetting industry.\
# 			Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,\
# 			when an unknown printer took a galley of type and scrambled it to make a type\
# 			specimen book. It has survived not only five centuries, but also the leap into\
# 			electronic typesetting, remaining essentially unchanged. It was popularised in\
# 			the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,\
# 			and more recently with desktop publishing software like Aldus PageMaker\
# 			including versions of Lorem Ipsum.",
# 		"id" : i,
# 		"user_rating" : random.randint(-100,100),
# 		"user_name" : "RandomUser",
# 		"question_rating" : random.randint(-100,100),
# 		"tags" : tags
# 		})
# 	answers.append({
# 		"text" : "Lorem, ipsum orci nam diam porta justo porttitor ornare massa - elementum,\
# 			sit a at. Sem, ligula sem pellentesque leo, sodales sed fusce molestie massa a\
# 			 commodo ligula tempus  ipsum, in sapien amet ornare rutrum amet tempus ligula\
# 			 curabitur - pellentesque. Justo ut arcu adipiscing eros vitae, diam, sit gravida,\
# 			 massa a ornare rutrum sem eget duis quisque vivamus. Nec pellentesque ligula, nibh\
# 			 ipsum quisque sit leo duis sapien ut. Eros leo sit diam eros quam massa diam congue\
# 			 lectus eros. Maecenas lorem nulla integer risus mattis odio sodales sem congue magna\
# 			 at duis sem sit mauris, justo, nam lorem lectus. ",
# 		"user_name" : "Loki",
# 		"user_rating" : random.randint(-100,100),
# 		"answer_rating" : random.randint(-100,100)
# 		})

		


def index(request, page = '1'):
	user = { "user_is_logged" : False}
	myquestions = Question.objects.newest()
	popular_tags = Tag.objects.get_popular_tags()
	question_list = pagination_function.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/"
	return render(request, 'index.html', {"data": question_list, "user" : user, "popular_tags" : popular_tags}, )

def hot_questions(request, page = '1'):
	user = { "user_is_logged" : True}
	myquestions = Question.objects.hot()
	popular_tags = Tag.objects.get_popular_tags()
	question_list = pagination_function.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/hot/"
	return render(request, 'hot_questions.html', {"data": question_list, "user" : user, "popular_tags" : popular_tags}, )

def profile(request, user_name, page = '1'):
	user = {"user_is_logged": True}
	myquestions = Question.objects.user_questions(user_name)
	profile = Profile.objects.get_by_name(user_name)
	popular_tags = Tag.objects.get_popular_tags()
	question_list = pagination_function.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/profile/" + profile[0].user.username + "/"
	return render(request, 'profile.html', {"data": question_list, "profile": profile[0], "user" : user,
											"popular_tags" : popular_tags}, )

def tag(request, tag, page = '1'):	
	user = { "user_is_logged" : True}
	myquestions = Question.objects.tag_search(tag)
	popular_tags = Tag.objects.get_popular_tags()
	question_list = pagination_function.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/tag/" + tag + "/"		
	return render(request, 'tag.html', {"data": question_list, "user" : user, "tag" : tag,
										"popular_tags" : popular_tags}, )

def single_question(request, id, page = '1'):
	user = { "user_is_logged" : True}
	question = Question.objects.get(pk=id)
	answers = question.answer_set.all()
	popular_tags = Tag.objects.get_popular_tags()
	answer_list = pagination_function.pagination(answers, 4, page)
	answer_list.paginator.baseurl = "/question/id" + id + "/"
	return render(request, 'question.html', {"question": question, "data" : answer_list, "user" : user,
											 "popular_tags" : popular_tags},)

def developing(request):
	user = { "user_is_logged" : True}
	popular_tags = Tag.objects.get_popular_tags()
	return render(request, 'developing.html', {"user" : user, "popular_tags" : popular_tags},)

def ask_question(request):
	user = { "user_is_logged" : True}
	popular_tags = Tag.objects.get_popular_tags()
	return render(request, 'ask.html', {"user" : user, "popular_tags" : popular_tags},)

def login(request):
	user = { "user_is_logged" : False}
	popular_tags = Tag.objects.get_popular_tags()
	return render(request, 'login.html', {"user" : user, "popular_tags" : popular_tags},)

def signup(request):
	user = { "user_is_logged" : False}
	popular_tags = Tag.objects.get_popular_tags()
	return render(request, 'signup.html', {"user" : user, "popular_tags" : popular_tags},)


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

	
	

