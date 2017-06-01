from django.conf.urls import url

from . import views

app_name = 'quiz'
urlpatterns = [

    url(r'^answer$', views.handle_user_answer, name='handle_answer'),
    url(r'^question$', views.render_next_question, name='next_question'),
    url(r'^$', views.start, name='start'),

]