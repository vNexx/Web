# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager
import datetime
# Create your models here.

class QuestionManager(models.Manager):
	def newest(self):
		return self.order_by('-created')

	def hot(self):
		return self.order_by('-rating')

	def tag_search(self, input_tag):
		return self.filter(tag__text = input_tag)

	def published(self):
		return self.filter(is_published=True)
	def user_questions(self, user_name):
		return self.filter(user__username = user_name)

class ProfileManager(models.Manager):
	def get(self, user_name):
		return self.filter(user__username = user_name)

class Tag(models.Model):
	text = models.CharField(max_length=50, verbose_name='Tag')

	def __unicode__(self):
		return self.text


class Like(models.Model):
	rating = models.IntegerField(default = 0, db_index=True)

	def __unicode__(self):
		return str(self.rating)


class Question(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length = 255, verbose_name=u'Заголовок')
	text = models.TextField(verbose_name=u'Текст')
	rating = models.IntegerField(verbose_name=u'Рэйтинг')
	is_published = models.BooleanField(default=False, verbose_name=u'Опубликована')
	created = models.DateTimeField(default = datetime.datetime.now)
	tag = models.ManyToManyField(Tag)
	id = models.IntegerField(unique=True, primary_key=True)

	objects = QuestionManager()

	def __unicode__(self):
		return self.title



	def __unicode__(self):
		return self.text

class Profile(models.Model):
	user = models.OneToOneField(User)
	avatar = models.ImageField(upload_to='uploads', default="uploads/user_avatar.jpeg")
	information = models.TextField()
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
	id = models.IntegerField(primary_key=True)


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


