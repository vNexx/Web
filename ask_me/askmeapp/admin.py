from django.contrib import admin
from askmeapp import models

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
	list_display=('title', 'id',)

class AnswerAdmin(admin.ModelAdmin):
	list_display=('text',)
class TagAdmin(admin.ModelAdmin):
	list_display=('text',)
class LikeAdmin(admin.ModelAdmin):
	list_display=('status',)
class ProfileAdmin(admin.ModelAdmin):
	list_display=('user',)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title',)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Like, LikeAdmin)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Category, CategoryAdmin)
