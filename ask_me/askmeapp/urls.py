from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<page>\d+)/', views.index, name='index'),
	url(r'^hot/(?P<page>\d+)/', views.hot_questions, name='hot_questions'),
	url(r'^hot/', views.hot_questions, name='hot_questions'),

	url(r'^question/id\d+/(?P<page>\d+)?/$', views.single_question, name='question'),
	url(r'^question/id\d+/$', views.single_question, name='question'),

	url(r'^ask/', views.ask_question, name='ask'),
	url(r'^developing/', views.developing, name='developing'),
	url(r'^login/', views.login, name='login'),
	url(r'^signup/', views.signup, name='signup'),

	url(r'^tag/(?P<tag>\w+)/$', views.tag, name='tag'),
	url(r'^tag/(?P<tag>\w+)/(?P<page>\d+)/$', views.tag, name='tag'),

	url(r'^profile/\w+/(?P<page>\d+)?/$', views.profile, name='profile'),
	url(r'^profile/\w+/$', views.profile, name='profile'),

	url(r'get_post_params/', views.get_post_params, name='get_post_params'),
]

