from django.conf.urls import url

from . import views

app_name = 'quiz'
urlpatterns = [

    url(r'^answer$', views.handle_user_answer, name='handle_answer'),
    url(r'^question$', views.render_next_question, name='next_question'),
    url(r'^$', views.start, name='start'),
    # url(r'^(?P<pk>[0-9]+)/?$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>[0-9]+)/results/?$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    #url(r'\w?$', views.index, name='index2'),
]