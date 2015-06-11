from django.db import models
from django.db.models import Avg
from math import sqrt


class Rater(models.Model):
    age = models.IntegerField('age', default=0)
    zip_code = models.CharField('zipcode', max_length=40)

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
        return Rating.objects.filter(rater= \
                            self.id).aggregate(Avg('rating'))['rating__avg']

    def top_seen(self, idx=20):
        """
        returns top 20 ratings by this user
        """
        queryset = self.rating_set.select_related('movie')
        if queryset.exists():
            if idx > queryset.count():
                idx = queryset.count()

            return map(lambda x: (x.rating, x.movie), sorted(queryset, \
                       key=lambda x: x.rating)[:idx])
        return None

    def distance(self, other):
        """
        The euclidean distance
        between this user and other
        """
        ours = self.rating_set.all()
        theirs = other.rating_set.all()
        dist = []
        for item in ours:
            if theirs.filter(movie=item.movie).exists():
                dist.append(item.rating - theirs.get(movie=item.movie).rating)

        if dist:
            return sqrt(sum(map(lambda x: x**2, dist)))
        else:
            return 0

    def most_similar(self, idx=5):
        """
        returns a list of the 'idx' most
        similar users by euclidean distance
        """
        raters = Rater.objects.exclude(pk=self.id)
        if raters.exists():
            if idx > raters.count():
                idx = raters.count()

            raters = filter(lambda x: x[1], map(lambda x: \
                            (x, self.distance(x)), raters))

            raters = sorted(raters, key=lambda x: x[1])[:idx]

            return [rater[0] for rater in raters]

        return None

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
    #genre = models.ManyToManyField('Genre')

    def get_ratings(self):
        """
        returns tuples of rater_id, rating
        for this movie
        """
        return map(lambda x: (x.rater.id, x.rating), self.rating_set.all())

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
        queryset = Movie.objects.all()
        queryset = list(filter(lambda x: len(x.rating_set.all()) > rates, queryset))
        if queryset:
            if len(queryset) < idx:
                return sorted(queryset, key=lambda x: x.average_rating(), \
                              reverse=True)

            return sorted(queryset, key=lambda x: x.average_rating(), \
                          reverse=True)[:idx]

        return ['No movies found!']

    def __str__(self):
        return str(self.title)


class Rating(models.Model):
    movie = models.ForeignKey('Movie')
    rater = models.ForeignKey('Rater')
    rating = models.FloatField()
    #timestamp = models.DateField()

    def __str__(self):
        return "{}: {}".format(str(self.movie), self.rating)

    class Meta:
        unique_together = ('movie', 'rater',)

"""
class Genre(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
"""
