from django.urls import path

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('create-poll', views.create_poll, name='create-poll'),
    path('commit-create-poll', views.commit_create_poll, name='commit-create-poll'),
    path('new-user', views.new_user, name='new-user'),
    path('create-user', views.create_user, name='create-user'),
    #path('user-page', views.user_page, name='user-page'),
    path('<int:user_id>/user-page', views.user_page, name='user-page'),
    path('log-in', views.log_in, name='log-in'),
    path('commit-login', views.commit_login, name='commit-login'),
    path('log-out', views.log_out, name='log-out'),
]