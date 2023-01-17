from django.contrib import admin

from exchange.models import book_exchange_model, Book, User,BookRequest

# Register your models here

admin.site.register(book_exchange_model)
admin.site.register(Book)
admin.site.register(User)
admin.site.register(BookRequest)
