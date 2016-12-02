# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models import Count
import datetime
# Create your models here.

class QuestionManager(models.Manager):
	def newest(self):
		return self.order_by('-created')

	def hot(self):
		return self.order_by('-rating')

	def tag_search(self, input_tag):
		return self.filter(tags__text = input_tag)

	def published(self):
		return self.filter(is_published=True)
	def user_questions(self, user_name):
		return self.filter(user__username = user_name)

class ProfileManager(models.Manager):
	def get_by_name(self, user_name):
		return self.filter(user__username = user_name)

class TagManager(models.Manager):
	# adds number of questions to each tag
	def with_question_count(self):
		return self.annotate(questions_count=Count('question'))

	# sorts tags using number of questions
	def order_by_question_count(self):
		return self.with_question_count().order_by('-questions_count')

	def order_by_name_with_question_count(self):
		return  self.with_question_count().order_by('text')

	def get_popular_tags(self):
		return self.order_by_question_count().all()[:10]

class Tag(models.Model):
	text = models.CharField(max_length=50, verbose_name='Tag', unique=True)
	style_number = models.IntegerField(default=1)
	objects = TagManager()
	def __unicode__(self):
		return self.text

class Category(models.Model):
	title = models.CharField(max_length = 50, verbose_name=u'Категория')

	def __unicode__(self):
		return self.title


class Question(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length = 255, verbose_name=u'Заголовок')
	text = models.TextField(verbose_name=u'Текст')
	rating = models.IntegerField(default=0, verbose_name=u'Рэйтинг')
	is_published = models.BooleanField(default=False, verbose_name=u'Опубликована')
	created = models.DateTimeField(default=datetime.datetime.now)
	tags = models.ManyToManyField(Tag)
	category = models.ForeignKey(Category, default=1)
	objects = QuestionManager()

	def get_absolute_url(self):
		return '/question/id%d/' % self.id
	def __unicode__(self):
		return self.title



	def __unicode__(self):
		return self.text

class Profile(models.Model):
	user = models.OneToOneField(User)
	avatar = models.ImageField(upload_to='uploads', default="uploads/user_avatar.jpeg")
	information = models.TextField(default="My info")
	rating = models.IntegerField( default=0)

	objects = ProfileManager()

	def __unicode__(self):
		return unicode(self.user)

class Answer(models.Model):
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	text = models.TextField()
	rating = models.IntegerField(default = 0)
	created = models.DateTimeField(default = datetime.datetime.now)
	is_correct = models.BooleanField(default = False)


class QuestionLikeManager(models.Manager):
	def like(self, id, user):
		compose_key = str(user) + str(id)
		question = Question.objects.get(pk=id)
		try:
			qLike = QuestionLike.objects.get(compose_key=compose_key)
		except QuestionLike.DoesNotExist:
			qLike = QuestionLike.objects.create(compose_key=compose_key)
		if qLike.value == 0:
			qLike.value = 1
			question.rating = question.rating + 1
			question.user.profile.rating = question.user.profile.rating + 1
			qLike.is_liked = True
		elif qLike.value == -1:
			qLike.value = 1
			question.rating = question.rating + 2
			question.user.profile.rating = question.user.profile.rating + 2
			qLike.is_liked = True
		elif qLike.value == 1:
			qLike.value = 0
			question.rating = question.rating - 1
			question.user.profile.rating = question.user.profile.rating - 1
			qLike.is_liked = False
		question.save()
		question.user.profile.save()
		qLike.save()

	def dislike(self, id, user):
		compose_key = str(user) + str(id)
		question = Question.objects.get(pk=id)
		try:
			qLike = QuestionLike.objects.get(compose_key=compose_key)
		except QuestionLike.DoesNotExist:
			qLike = QuestionLike.objects.create(compose_key=compose_key)

		if qLike.value == 0:
			qLike.value = -1
			question.rating = question.rating - 1
			question.user.profile.rating = question.user.profile.rating - 1
			qLike.is_disliked = True
		elif qLike.value == 1:
			qLike.value = -1
			question.rating = question.rating - 2
			question.user.profile.rating = question.user.profile.rating - 2
			qLike.is_disliked = True
		elif qLike.value == -1:
			qLike.value = 0
			question.rating = question.rating + 1
			question.user.profile.rating = question.user.profile.rating + 1
			qLike.is_disliked = False
		question.save()
		question.user.profile.save()
		qLike.save()




class QuestionLike(models.Model):

	value = models.IntegerField(default=0)
	#question = models.ForeignKey(Question)
	#user = models.OneToOneField(User)
	compose_key = models.CharField(max_length=70, unique=True, default='None0')
	is_liked = models.BooleanField(default=False)
	is_disliked = models.BooleanField(default=False)

	objects = QuestionLikeManager()
	def __unicode__(self):
		return str(self.value)




