from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='ratings-index'),
    url(r'^movie/$', views.movie_index, name='movie-top'),
    url(r'^movie/(?P<movie_id>[0-9]+)/$',
        views.movie_detail, name='movie-detail'),
    url(r'^rater/$', views.rater_detail,
        name='rater-detail'),
]
