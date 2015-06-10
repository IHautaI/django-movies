from django.contrib import admin
from .models import Rater, Movie, Rating
# Register your models here.
class RaterAdmin(admin.ModelAdmin):

    readonly_fields = ('id', 'average_rating')

    fieldsets = [(None, {'fields': ['id', 'average_rating']})]


class MovieAdmin(admin.ModelAdmin):

    readonly_fields = ('get_ratings', 'average_rating',)

    fieldsets = [(None, {'fields': ['id', 'title', 'get_ratings',
                                    'average_rating']})]

class RatingAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['rater', 'movie', 'rating']})]



admin.site.register(Rater, RaterAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating, RatingAdmin)
