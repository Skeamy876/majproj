from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='base'),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('accounts/<str:username>/', views.userview, name='userview' ),
    path('logout/', views.logout_request, name='logout'),
    path('accounts/<str:username>/addbook/', views.add_book_request, name='add_book_request'),
    path('accounts/<str:username>/requestbook/', views.request_books, name='request_books'),
    path('add-book/<int:bk>/', views.book_detail, name='book_details'),
    path('<int:bk>/sent', views.book_request_sent, name='book_request_sent'),
    path('remove_book/', views.remove_book, name='remove_book'),
    path('search&results/', views.search, name='search_for_book'),
]