from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# Create your models here.
class User(AbstractUser):
    username=models.CharField(max_length=50,unique=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100,unique=True)
    password=models.CharField(max_length=100)
    books=models.ManyToManyField('Book',related_name='Books_user')
    has_books=models.BooleanField(default=False)
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=[ 'first_name', 'last_name', 'email', 'password']

    def __str__(self):
        return self.username
    
class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_books')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='borrowed_books')
    is_available = models.BooleanField(default=True)
    objects = models.Manager()
    def __str__(self):
        return self.title

       
class book_exchange_model(models.Model):
    users = models.ManyToManyField(User, related_name='user')
    books = models.ManyToManyField(Book, related_name='books_exchange_model')


    
class BookRequest(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'
    REQUEST_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    )
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

 


    


