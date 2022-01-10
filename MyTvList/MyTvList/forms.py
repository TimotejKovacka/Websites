from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from MyTvList.models import User, UserProfile
from MyTvList.models import Review
from django.db import models
from django.contrib.auth.forms import AuthenticationForm, UsernameField
import tmdbSimpleApi


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    picture = forms.ImageField(required = False)
    favourite_show = forms.CharField(max_length=150)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'picture', 'favourite_show' ]

    def save(self, commit = True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data.get("email")
        user.picture = self.cleaned_data.get("picture")
        user.favourite_show = self.cleaned_data.get("favourite_show")
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        favourite_show = cleaned_data.get("favourite_show")
        favouriteShow = tmdbSimpleApi.getId(favourite_show)
        if favouriteShow == None:
            self.add_error('favourite_show', 'Can not find show')
        return cleaned_data

class SearchForm(forms.Form):
    search_input = forms.CharField()

class ReviewForm(forms.ModelForm):
    review = forms.CharField(max_length = 496)
    rating = forms.DecimalField(max_value = 10, min_value = 1, max_digits = 3, decimal_places = 1)
    class Meta:
        model = Review
        fields = ('rating', 'review',)

    def clean(self):
        cleaned_data = super(ReviewForm, self).clean()
        rating = cleaned_data.get("rating")
        return cleaned_data
