from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from askmeapp.models import *
from askmeapp.forms import *
from askmeapp import pagination_function




def index(request, page = '1'):
	myquestions = Question.objects.newest()
	popular_tags = Tag.objects.get_popular_tags()
	question_list = pagination_function.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/"
	return render(request, 'index.html', {"data": question_list, "popular_tags" : popular_tags}, )

def hot_questions(request, page = '1'):
	myquestions = Question.objects.hot()
	popular_tags = Tag.objects.get_popular_tags()
	question_list = pagination_function.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/hot/"
	return render(request, 'hot_questions.html', {"data": question_list, "popular_tags" : popular_tags}, )

def profile(request, user_name, page = '1'):
	myquestions = Question.objects.user_questions(user_name)
	profile = Profile.objects.get_by_name(user_name)
	popular_tags = Tag.objects.get_popular_tags()
	question_list = pagination_function.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/profile/" + profile[0].user.username + "/"
	return render(request, 'profile.html', {"data": question_list, "profile": profile[0], "popular_tags" : popular_tags}, )

def tag(request, tag, page = '1'):
	myquestions = Question.objects.tag_search(tag)
	popular_tags = Tag.objects.get_popular_tags()
	question_list = pagination_function.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/tag/" + tag + "/"		
	return render(request, 'tag.html', {"data": question_list, "tag" : tag,	"popular_tags" : popular_tags}, )

def single_question(request, id, page = '1'):
	question = Question.objects.get(pk=id)
	answers = question.answer_set.all()
	popular_tags = Tag.objects.get_popular_tags()
	answer_list = pagination_function.pagination(answers, 4, page)
	answer_list.paginator.baseurl = "/question/id" + id + "/"
	last_page_num = (answers.count() + 1) / 4 +1

	try:
		question = Question.objects.get(pk=id)
	except Question.DoesNotExist:
		raise Http404

	if request.method == "POST":
		answer_form = AnswerForm(request.POST)

		if answer_form.is_valid():
			answer = answer_form.save(question, request.user)
			return HttpResponseRedirect(reverse('question', kwargs={'id': question.id, 'page' : last_page_num})
										+ '#answer_' + str(answer.id))
	else:
		answer_form = AnswerForm()
	return render(request, 'question.html', {"question": question, "data" : answer_list,
											 "popular_tags" : popular_tags, "form" : answer_form},)

def developing(request):
	popular_tags = Tag.objects.get_popular_tags()
	return render(request, 'developing.html', {"popular_tags" : popular_tags},)


@login_required
def ask_question(request):
	popular_tags = Tag.objects.get_popular_tags()
	if request.method == "POST":
		form = QuestionForm(request.POST)
		if form.is_valid():
			q = form.save(request.user)
			return HttpResponseRedirect(reverse('question', kwargs={'id': q.id}))
	else:
		form = QuestionForm()
	return render(request, 'ask.html', {"popular_tags" : popular_tags, 'form': form},)


def login(request):
	popular_tags = Tag.objects.get_popular_tags()
	redirect = request.GET.get('continue', '/')

	if request.user.is_authenticated():
		return HttpResponseRedirect(redirect)

	if request.method == "POST":
		form = LoginForm(request.POST)

		if form.is_valid():
			auth.login(request, form.cleaned_data['user'])
			return HttpResponseRedirect(redirect)
	else:
		form = LoginForm()
	return render(request, 'login.html', {"popular_tags" : popular_tags, 'form': form},)

@login_required
def logout(request):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    return HttpResponseRedirect(redirect)

def signup(request):
	popular_tags = Tag.objects.get_popular_tags()
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')

	if request.method == "POST":
		form = SignupForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save()
			auth.login(request, user)
			return HttpResponseRedirect('/')
	else:
		form = SignupForm()

	return render(request, 'signup.html', {"popular_tags" : popular_tags, 'form': form},)


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

	
	

