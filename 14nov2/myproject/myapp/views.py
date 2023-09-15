from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.paginator import Paginator
from .models import Contact


# Home
def home(request):
    ap = Post.objects.all().order_by('id')
    threepage = Paginator(ap, 3, orphans=1)
    pagenumber = request.GET.get('page')
    po = threepage.get_page(pagenumber)

    return render(request, 'myapp/home.html', {'po': po})


# About
def about(request):
    return render(request, 'myapp/about.html')


# Contact
def contact(request):
    if request.method == 'POST':
        n = request.POST['name']
        e = request.POST['email']
        a = request.POST['address']
        m = request.POST['message']
        con = Contact(name=n, email=e, address=a, message=m)
        con.save()
        messages.success(request, 'submitted successfully')
    return render(request, 'myapp/contact.html')


# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        ct = cache.get('count', version=user.pk)
        return render(request, 'myapp/dashboard.html', {'posts': posts, 'full_name': full_name,
                                                        'groups': gps, 'ct': ct})
    else:
        return HttpResponseRedirect('/login/')


# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# Sigup
def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! You have become an Author.')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})


# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully !!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'myapp/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')


# Add New Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'myapp/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


# Update/Edit Post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'myapp/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


# Delete Post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')


def onedata(request, id):
    po = Post.objects.get(id=id)

    return render(request, 'myapp/onedata.html', {'po': po})


def search(request):
    if request.method == 'GET':
        q = request.GET.get('searchbox')
        if q != None:
            po = Post.objects.filter(title__icontains=q)

    return render(request, 'myapp/search.html', {'po': po})

