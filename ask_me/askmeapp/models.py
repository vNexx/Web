# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from django.contrib.auth.models. import User

from django.db import models

# Create your models here.


class ArticleManager(models.Manager):
	def published(self):
		return self.filter(is_published=True)


class Article(models.Model):
	title = models.CharField(max_length=255, verbose_name=u'заголовок')
	text = models.TextField(verbose_name=u'Текст')
	is_published = models.BooleanField(default = False, verbose_name=u'Опубликована')
	author = models.ForeignKey('Author')
	objects = ArticleManager()
	#author = models.ForeignKey('User')
	
	class Meta:
		verbose_name = u'Статья'
		verbose_name_plural = u'Статьи'
	def __unicode__(self):
		return self.title


class Author(models.Model):
	name = models.CharField(max_length=255, verbose_name=u'имя')
	birthday = models.DateField(null=False, blank=False, verbose_name=u'Data rozhdeniya')
	
	class Meta:
		verbose_name = u'Автор'
		verbose_name_plural = u'Авторы'
	def __unicode__(self):
		return u"{} {}".format(self.name, self.birthday)



