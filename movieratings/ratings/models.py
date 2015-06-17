from django.db import models
from django.db.models import Avg, Count
from math import sqrt
from django.contrib.auth.models import User
import numpy as np
from math import sqrt


class Rater(models.Model):
    age = models.IntegerField('age', default=0)
    zip_code = models.CharField('zipcode', max_length=40)
    user = models.OneToOneField(User, null=True)
    description = models.CharField(max_length=511)

    def top_unseen(self, idx=5):
        """
        Highest rated movies
        not rated by this user
        """
        queryset = self.rating_set.values('movie')
        result = Movie.objects.filter(~models.Q(id__in=queryset))

        if idx >= result.count():
            return result

        return result[:idx]

    def average_rating(self):
        """
        The average rating given
        by this user
        """
        return round(Rating.objects.filter(rater= \
                            self.id).aggregate(Avg('rating'))['rating__avg'], 1)

    def top_seen(self, idx=20):
        """
        returns top 20 ratings by this user
        """
        queryset = self.rating_set.all()
        if queryset.exists():
            if idx > queryset.count():
                idx = queryset.count()

            return sorted(queryset, key=lambda x: x.rating, reverse=True)[:idx]
        return None

    def distance(self, ours, theirs):
        """
        The euclidean distance
        between this user and other
        """
        return sqrt(sum((ours[idx].rating - theirs[idx].rating)**2 for idx in range(ours.count())))

    def most_similar(self, idx=5):
        """
        returns users with smallest (nonzero) distance
        to user
        """
        ours = self.rating_set.all().select_related('movie')
        ids = [item.movie_id for item in ours]

        return sorted((item for item in Rater.objects.exclude(id=self.id).prefetch_related('rating_set').filter(rating__movie_id__in=ids)),\
                      key=lambda x: self.distance(ours, x.rating_set.all().order_by('movie_id')))[:idx]

        # pull in rating objects instead, select related user?

    def suggestions(self):
        users = self.most_similar()
        suggest = []
        for user in users:
            suggest.extend(sorted(user.rating_set.all(), \
                           key=lambda x: x.rating, reverse=True)[:2])

        return suggest

    def add_rating(self, movie, rating, timestamp):
        """
        creates a new rating for this user
        """
        Rating.objects.create(rater=self, movie=movie, rating=rating, \
                              timestamp=timestamp)

    def __str__(self):
        return str(self.id)


class Movie(models.Model):
    title = models.CharField(max_length=255, default='')

    def get_ratings(self):
        """
        returns tuples of rater_id, rating
        for this movie
        """
        return map(lambda x: (x.rater, x.rating), \
                   self.rating_set.all().order_by('-rating'))

    def average_rating(self):
        """
        returns the average rating
        for this movie
        """
        ratings = Rating.objects.filter(movie= \
                            self.id).aggregate(Avg('rating'))['rating__avg']
        if ratings:
            return ratings
        return 0

    @classmethod
    def top_movies(cls, idx=6, rates=10):
        """
        returns the top 'idx' movies
        by rating
        """
        queryset = Movie.objects.annotate(rating_count=\
                    Count('rating'), rating_avg=Avg('rating__rating'\
                    )).filter(rating_count__gt=rates).order_by('-rating_avg'\
                    )[:idx]

        return queryset


        return ['No movies found!']

    def __str__(self):
        return str(self.title)


class Rating(models.Model):
    movie = models.ForeignKey('Movie')
    rater = models.ForeignKey('Rater')
    rating = models.IntegerField()
    description = models.CharField(max_length=511, default=' ')
    timestamp = models.DateTimeField(null=True)

    def __str__(self):
        return "{}: {}".format(str(self.movie), self.rating)

    class Meta:
        unique_together = ('movie', 'rater',)


def create_users_for_ratings():
    for item in Rater.objects.all():
        item.user = User.objects.get(id=User.objects.create(username=item.id, \
                     email='{}@ex.org'.format(item.id), password=item.id).id)

        item.save()


class Genre(models.Model):
    name = models.CharField(max_length=40)
    movies = models.ManyToManyField('Movie')

    def __str__(self):
        return self.name
