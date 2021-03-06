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
	question_list = pagination_function.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/"
	return render(request, 'index.html', {"data": question_list}, )

def hot_questions(request, page = '1'):
	myquestions = Question.objects.hot()
	question_list = pagination_function.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/hot/"
	return render(request, 'hot_questions.html', {"data": question_list}, )

def profile(request, user_name, page = '1'):
	myquestions = Question.objects.user_questions(user_name)
	profile = Profile.objects.get_by_name_with_question_count(user_name)
	p2 = Profile.objects.get_by_name_with_answer_count(user_name)

	question_list = pagination_function.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/profile/" + profile[0].user.username + "/"
	return render(request, 'profile.html', {"data": question_list, "profile": profile[0],
											'answers_count' : p2[0].answers_count}, )

def tag(request, tag, page = '1'):
	myquestions = Question.objects.tag_search(tag)
	question_list = pagination_function.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/tag/" + tag + "/"		
	return render(request, 'tag.html', {"data": question_list, "tag" : tag}, )

def single_question(request, id, page = '1'):

	question = get_object_or_404(Question, pk=id)
	answers = question.answer_set.all()
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
											 "form" : answer_form},)

def developing(request):
	return render(request, 'developing.html', {},)


@login_required
def ask_question(request):
	if request.method == "POST":
		form = QuestionForm(request.POST)
		if form.is_valid():
			q = form.save(request.user, 0)
			return HttpResponseRedirect(reverse('question', kwargs={'id': q.id}))
	else:
		form = QuestionForm()
	return render(request, 'ask.html', {'form': form},)
@login_required
def edit_question(request, id):
	question = get_object_or_404(Question, pk=id)
	if question.user != request.user:
		return HttpResponseRedirect(reverse('question', kwargs={'id': id}))
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
	return render(request, 'ask.html', {'form': form}, )


def login(request):
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
	return render(request, 'login.html', {'form': form},)

@login_required
def logout(request):
	redirect = request.GET.get('continue', '/')
	auth.logout(request)
	return HttpResponseRedirect(redirect)

def signup(request):
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

	return render(request, 'signup.html', {'form': form},)

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
	return render(request, 'edit_profile.html', {'form': form},)

@login_required
def change_password(request):
	if request.method == "POST":
		form = ChangePasswordForm(request.POST)
		form.user = request.user
		if form.is_valid():
			form.save(request.user)
			form.status = True
			auth.login(request, form.user)
			#return HttpResponseRedirect('/')
	else:
		form = ChangePasswordForm()
		form.user = request.user
	return render(request, 'change_password.html', {'form': form}, )

def tag_list(request):
	tags = Tag.objects.order_by_name_with_question_count()
	return render(request, 'tag_list.html', {'tag_list' : tags},)


def date_search(request, month, day, year, page = '1'):
	year = int(year)
	month = int(month)
	day = int(day)
	search_date = datetime.date(year, month, day)
	questions = Question.objects.date_search(search_date)
	question_list = pagination_function.pagination(questions, 5, page)
	question_list.paginator.baseurl = "/questions/" + str(year) + "/" + str(month) + "/" + str(day) + "/"
	return render(request, 'dates.html', {"data" : question_list, 'date': search_date}, )


@login_required_ajax
@require_POST
def answer_check(request):
	ansid = int(request.POST.get('ansid'))
	qid = int(request.POST.get('qid'))
	question = get_object_or_404(Question, pk=qid)
	if request.user == question.user:
		answer = get_object_or_404(Answer, pk=ansid)
		answer.is_correct = not answer.is_correct
		answer.save()
		response = {'ansid' : str(ansid), 'qid' : str(qid), 'iscorrect' : answer.is_correct}

		return HttpResponse(json.dumps(response), content_type='application/json')


@login_required_ajax
@require_POST
def question_like(request):
	if request.method == 'POST':
		user = request.user
		id = int(request.POST.get('id'))
		is_like = int(request.POST.get('like'))
		question = get_object_or_404(Question, pk=id)

		if question.rating >= 0:
			qstyleid = '.askme__question-rate.like' + str(question.id) + '.like.pull-right'
		else:
			qstyleid = '.askme__question-rate.dislike' + str(question.id) + '.dislike.pull-right'

		if question.user.profile.rating >= 0:
			ustyleid = '.likeu' + str(question.user.id) + '.like'
		else:
			ustyleid = '.dislikeu' + str(question.user.id) + '.dislike'

		if is_like == 1:
			qLike = QuestionLike.objects.like(question.id, user)
		else:
			qLike = QuestionLike.objects.dislike(question.id, user)
		question = get_object_or_404(Question, pk=id)

		if question.rating >= 0:
			qrating = '+' + str(question.rating)
			qstyle = 'askme__question-rate like' + str(question.id) + ' like pull-right'
		else:
			qrating = str(question.rating)
			qstyle = 'askme__question-rate dislike' + str(question.id) + ' dislike pull-right'

		if question.user.profile.rating >= 0:
			urating = '+' + str(question.user.profile.rating)
			ustyle = 'likeu' + str(question.user.id) + ' like'
		else:
			urating = str(question.user.profile.rating)
			ustyle = 'dislikeu' + str(question.user.id) + ' dislike'
		likebuttonid = '#l' + str(question.id)
		dislikebuttonid = '#d' + str(question.id)
		likebuttonstyle = 'btn btn-success btn-md likebutton'
		dislikebuttonstyle = 'btn btn-danger btn-md dislikebutton'

		if qLike.is_liked:
			likebuttonstyle = likebuttonstyle + ' btn-liked'
		elif qLike.is_disliked:
			dislikebuttonstyle = dislikebuttonstyle + ' btn-disliked'

		response = {'qrating': qrating, 'qstyleid': qstyleid, 'qstyle': qstyle,
			   'urating': urating, 'ustyleid': ustyleid, 'ustyle': ustyle,
			   'likebuttonid': likebuttonid, 'likebuttonstyle': likebuttonstyle,
			   'dislikebuttonid': dislikebuttonid, 'dislikebuttonstyle': dislikebuttonstyle}


	return HttpResponse(json.dumps(response), content_type='application/json')



@login_required_ajax
@require_POST
def answer_like(request):
	if request.method == 'POST':
		user = request.user
		id = int(request.POST.get('id'))
		is_like = int(request.POST.get('like'))
		answer = get_object_or_404(Answer, pk=id)
		if answer.rating >= 0:
			astyleid = '.askme__question-rate.alike' + str(answer.id) + '.like'
		else:
			astyleid = '.askme__question-rate.adislike' + str(answer.id) + '.dislike'

		if answer.user.profile.rating >= 0:
			ustyleid = '.likeu' + str(answer.user.id) + '.like'
		else:
			ustyleid = '.dislikeu' + str(answer.user.id) + '.dislike'

		if is_like == 1:
			aLike = AnswerLike.objects.like(answer.id, user)
		else:
			aLike = AnswerLike.objects.dislike(answer.id, user)
		answer = get_object_or_404(Answer, pk=id)

		if answer.rating >= 0:
			arating = '+' + str(answer.rating)
			astyle = 'askme__question-rate alike' + str(answer.id) + ' like'
		else:
			arating = str(answer.rating)
			astyle = 'askme__question-rate adislike' + str(answer.id) + ' dislike'

		if answer.user.profile.rating >= 0:
			urating = '+' + str(answer.user.profile.rating)
			ustyle = 'likeu' + str(answer.user.id) + ' like'
		else:
			urating = str(answer.user.profile.rating)
			ustyle = 'dislikeu' + str(answer.user.id) + ' dislike'
		likebuttonid = '#al' + str(answer.id)
		dislikebuttonid = '#ad' + str(answer.id)
		likebuttonstyle = 'btn btn-success btn-md alikebutton'
		dislikebuttonstyle = 'btn btn-danger btn-md adislikebutton'

		if aLike.is_liked:
			likebuttonstyle = likebuttonstyle + ' btn-liked'
		elif aLike.is_disliked:
			dislikebuttonstyle = dislikebuttonstyle + ' btn-disliked'

		response = {'arating': arating, 'astyleid': astyleid, 'astyle': astyle,
			   		'urating': urating, 'ustyleid': ustyleid, 'ustyle': ustyle,
			   		'likebuttonid': likebuttonid, 'likebuttonstyle': likebuttonstyle,
			   		'dislikebuttonid': dislikebuttonid, 'dislikebuttonstyle': dislikebuttonstyle}

		return HttpResponse(json.dumps(response), content_type='application/json')

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



