from django.test import TestCase
from ratings.models import Movie, Rating, Rater
from math import sqrt


class MovieTestCase(TestCase):
    def setUp(self):


        das = Movie.objects.create(title='Das Fahrrad')
        ell = Movie.objects.create(title='Elliot\'s Run')
        goob = Movie.objects.create(title='The Goobers')
        nurb = Movie.objects.create(title='Non-uniform Rational B-Splines')


        us1 = Rater.objects.create(age=5, zip_code='12345')
        us2 = Rater.objects.create(age=45, zip_code='23456')

        Rating.objects.create(movie=das, rater=us1, rating=5)

        Rating.objects.create(movie=das, rater=us2, rating=2)

        Rating.objects.create(movie=ell, rater=us1, rating=3)

        Rating.objects.create(movie=ell, rater=us2, rating=4.5)

        Rating.objects.create(movie=goob, rater=us1, rating=5)

        Rating.objects.create(movie=nurb, rater=us1, rating=4)

    def test_movie_rating(self):
        das = Movie.objects.get(title='Das Fahrrad')
        self.assertEqual(sorted(das.get_ratings()), sorted([(1, 5.0), (2, 2.0)]))

    def test_movie_average_rating(self):
        das = Movie.objects.get(title='Das Fahrrad')
        self.assertEqual(das.average_rating(), 7/2)

    def test_top_movies(self):
        das = Movie.objects.get(title='Das Fahrrad')
        ell = Movie.objects.get(title='Elliot\'s Run')
        goob = Movie.objects.get(title='The Goobers')
        nurb = Movie.objects.get(title='Non-uniform Rational B-Splines')

        self.assertEquals(Movie.top_movies(1, rates=0), [goob])
        self.assertEquals(Movie.top_movies(2, rates=0), [goob, nurb])
        self.assertEquals(Movie.top_movies(rates=0), [goob, nurb, ell, das])

    def test_rater_average_rating(self):
        rater = Rater.objects.get(id=2)

        self.assertEquals(rater.average_rating(), 3.25)

    def test_top_unseen(self):
        rater = Rater.objects.get(id=2)
        goob = Movie.objects.get(title='The Goobers')
        nurb = Movie.objects.get(title='Non-uniform Rational B-Splines')

        self.assertEquals(list(map(lambda x: x.id, rater.top_unseen())),\
                          [goob.id, nurb.id])

    def test_distance(self):
        us1 = Rater.objects.get(id=1)
        us2 = Rater.objects.get(id=2)

        self.assertEquals(us1.distance(us2), sqrt(1.5**2 + 9))
