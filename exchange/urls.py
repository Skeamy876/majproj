from django.urls import path
from . import views
from exchange.views import (RegistrationView, LoginView, BaseView, logout_request,Home)


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('accounts/<str:username>/', views.userview, name='userview' ),
   # path('accounts/<str:username>/', UserView.as_view(), name='userview'),
    path('logout/', logout_request.as_view(), name='logout'),
    path('accounts/<str:username>/addbook/', views.add_book_request, name='add_book_request'),
    path('accounts/<str:username>/requestbook/', views.request_books, name='request_books'),
    path('add-book/<int:bk>/', views.book_detail, name='book_details'),
    path('<int:bk>/sent', views.book_request_sent, name='book_request_sent'),
    path('remove_book/', views.remove_book, name='remove_book'),
    path('search&results/', views.search, name='search_for_book'),
]