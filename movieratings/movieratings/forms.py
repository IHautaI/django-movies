from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from ratings.models import Rating, Movie, Rater

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class RatingForm(forms.ModelForm):
    RATING_CHOICES = ((1,  '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))
    rating = forms.TypedChoiceField(widget=forms.Select(), \
                   choices=RATING_CHOICES, coerce=int, empty_value=None)
                   
    descr = forms.CharField()

    class Meta:
        model = Rating
        fields = ('rating', 'descr',)


def in_set(item):
    if not isinstance(item, int):
        raise ValidationError('Input value was not a valid choice')

    if item not in range(1, 6):
        raise ValidationError('Input value was not a valid choice')


class NewRatingForm(forms.ModelForm):

    movie = forms.ModelChoiceField(queryset=None, empty_label=None, validators=[in_set])

    def __init__(self, choices, *args, **kwargs):
        super(NewRatingForm, self).__init__(*args, **kwargs)
        self.fields['movie'].queryset = choices

    RATING_CHOICES = ((1,  '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))
    rating = forms.TypedChoiceField(widget=forms.Select(), choices=RATING_CHOICES, coerce=int, empty_value=None)
    descr = forms.CharField()

    class Meta:
        model = Rating
        fields = ('rating', 'movie')


class RaterDescrForm(forms.ModelForm):
    descr = forms.CharField()

    class Meta:
        model = Rater
        fields = ('descr',)
