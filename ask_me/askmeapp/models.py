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

	def get_popular_tags(self):
		return self.order_by_question_count().all()[:10]

class Tag(models.Model):
	text = models.CharField(max_length=50, verbose_name='Tag')
	style_number = models.IntegerField(default=1)
	objects = TagManager()
	def __unicode__(self):
		return self.text

class Category(models.Model):
	title = models.CharField(max_length = 50, verbose_name=u'Категория', default="General")

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
	#id = models.IntegerField(unique=True, primary_key=True)
	category = models.ForeignKey(Category)
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
	rating = models.IntegerField()

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
	#id = models.IntegerField(primary_key=True)


class Like(models.Model):
	status = models.IntegerField(default=0)
	#question = models.ForeignKey(Question)


	def __unicode__(self):
		return str(self.rating)

# class ArticleManager(models.Manager):
# 	def published(self):
# 		return self.filter(is_published=True)
#
#
# class Article(models.Model):
# 	title = models.CharField(max_length=255, verbose_name=u'заголовок')
# 	text = models.TextField(verbose_name=u'Текст')
# 	is_published = models.BooleanField(default = False, verbose_name=u'Опубликована')
# 	author = models.ForeignKey('Author')
# 	objects = ArticleManager()
#
# 	#author = models.ForeignKey('User')
#
# 	class Meta:
# 		verbose_name = u'Статья'
# 		verbose_name_plural = u'Статьи'
# 	def __unicode__(self):
# 		return self.title
#
#
# class Author(models.Model):
# 	name = models.CharField(max_length=255, verbose_name=u'имя')
# 	birthday = models.DateField(null=False, blank=False, verbose_name=u'Data rozhdeniya')
#
# 	class Meta:
# 		verbose_name = u'Автор'
# 		verbose_name_plural = u'Авторы'
# 	def __unicode__(self):
# 		return u"{} {}".format(self.name, self.birthday)


