from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='ratings-index'),
    url(r'^movie/$', views.MovieListView.as_view(), name='movie-top'),
    url(r'^movie/(?P<pk>[0-9]+)/$', \
        views.MovieDetailView.as_view(), name='movie-detail'),
    url(r'^most-rated/', views.MostRatedListView.as_view(), name='most-rated'),

    url(r'^genre/(?P<genre_id>[0-9]+)/$', views.genre_view, name='by-genre'),

    url(r'^rater/(?P<rater_id>[0-9]+)/$', views.rater_detail, name='rater-detail'),
    url(r'^rater/$', views.rater_detail, name='rater-detail'),

    url(r'^rate/(?P<user_id>[0-9]+)/(?P<pk>[0-9]+)/$', views.new_rating, name='rate'),
    url(r'^edit/(?P<rater_id>[0-9]+)/(?P<pk>[0-9]+)/$', views.edit, name='edit'),

    url(r'^search/$', views.search, name='search'),
    url(r'^search-error/', views.search_error, name='search-error'),
]
