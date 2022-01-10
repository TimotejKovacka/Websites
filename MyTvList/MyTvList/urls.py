from os import name
from django.urls import path
from MyTvList import views 
app_name = 'MyTvList'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('topshows/', views.topshows, name='topshows'),
    path('recommended/', views.recommended, name='recommended'),
    path('castPage/', views.castPage, name='castPage'),
    path('searchResults/', views.searchResults, name='search'),
    path('showPage/<name>/', views.showPage, name='showPage'),
    path('showPage/<name>/reviews', views.showPageReviews, name='showPageReviews'),
    path('showPage/<name>/reviews/addReview/', views.addReview, name='showPageAddReview'),
    path('watchListPage/', views.watchListPage, name='watchListPage'),
    path('showUser/', views.showUser, name='showUser'),
    path('getPoster/', views.getPoster, name='getPoster'),
]
