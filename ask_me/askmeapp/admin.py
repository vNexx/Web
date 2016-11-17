from django.contrib import admin
from askmeapp import models

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
	list_display=('title',)

class AnswerAdmin(admin.ModelAdmin):
	list_display=('text',)
class TagAdmin(admin.ModelAdmin):
	list_display=('text',)
class LikeAdmin(admin.ModelAdmin):
	list_display=('rating',)
class ProfileAdmin(admin.ModelAdmin):
	list_display=('user',)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Like, LikeAdmin)
admin.site.register(models.Profile, ProfileAdmin)
