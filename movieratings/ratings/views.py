from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from movieratings.forms import RatingForm, NewRatingForm
from .models import Movie, Rater, Rating


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


    return render(request, 'ratings/movie.html', {'movie':movie,
                                    'avg':round(movie.average_rating(), 1),
                                    'ratings':movie.get_ratings(), 'rate':rate})

@login_required
def rater_detail(request):
    rater = get_object_or_404(Rater, user_id=request.user.id)
    return render(request, 'ratings/rater.html', {'rater':rater, \
                  'email':request.user.email, 'ratings':rater.top_seen(), \
                  'avg':rater.average_rating()})#,
                  #'most_similar':rater.most_similar(),
                  #'suggested':rater.suggestions()})

@login_required
def edit(request, user_id, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    rater = get_object_or_404(Rater, user_id=request.user.id)


    if request.method == 'POST':
        form = RatingForm(request.POST)

        if form.is_valid():
            rating = get_object_or_404(Rating, movie=movie, rater=rater)
            rating.rating = form.save(commit=False).rating
            rating.movie = movie
            rating.rater = rater
            rating.save()

            return redirect('ratings:rater-detail')


    else:
        form = RatingForm()

    rating = get_object_or_404(Rating, movie=movie, rater=rater)

    return render(request, 'ratings/edit.html', \
                  {'form': form, 'rating': rating, 'user_id': user_id,\
                  'movie_id': movie.id, 'movie': movie})


@login_required
def new_rating(request, user_id):
    rater = get_object_or_404(Rater, user_id=request.user.id)
    if request.method == 'GET':
        name = request.GET['movie_name']
        ids = [item['movie_id'] for item in rater.rating_set.values('movie_id')]
        queryset = Movie.objects.filter(title__icontains=name).exclude(id__in=ids)

        if name == '' or queryset.count() > 100:
            return redirect('ratings:rater-detail')


    if request.method == 'POST':
        form = NewRatingForm(request.POST)

        if form.is_valid():
            movie = get_object_or_404(Movie, title=form.title)
            rating = Rating.objects.create(movie=movie, rater=rater, rating=form.rating)
            rating.save()

        return redirect('ratings:rater-detail')

    else:
        form = NewRatingForm(queryset)

    rater = get_object_or_404(Rater, user_id=request.user.id)

    return render(request, 'ratings/new.html', {'form': form, 'user_id': user_id})
