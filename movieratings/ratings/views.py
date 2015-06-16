from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
import datetime
from django.contrib import messages

from movieratings.forms import RatingForm, NewRatingForm, RaterDescrForm
from .models import Movie, Rater, Rating, Genre


def index(request):
    return render(request, 'index.html')


def movie_index(request):
    top_movie_list = Movie.top_movies(20)

    context = {'top_movie_list': top_movie_list}
    return render(request, 'ratings/movies.html', context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    rated = False
    rating = None
    descr = ''
    if request.user.is_authenticated():
        rating = Rating.objects.filter(movie=movie, rater=request.user.rater)
        if rating.exists():
            rating = rating[0]
            rated = True
            messages.add_message(request, messages.SUCCESS, str(rating))


    ratings = Rating.objects.filter(movie_id=movie.id).select_related('rater')

    context= {'movie': movie, 'avg': round(movie.average_rating(), 1),
              'rated': rated, 'rating': rating, 'ratings': ratings}

    return render(request, 'ratings/movie.html', context)


def rater_detail(request, rater_id=None):
    theirs = False

    if rater_id is not None:
        if int(request.user.rater.id) == int(rater_id):
            theirs = True

    else:
        if request.user.is_authenticated():
            rater_id = request.user.rater.id
            theirs = True


    rater = get_object_or_404(Rater, id=rater_id)

    if request.method == 'POST':
        form = RaterDescrForm(request.POST)

        if form.is_valid():
            rater.description = form.description
            rater.save()

            return redirect('ratings:rater-detail')

    form = RaterDescrForm(instance=rater)
    ratings = rater.rating_set.order_by('-rating').select_related('movie')

    context = {'rater':rater, 'email':rater.user.email, \
               'ratings':ratings, \
               'avg':rater.average_rating(), 'theirs': theirs,
               'form': form}
               #'most_similar':rater.most_similar(),
               #'suggested':rater.suggestions()}
    return render(request, 'ratings/rater.html', context)


@login_required
def edit(request, rater_id, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    rater = get_object_or_404(Rater, id=rater_id)

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)

        if rating_form.is_valid():
            rating = get_object_or_404(Rating, movie=movie, rater=rater)
            rating.timestamp = datetime.datetime.now()
            form = rating_form.save(commit=False)
            rating.description = form.description
            rating.save()

            return redirect('ratings:rater-detail')


    else:
        rating_form = RatingForm()

    rating = get_object_or_404(Rating, movie=movie, rater=rater)

    context =  {'rating_form': rating_form, 'rating': rating, \
                'rater_id':rater_id, 'movie_id': movie.id, 'movie': movie}
    return render(request, 'ratings/edit.html', context)


@login_required
def search(request):

    if request.method == 'GET':
        if 'movie_name' in request.GET:
            name = request.GET['movie_name']
            queryset = Movie.objects.filter(title__icontains=name)

            if not queryset.exists():
                return redirect('ratings:search-error')

            context = {'movie_name': name, 'movies':queryset}
            return render(request, 'ratings/search.html', context)

    return render(request, 'ratings/search-error.html')

def search_error(request):
    return render(request, 'ratings/search-error.html')

@login_required
def new_rating(request, user_id, movie_id):
    rater = get_object_or_404(Rater, user_id=request.user.id)
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        form = NewRatingForm(request.POST)

        if form.is_valid():
            rating = form.save(commit=False)
            rating.movie = movie
            rating.rater = rater
            rating.timestamp = datetime.datetime.now()

            rating.save()
            messages.add_message(request, messages.SUCCESS, \
                                 'New Rating Successfully Added!')

        else:
            messages.add_message(request, messages.ERROR, \
                                  'New Rating Not Created')


        return redirect('ratings:rater-detail')

    else:
        form = NewRatingForm()

    rater = get_object_or_404(Rater, user_id=request.user.id)

    context = {'form': form, 'user_id': user_id, 'movie': movie}
    return render(request, 'ratings/new.html', context)


def most_rated(request):
    most_rated = Movie.objects.annotate(rates=Count('rating')).order_by('-rates')[:20]

    context = {'most_rated': most_rated}
    return render(request, 'ratings/most_rated.html', context)


def by_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    movies = genre.movies.all()

    context = {'genre':genre, 'movies':movies}
    return render(request, 'ratings/genre.html', context)
