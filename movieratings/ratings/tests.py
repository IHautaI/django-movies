from django.test import TestCase
from ratings.models import Movie, Rating, Rater, Genre
from math import sqrt


class MovieTestCase(TestCase):
    def setUp(self):
        a = Genre.objects.create(name='western')
        b = Genre.objects.create(name='scifi')

        das = Movie.objects.create(mid=1, title='Das Fahrrad')
        ell = Movie.objects.create(mid=2, title='Elliot\'s Run')
        goob = Movie.objects.create(mid=3, title='The Goobers')
        nurb = Movie.objects.create(mid=4, \
                                    title='Non-uniform Rational B-Splines')

        a.movie_set.add(das)
        b.movie_set.add(ell)
        b.movie_set.add(goob)
        a.movie_set.add(nurb)

        us1 = Rater.objects.create(uid=1)
        us2 = Rater.objects.create(uid=2)

        Rating.objects.create(movie=das, rater=us1, rating=5,
                              timestamp='2014-01-01')

        Rating.objects.create(movie=das, rater=us2, rating=2,
                              timestamp='2014-01-01')

        Rating.objects.create(movie=ell, rater=us1, rating=3,
                              timestamp='2014-01-01')

        Rating.objects.create(movie=ell, rater=us2, rating=4,
                              timestamp='2014-01-01')

        Rating.objects.create(movie=goob, rater=us1, rating=5,
                              timestamp='2014-01-01')

        Rating.objects.create(movie=nurb, rater=us1, rating=4,
                              timestamp='2014-04-04')

    def test_movie_rating(self):
        das = Movie.objects.get(title='Das Fahrrad')
        self.assertEqual(sorted(das.get_ratings()), sorted([5, 2]))

    def test_movie_average_rating(self):
        das = Movie.objects.get(title='Das Fahrrad')
        self.assertEqual(das.average_rating(), 7/2)

    def test_top_movies(self):
        das = Movie.objects.get(title='Das Fahrrad')
        ell = Movie.objects.get(title='Elliot\'s Run')
        goob = Movie.objects.get(title='The Goobers')
        nurb = Movie.objects.get(title='Non-uniform Rational B-Splines')

        self.assertEquals(Movie.top_movies(1), [das])
        self.assertEquals(Movie.top_movies(2), [das, ell])
        self.assertEquals(Movie.top_movies(), [das, ell, nurb, goob])

    def test_rater_ratings(self):
        rater = Rater.objects.get(uid=2)

        self.assertEquals(rater.ratings(), \
            "Das Fahrrad: 2.0, Elliot\'s Run: 4.0")

    def test_rater_average_rating(self):
        rater = Rater.objects.get(uid=2)

        self.assertEquals(rater.average_rating(), 3)

    def test_seen(self):
        rater = Rater.objects.get(uid=1)
        das = Movie.objects.get(title='Das Fahrrad')
        ell = Movie.objects.get(title='Elliot\'s Run')
        goob = Movie.objects.get(title='The Goobers')
        nurb = Movie.objects.get(title='Non-uniform Rational B-Splines')

        self.assertEquals(rater.seen(), {das:5.0, ell:3.0, goob:5.0, nurb:4})

    def test_top_unseen(self):
        rater = Rater.objects.get(uid=2)
        goob = Movie.objects.get(title='The Goobers')
        nurb = Movie.objects.get(title='Non-uniform Rational B-Splines')

        self.assertEquals(rater.top_unseen(), [nurb, goob])

    def test_distance(self):
        us1 = Rater.objects.get(uid=1)
        us2 = Rater.objects.get(uid=2)

        self.assertEquals(us1.distance(us2), sqrt(10))
