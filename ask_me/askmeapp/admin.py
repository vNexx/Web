from django.contrib import admin
from askmeapp import models

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
	list_display=('title',)

class AuthorAdmin(admin.ModelAdmin):
	list_display=('name',)

admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Article, ArticleAdmin)
