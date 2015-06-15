from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
import datetime

from movieratings.forms import RatingForm, NewRatingForm, RaterDescrForm
from .models import Movie, Rater, Rating, Genre


def index(request):
    return render(request, 'ratings/index.html')


def movie_index(request):
    top_movie_list = Movie.top_movies(20)

    context = {'top_movie_list': top_movie_list}
    return render(request, 'ratings/movies.html', context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user.is_authenticated():
        rating = Rating.objects.filter(movie=movie, rater=request.user.rater)
        if rating.exists():
            rate = rating[0].rating
        else:
            rate = 0
    else:
        rate = 0

    context= {'movie':movie, 'avg':round(movie.average_rating(), 1),
              'ratings':movie.get_ratings(), 'rate':rate,
              'genres':movie.genre_set.all()}
    return render(request, 'ratings/movie.html', context)


def rater_detail(request, user_id=None):
    if not user_id and request.user.is_authenticated():
        user_id = request.user.id
    rater = get_object_or_404(Rater, user_id=user_id)
    theirs = False

    if request.user.id == user_id:
        theirs = True

    if request.method == 'POST':
        form = RaterDescrForm(request.POST)

        if form.is_valid():
            rater.descr = form.descr
            rater.save()

            return redirect('ratings:rater-detail')

    form = RaterDescrForm(instance=rater)

    context = {'rater':rater, 'email':rater.user.email, \
               'ratings':rater.rating_set.order_by('-rating'), \
               'avg':rater.average_rating(), 'theirs': theirs,
               'form': form}
               #'most_similar':rater.most_similar(),
               #'suggested':rater.suggestions()}
    return render(request, 'ratings/rater.html', context)


@login_required
def edit(request, user_id, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    rater = get_object_or_404(Rater, user_id=request.user.id)


    if request.method == 'POST':
        rating_form = RatingForm(request.POST)

        if rating_form.is_valid():
            rating = get_object_or_404(Rating, movie=movie, rater=rater)
            rating.timestamp = datetime.now()
            rating.rating = rating_form.save(commit=False).rating
            rating.descr = rating_form.descr
            rating.movie = movie
            rating.rater = rater
            rating.save()

            return redirect('ratings:rater-detail')


    else:
        rating_form = RatingForm()

    rating = get_object_or_404(Rating, movie=movie, rater=rater)

    context =  {'rating_form': rating_form, 'rating': rating, \
                'user_id': user_id, 'movie_id': movie.id, 'movie': movie}
    return render(request, 'ratings/edit.html', context)


@login_required
def new_rating(request, user_id):
    rater = get_object_or_404(Rater, user_id=request.user.id)
    if request.method == 'GET':
        name = request.GET['movie_name']
        ids = [item['movie_id'] for item in rater.rating_set.values('movie_id')]
        queryset = Movie.objects.filter(title__icontains=name).exclude(id__in=ids)

        if name == '' or queryset.count() > 100:
            return redirect('ratings:rater-detail')

        if not queryset.exists():
            # put message here

            return redirect('ratings:rater-detail')

    if request.method == 'POST':
        form = NewRatingForm(request.POST)

        if form.is_valid():
            movie = get_object_or_404(Movie, title=form.title)
            rating = Rating.objects.create(movie=movie, rater=rater, \
                       rating=form.rating, timestamp=datetime.now(),
                       descr=form.descr)
            rating.save()

        return redirect('ratings:rater-detail')

    else:
        form = NewRatingForm(queryset)

    rater = get_object_or_404(Rater, user_id=request.user.id)

    context = {'form': form, 'user_id': user_id}
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
