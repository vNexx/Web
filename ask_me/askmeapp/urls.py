from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^question/', views.single_question, name='question'),
	url(r'^ask/', views.ask_question, name='ask'),
	url(r'^login/', views.login, name='login'),
]

