from django.shortcuts import render, get_object_or_404

from .models import Movie, Rater
# Create your views here.

def index(request):
    return render(request, 'ratings/index.html')

def movie_index(request):
    top_movie_list = Movie.top_movies(20)
    context = {'top_movie_list': top_movie_list}
    return render(request, 'ratings/movies.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'ratings/movie.html', {'movie':movie,
                                    'avg':round(movie.average_rating(), 1),
                                    'ratings':movie.get_ratings()})

def rater_detail(request, rater_id):
    rater = get_object_or_404(Rater, pk=rater_id)
    return render(request, 'ratings/rater.html', {'rater':rater,
                  'ratings':rater.top_seen(), 'avg':rater.average_rating(),
                  'most_similar':rater.most_similar(),
                  'suggested':rater.suggestions()})
