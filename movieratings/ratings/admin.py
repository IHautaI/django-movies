from django.contrib import admin
from .models import Rater, Movie, Rating
# Register your models here.
class RaterAdmin(admin.ModelAdmin):

    readonly_fields = ('uid', 'ratings', 'average_rating')

    fieldsets = [(None, {'fields': ['uid', 'ratings', 'average_rating']})]


class MovieAdmin(admin.ModelAdmin):

    readonly_fields = ('get_ratings', 'genre', 'average_rating',)

    fieldsets = [(None, {'fields': ['mid', 'title', 'get_ratings',
                                    'average_rating', 'genre']})]

class RatingAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['rater', 'movie', 'rating', 'timestamp']})]

admin.site.register(Rater, RaterAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating, RatingAdmin)
