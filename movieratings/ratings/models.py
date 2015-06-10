from django.db import models
from django.db.models import Avg
from math import sqrt


class Rater(models.Model):
    uid = models.IntegerField('User ID')

    def ratings(self):
        return ", ".join(map(str, self.rating_set.all()))

    def top_unseen(self, idx=5):
        queryset = map(lambda x: x.movie.id, self.rating_set.all())

        result = sorted(Movie.objects.all().exclude(id__in=queryset), \
                      key=lambda x: x.average_rating())

        if idx >= len(result):
            return result

        return result[:idx]

    def average_rating(self):
        return Rating.objects.all().filter(rater= \
                            self.id).aggregate(Avg('rating'))['rating__avg']

    def seen(self):
        return {item.movie: item.rating for item in self.rating_set.all()}

    def distance(self, other):
        ours = self.seen()
        theirs = other.seen()
        dist = [ours[item] - theirs[item] for item in ours if item in theirs]
        if dist:
            return sqrt(sum(map(lambda x: x**2, dist)))
        else:
            return 0


    def __str__(self):
        return str(self.uid)


class Movie(models.Model):
    mid = models.IntegerField()
    title = models.CharField(max_length=40, default='')
    genre = models.ManyToManyField('Genre')

    def get_ratings(self):
        return map(lambda x: x.rating, self.rating_set.all())

    def average_rating(self):
        return Rating.objects.all().filter(movie= \
                            self.id).aggregate(Avg('rating'))['rating__avg']

    @classmethod
    def top_movies(cls, idx=6):
        queryset = Movie.objects.all()

        if len(queryset) < idx:
            return sorted(queryset, key=lambda x: x.average_rating())

        return sorted(queryset, key=lambda x: x.average_rating())[:idx]

    def __str__(self):
        return str(self.title)


class Rating(models.Model):
    movie = models.ForeignKey('Movie')
    rater = models.ForeignKey('Rater')
    rating = models.FloatField()
    timestamp = models.DateField()

    def __str__(self):
        return "{}: {}".format(str(self.movie), self.rating)


class Genre(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
