from tmdbsimple.base import TMDB
from MyTvList.models import UserProfile, Review
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from MyTvList.forms import RegistrationForm, ReviewForm, SearchForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import tmdbSimpleApi
import tmdbsimple as tmdb
from django.contrib.auth.views import LoginView
from django.contrib import messages

def index(request):
    context_dict = {'form': SearchForm()}
    context_dict['popular'] = tmdbSimpleApi.getPopular(1)
    context_dict['popular']['genres'] = tmdbSimpleApi.getGenres(context_dict['popular']['id'])
    context_dict['popular']['imgFile'] = tmdbSimpleApi.img(context_dict['popular']['poster_path'])
    if request.user.is_authenticated:
        userprofile = get_object_or_404(UserProfile, user=request.user)
        context_dict['recs'] = tmdbSimpleApi.getRecommendations(userprofile.favourite_show, 6)
        for show in context_dict['recs']:
            show['imgFile'] = tmdbSimpleApi.img(show['poster_path'])
    else:
        context_dict['tops'] = tmdbSimpleApi.getPopular(7)
        context_dict['tops'] = context_dict['tops'][1:]
        for show in context_dict['tops']:
            show['genres'] = tmdbSimpleApi.getGenres(show['id'])
            show['imgFile'] = tmdbSimpleApi.img(show['poster_path'])

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print(username, password)
        user = authenticate(username=username, password=password)
        #print(user)
        if user:
            if user.is_active:
                login(request, user)
            else:
                return HttpResponse("Your MyTvList account is disabled")
    response = render(request, 'Homepage.html', context=context_dict)

    return response


@login_required
def user_logout(request):
    logout(request)
    #check for permissions on current site if it doesnt match users permissions redirect to index
    return redirect(reverse('MyTvList:index'))

def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('MyTvList:index'))
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect(reverse('MyTvList:index'))
            else:
                messages.error(request, "Error")
        form = RegistrationForm()
        return render(request, 'register.html', context = {'form': form, })

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def topshows(request):
    context_dict = {}
    context_dict['popular'] = tmdbSimpleApi.getPopular(16)
    for show in context_dict['popular']:
        show['genres'] = tmdbSimpleApi.getGenres(show['id'])
        show['imgFile'] = tmdbSimpleApi.img(show['poster_path'])

    response = render(request, 'TopShows.html', context=context_dict)

    return response

@login_required
def recommended(request):
    context_dict = {}

    userprofile = get_object_or_404(UserProfile, user=request.user)
    context_dict['recs'] = tmdbSimpleApi.getRecommendations(userprofile.favourite_show, 16)
    for pop in context_dict['recs']:
        pop['imgFile'] = tmdbSimpleApi.img(pop['poster_path'])
    response = render(request, 'Recommended.html', context=context_dict)

    return response


def castPage(request):

    #context_dict = tmdbSimpleApi.getCastMemberPage(tmdbSimpleApi.getIdPerson(castMember))
    context_dict = tmdbSimpleApi.getCastMemberPage(tmdbSimpleApi.getIdPerson("James Gandolfini"))
    context_dict['imgFile'] =tmdbSimpleApi.img(context_dict['image'])

    for cred in context_dict['credits']:
        cred['imgFile'] = tmdbSimpleApi.img(cred['image'])
    response = render(request, 'castPage.html',context=context_dict)

    return response

def searchResults(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['search_input']
        matching_list = tmdbSimpleApi.getShow(query)
        if len(matching_list) == 1:
            return redirect(reverse('MyTvList:showPage', args=[query]))
        context_dict = {}
        context_dict ['results'] = matching_list
        for show in context_dict['results']:
            genres = []
            for genre in show['genres'][:2]:
                genres.append(genre['name'])
            show['genres'] = genres
        for pop in context_dict['results']:
            pop['imgFile'] = tmdbSimpleApi.img(pop['poster_path'])
        return render(request, 'searchResults.html', context=context_dict)
    return redirect(reverse('MyTvList:index'))

def showPage(request, name):
    #print(name, tmdbSimpleApi.getId(name))
    context_dict = {'form': SearchForm()}
    context_dict = tmdbSimpleApi.getShowPage(name)
    context_dict['imgFile'] = tmdbSimpleApi.img(context_dict['poster_path'])
    context_dict['videoURL'] = tmdbSimpleApi.getVideo(tmdbSimpleApi.getId(name))
    for castMember in context_dict['cast']:
        #print(castMember['image'])
        castMember['imgFile'] = tmdbSimpleApi.img_crop(tmdbSimpleApi.img_size(castMember['image'], "w300"),0,0,300,400)
    context_dict['last_season']['poster_path'] = tmdbSimpleApi.img(context_dict['last_season']['poster_path'])
    context_dict['networks']['logo_path'] = tmdbSimpleApi.img_size(context_dict['networks']['logo_path'], "w45")
    context_dict['last_season']['air_date_year'] =  context_dict['last_season']['air_date'][:4]
    if context_dict['last_season']['overview'] == "":
        context_dict['last_season']['overview'] = context_dict['last_season']['name']+" of "+name+" premiered on "+str(context_dict['last_season']['air_date'])
    if context_dict['in_production'] == True:
        context_dict['in_production'] = "Current Season"
    else:
        context_dict['in_production'] = "Last Season"
    query = Review.objects.filter(showTitle = name).order_by('-rating')
    if not query:
        context_dict['review'] = query
    else:
        context_dict['review'] = query[0]
    return render(request, 'showPage.html', context=context_dict)

def showPageReviews(request, name):
    context_dict = {'form': SearchForm()}
    context_dict = tmdbSimpleApi.getShowPage(name)
    context_dict['imgFile'] = tmdbSimpleApi.img_resize(tmdbSimpleApi.img(context_dict['poster_path']), 58, 87)
    query = Review.objects.filter(showTitle = name)
    context_dict['reviews'] = query
    return render(request, 'showPageReviews.html', context=context_dict)


def watchListPage(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    favouriteShow = profile.favourite_show
    #favouriteShowId = tmdbSimpleApi.getId(favouriteShow)
    watchList = profile.watchlist
    if favouriteShow not in watchList:
        watchList.append(favouriteShow)
    context_dict = {}
    context_dict['shows'] = tmdbSimpleApi.getWatchListShows(watchList)
    for show in context_dict['shows']:
        show['imgFile'] = tmdbSimpleApi.img(show['poster_path'])

    context_dict['profilepicture'] = profile.picture
    context_dict['username'] = request.user
    response = render(request, 'watchList.html',context=context_dict)
    return response

def addReview(request, name):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.review_creator = get_object_or_404(UserProfile, user=request.user)
            review.showTitle = name
            review.save()
        else:
            print(form.errors)
    else:
        form = ReviewForm()

    return render(request, 'addReview.html', context = {'form': form, 'title': name})


def showUser(request):
    context_dict = {}
    if request.method == "POST":
        if 'search_input' in request.POST:
            search_input = request.POST['search_input']
            searched_user = get_object_or_404(UserProfile, user=search_input)

            context_dict['Username'] = search_input
            context_dict['UserIcon'] = searched_user.picture
            context_dict['FavouriteShow'] = searched_user.favourite_show



            response = render(request, 'profile.html',context=context_dict)
            return response
    else:
        return redirect(reverse('MyTvList:index'))


def getPoster(request):
    if request.method == "GET":
        file_path = request.GET['file_path']
        width = int(request.GET['width'])
        height = int(request.GET['height'])
    file_path = tmdbSimpleApi.img_resize(file_path, width, height)

    return HttpResponse(file_path)