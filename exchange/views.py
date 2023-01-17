from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from exchange.forms import myUserCreationform, UserLoginForm, add_book, AcceptForm, RejectForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, Book, BookRequest
# Create your views here.
    
#Base index view
def base(request):
    return render(request, 'exchange/base.html',{})

#registration view
def register_request(request):
    if request.method=='POST':
        regform = myUserCreationform(request.POST)
        if regform.is_valid():
            username = regform.cleaned_data['username']
            password = regform.cleaned_data['password1']
            email = regform.cleaned_data['email']
            first_name = regform.cleaned_data['first_name']
            last_name = regform.cleaned_data['last_name']
            has_books = regform.cleaned_data['has_books']
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, has_books=has_books)
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'Invalid form')
            return render(request, 'exchange/register.html',{'form':regform})
            
    else:
        regform = myUserCreationform()
        return render(request, 'exchange/register.html',{'form':regform})

#login view
def login_request(request):
    if request.method=='POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('userview', username=user.username)
            else:
                messages.error(request, 'Invalid username or password')
                return render(request, 'exchange/login.html',{'form':form})
        else:
            messages.error(request, 'Invalid form')
            return render(request, 'exchange/login.html',{'form':form})
    form = UserLoginForm()
    return render(request, 'exchange/login.html',{'form':form})

@login_required
def logout_request(request):
    logout(request)
    return redirect('base')

@login_required
def add_book_request(request, username):
    if request.method=='POST':
        form= add_book(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
            author=form.cleaned_data['author']
            owner=request.user
            book=Book.objects.create(title=title, author=author, owner=owner)
            book.save()
            return redirect('userview', username=request.user.username)
    form = add_book()
    return render(request, 'exchange/add_book.html',{'form':form})


def request_books(request,  username):   
    books=Book.objects.exclude(owner=request.user)
    return render(request, 'exchange/request_books.html',{'books':books})


def book_detail(request, bk):
    book=get_object_or_404(Book, id=bk)
    return render(request, 'exchange/book.html',{'books':book})
    

def book_request_sent(request, bk):
    book=get_object_or_404(Book, id=bk)
    if request.user== book.owner:
        return redirect('userview', username=request.user.username)
    book_request= BookRequest.objects.filter(requester=request.user, book=book)
    if book_request.exists():
        return redirect('userview', username=request.user.username)
    else:
        book_request=BookRequest.objects.create(requester=request.user, book=book, recipient=book.owner, status='pending')
        book_request.save()
        return render(request, 'exchange/Components/book_request_sent.html') 

def accept_book_request(request, request_id):
    if request_id is not None:
        book_request=get_object_or_404(BookRequest, id=request_id)
        user_requester=User.objects.get(id=book_request.requester.id)
        book=Book.objects.get(id=book_request.book.id)
        if book_request.recipient != request.user:
            return redirect('userview', username=request.user.username)
        else:
            book_request.status='accepted'
            user_requester.books.set([book])
            book.owner=user_requester
            user_requester.save()
            book.save()
            book_request.save()
            return redirect('userview', username=request.user.username)
    else:
        return HttpResponse('Not executed')


def decline_book_request(request, request_id):
    book_request = get_object_or_404(BookRequest, id=request_id)
    if book_request.recipient != request.user:
        return redirect('userview', username=request.user.username)
    else:
        book_request.status = 'declined'
        book_request.save()
        #inplement request declined notification
        return redirect('userview', username=request.user.username)

@login_required
def remove_book(request):
    if request.method == 'POST':
        selected_books = request.POST.getlist('books')
        Book.objects.filter(id__in=selected_books, owner=request.user).delete()
    book=Book.objects.filter(owner=request.user)
    return render(request, 'exchange/remove_book.html',{'books':book})
 
#userview
login_required(login_url='login')
def userview(request, username):
    user=get_object_or_404(User, username=username)
    books=Book.objects.filter(owner=user)
    book_request_for_requester=BookRequest.objects.filter(requester=user, status='pending')
    book_requests=BookRequest.objects.filter(recipient=user, status='pending')
    request_user=User.objects.get(id=request.user.id)
   
    if request.method == 'POST':
        if 'accept' in request.POST:
            form = AcceptForm(request.POST)
            if form.is_valid():
                request_id = form.cleaned_data['request_id']
                accept_book_request(request, request_id)
        elif 'reject' in request.POST:
            form = RejectForm(request.POST)
            if form.is_valid():
                request_id = form.cleaned_data['request_id']
                decline_book_request(request, request_id)

    return render(request, 'exchange/user_view.html',{
        'user':user,
        'books':books,
        'book_request_for_requester':book_request_for_requester,
        'request_user':request_user,
        'book_requests':book_requests,
        })

