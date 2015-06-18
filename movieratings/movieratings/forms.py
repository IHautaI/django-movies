from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from ratings.models import Rating, Movie, Rater

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


# class RatingForm(forms.ModelForm):
#     RATING_CHOICES = ((1,  '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))
#     rating = forms.TypedChoiceField(widget=forms.Select(), \
#                    choices=RATING_CHOICES, coerce=int, empty_value=None)
#
#     description = forms.CharField(required=False)
#
#     class Meta:
#         model = Rating
#         fields = ('rating', 'description',)


def in_set(item):
    #if int(item) not in range(1, 6):
    #    raise ValidationError('Input value was not a valid choice')
    pass


class NewRatingForm(forms.ModelForm):
    RATING_CHOICES = ((1,  '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))

    rating = forms.ChoiceField(widget=forms.Select(), \
                                    choices=RATING_CHOICES)#, \
                                    #empty_value=None, \
                                    #validators=[in_set])
    description = forms.CharField(required=False)

    class Meta:
        model = Rating
        fields = ('rating', 'description',)


class RaterDescrForm(forms.ModelForm):
    description = forms.CharField()

    class Meta:
        model = Rater
        fields = ('description',)
