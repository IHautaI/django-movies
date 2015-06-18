from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
import datetime
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django import forms
from django.core.urlresolvers import reverse

#from movieratings.forms import RatingForm, NewRatingForm, RaterDescrForm
from movieratings.forms import NewRatingForm, RaterDescrForm
from .models import Movie, Rater, Rating, Genre


def index(request):
    return render(request, 'index.html')

class MovieListView(ListView):
    model = Movie
    template_name = 'ratings/movies.html'
    paginate_by = 20
    queryset = list(Movie.top_movies(Movie.objects.count()))

    # def get_queryset(self):
    #     return list(Movie.top_movies(Movie.objects.count()))


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'ratings/movie.html'

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            rater = Rater.objects.filter(user=self.request.user)
            if rater.exists():
                rating = Rating.objects.filter(movie=self.object, \
                                               rater=rater)
            else:
                rating = Rating.objects.none()

            if rating.exists():
                rating = rating[0]
                rated = True
            else:
                rated = False

            context['rated'] = rated
            context['rating'] = rating
            context['avg'] = round(self.object.average_rating(), 1)

        context['ratings'] = self.object.rating_set.select_related('rater').order_by('-rating')

        return context


def rater_detail(request, rater_id=None):
    theirs = False

    if rater_id is not None and request.user.is_authenticated():
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
               'form': form}#, 'most_similar':rater.most_similar()}
               #'suggested':rater.suggestions()} these are still waaaay too slow
    return render(request, 'ratings/rater.html', context)



class RatingEditView(UpdateView):
    model = Rating
    template_name_suffix = '_update'
    fields = ['rating', 'description']
    RATING_CHOICES = ((1,  '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))
    widgets = {'rating':forms.ChoiceField(choices=RATING_CHOICES)}
    success_url = '/ratings/rater/'

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
def new_rating(request, user_id, movie_pk):

    rater = get_object_or_404(Rater, user_id=request.user.id)
    movie = get_object_or_404(Movie, id=movie_pk)

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
    return render(request, 'ratings/rating_form.html', context)

    def get_queryset(self):

        return Rating.objects.filter(rater=self.request.user.rater, pk=movie_pk)

    RATING_CHOICES = ((1,  '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))
    widgets = {'rating':forms.ChoiceField(choices=RATING_CHOICES)}
    success_url = 'ratings/rater/'



class MostRatedListView(ListView):
    model = Movie
    template_name = 'ratings/most_rated.html'

    def get_queryset(self):
        return Movie.objects.annotate(rates=Count('rating')).order_by('-rates')[:20]


def genre_view(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    movies = genre.movies.all()

    context = {'genre':genre, 'movies':movies}
    return render(request, 'ratings/genre.html', context)
