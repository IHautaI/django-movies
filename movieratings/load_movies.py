from django.conf import settings
import pandas as pd

settings.configure(DEBUG=True, TEMPLATE_DEBUG=True)


from ratings.models import Rater, Movie, Rating, Genre



ratings = pd.read_csv('ratings.dat', sep='::', engine='python')
movies = pd.read_csv('movies.dat', sep='::', engine='python')

ratings.columns = ['uid', 'mid', 'rating', 'timestamp']
movies.columns = ['mid', 'title', 'genre']


def make_movie(mid, title, genres):
    for item in genres:
        if not Genre.objects.all().get(name=genre):
            Genre.objects.create(name=genre)

    a = Movie.objects.create(mid=mid, title=title)

    for item in genres:
        Genre.objects.get(name=item).movie_set.add(a)

def make_rater(uid):
    Rater.objects.create(uid=uid)

def make_rating(uid, mid, rating, timestamp):
    if not Rater.objects.get(uid=uid):
        make_rater(uid)

    user = Rater.objects.get(uid=uid)
    movie = Movie.objects.get(mid=mid)
    Rating.objects.create(user=user, movie=movie, rating=rating,
                          timestamp=timestamp)

for idx in movies.index:
    args = tuple(movies.xs[idx])
    make_movie(*args)
