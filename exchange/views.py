from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from exchange.forms import myUserCreationform, UserLoginForm, add_book, AcceptForm, RejectForm, CancelForm, SearchForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, FormView, TemplateView
from django.contrib import messages

from .models import User, Book, BookRequest
from django.db.models import Q

# Create your views here.
    
#Base index view
class BaseView(TemplateView):
    template_name = 'exchange/base.html'
    

class Home(TemplateView):
    template_name = 'exchange/home.html'


class RegistrationView(CreateView):
    template_name = 'exchange/register.html'
    form_class = myUserCreationform

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
        return render(request, self.template_name, {'form': form})

class LoginView(FormView):
    model = User
    template_name = 'exchange/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            super().form_valid(form) 
            return redirect('userview', username=user.username)
            
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('userview', kwargs={'username': self.request.user.username})

  
class logout_request(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect('home')

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

""" class UserView(DetailView):
    model = User
    template_name = 'exchange/user.html'

    def get(self, request, *args, **kwargs):
       return render(request, self.template_name, self.get_context_data())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        context['books'] = Book.objects.filter(owner=user)
        context['book_request_for_requester'] = BookRequest.objects.filter(requester=user, status='pending')
        context['book_requests'] = BookRequest.objects.filter(recipient=user, status='pending')
        context['request_user'] = User.objects.get(id=self.request.user.id)
        return context

    def post(self, request, *args, **kwargs):
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

        if 'cancel' in request.POST:
            form=CancelForm(request.POST)
            if form.is_valid():
                request_id=form.cleaned_data['request_id']
                book_requester_myrequest=BookRequest.objects.get(id=request_id)
                book_requester_myrequest.delete()
                return redirect('userview', username=request.user.username) """
    


    
    
 
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

    if request.method == 'POST':
        if 'cancel' in request.POST:
            form=CancelForm(request.POST)
            if form.is_valid():
                request_id=form.cleaned_data['request_id']
                book_requester_myrequest=BookRequest.objects.get(id=request_id)
                book_requester_myrequest.delete()
                return redirect('userview', username=request.user.username)

    return render(request, 'exchange/user_view.html',{
        'user':user,
        'books':books,
        'book_request_for_requester':book_request_for_requester,
        'request_user':request_user,
        'book_requests':book_requests,
        })
 
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            books = Book.objects.filter(Q(title__icontains=search) | Q(author__icontains=search))

            return render(request, 'exchange/search.html', {'form': form, 'search': search, 'books': books})
    else:
        form = SearchForm()
    return render(request, 'exchange/search.html', {'form': form})
    

    
    


