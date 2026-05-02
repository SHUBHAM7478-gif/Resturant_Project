from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Receipe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def receipe(request):
    if request.method == "POST":
        data = request.POST
        Receipe.objects.create(
            
            receipe_name = data.get('receipe_name'),
            receipe_description = data.get('receipe_description'),
            receipe_image = request.FILES.get('receipe_image'),
        )
        return redirect('/recipes')
    
    queryset = Receipe.objects.all()
    context = {'receipes': queryset}


    return render(request, 'receipes.html', context)

def update_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    context = {'receipes': queryset}
    if request.method == "POST":
        data = request.POST
        
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description

        if receipe_image:
            queryset.receipe_image = receipe_image

        queryset.save()
        
        return redirect('/recipes')
    
    return render(request, 'update_receipes.html', context)

    



def delete_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
                                   
    return redirect('/recipes')


def search(request):
    query = request.GET.get('searchdata')
    results = []

    if query:
        results = Receipe.objects.filter(
            receipe_name__icontains = query
        )

    return render(request, 'receipes_search.html', {'result': results})



def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, 'Username already exists')
            return render(request, 'register.html', {'error' : 'username already exists.'})
        user = User.objects.create(
            first_name=first_name,
            last_name = last_name,
            username=username,
        )

        # for encryption
        user.set_password(password)
        user.save()
        messages.error(request, 'Account created successfully.')
        return redirect('/login/')
    return render(request, 'register.html')



def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'User does not exist')
            return redirect('/login/')

        user = authenticate(request, username=username, password=password)

        # print("Authenticated user:", user)  # DEBUG

        if user is not None:
            login(request, user)
            return redirect('/recipes/')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('/login/')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')