from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
import json
from askmeapp.models import *
from askmeapp.forms import *
from askmeapp import pagination_function
from askmeapp.ajax_funcs import *




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

	question = get_object_or_404(Question, pk=id)
	answers = question.answer_set.all()
	popular_tags = Tag.objects.get_popular_tags()
	answer_list = pagination_function.pagination(answers, 4, page)
	answer_list.paginator.baseurl = "/question/id" + id + "/"
	last_page_num = (answers.count() + 1) / 4 + 1

	if request.method == "POST":
		answer_form = AnswerForm(request.POST)

		if answer_form.is_valid():
			answer = answer_form.save(question, request.user)
			return HttpResponseRedirect(reverse('question', kwargs={'id': question.id, 'page' : last_page_num})
										+ '#answer_' + str(answer.id))
	else:
		answer_form = AnswerForm()
	return render(request, 'question.html', {"question": question, "data" : answer_list, "new_question" : True,
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
			q = form.save(request.user, 0)
			return HttpResponseRedirect(reverse('question', kwargs={'id': q.id}))
	else:
		form = QuestionForm()
	return render(request, 'ask.html', {"popular_tags" : popular_tags, 'form': form},)
@login_required
def edit_question(request, id):
	question = get_object_or_404(Question, pk=id)
	if question.user != request.user:
		return HttpResponseRedirect(reverse('question', kwargs={'id': id}))
	popular_tags = Tag.objects.get_popular_tags()
	if request.method == "POST":
		form = QuestionForm(request.POST)
		if form.is_valid():
			q = form.save(request.user, id)
			return HttpResponseRedirect(reverse('question', kwargs={'id': q.id}))
	else:
		q = model_to_dict(question)
		tags = question.tags.all()
		q['tags'] = ''
		first = True
		for tag in tags:
			if first:
				q['tags'] = tag.text
				first = False
			else:
				q['tags'] = q['tags'] + ',' + tag.text

		q['category'] = question.category.title
		form = QuestionForm(q)
	return render(request, 'ask.html', {"popular_tags": popular_tags, 'form': form}, )


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

@login_required
def profile_edit(request):


	if request.method == "POST":
		form = ProfileEditForm(request.POST, request.FILES)

		if form.is_valid():
			form.save(request.user)
			form.status = True
			#return HttpResponseRedirect('/profile/' + request.user.username + '/')
	else:
		u = model_to_dict(request.user)
		up = request.user.profile
		u['information'] = up.information
		form = ProfileEditForm(u)
		form.status = False
	popular_tags = Tag.objects.get_popular_tags()
	return render(request, 'edit_profile.html', {"popular_tags" : popular_tags,'form': form},)

@login_required
def change_password(request):
	if request.method == "POST":
		form = ChangePasswordForm(request.POST)
		form.user = request.user
		if form.is_valid():
			form.save(request.user)
			form.status = True
			#return HttpResponseRedirect('/')
	else:
		form = ChangePasswordForm()
		form.user = request.user
	popular_tags=Tag.objects.get_popular_tags()
	return render(request, 'change_password.html', {"popular_tags": popular_tags, 'form': form}, )

def tag_list(request):
	tags = Tag.objects.order_by_name_with_question_count()
	popular_tags = Tag.objects.get_popular_tags()
	return render(request, 'tag_list.html', {"popular_tags": popular_tags, 'tag_list' : tags},)


@login_required_ajax
@require_POST
def question_like(request):
	if request.method == 'POST':
		user = request.user
		id = int(request.POST.get('id'))
		is_like = int(request.POST.get('like'))
		print request.POST
		question = get_object_or_404(Question, pk=id)
		if is_like == 1:
			QuestionLike.objects.like(question.id, user)
		else:
			QuestionLike.objects.dislike(question.id, user)
		question = get_object_or_404(Question, pk=id)
		if question.rating >= 0:
			qrating = '+' + str(question.rating)
			qstyleid = '#like'
		else:
			qrating = str(question.rating)
			qstyleid = '#dislike'

		if question.user.profile.rating >= 0:
			urating = '+' + str(question.user.profile.rating)
			ustyleid = '.like' + str(question.user.id) + '.like'
		else:
			urating = str(question.user.profile.rating)
			ustyleid = '.dislike' + str(question.user.id) + '.dislike'


	message = u'liked'

	ctx = {'message': message, 'qid' : question.id, 'qrating' : qrating, 'qstyleid' : qstyleid,
		   'uid' : question.user.id, 'urating' : urating, 'ustyleid' : ustyleid}

	return HttpResponse(json.dumps(ctx), content_type='application/json')

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



