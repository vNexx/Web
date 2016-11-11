from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^hot/', views.hot_questions, name='hot_questions'),
	url(r'^question/', views.single_question, name='question'),
	url(r'^ask/', views.ask_question, name='ask'),
	url(r'^developing/', views.developing, name='developing'),
	url(r'^login/', views.login, name='login'),
	url(r'^signup/', views.signup, name='signup'),
	url(r'^tag/(?P<tag>\w+)/?$', views.tag, name='tag'),
	url(r'^profile/', views.profile, name='profile'),
]

