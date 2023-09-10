from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import UserFlag


def authorization(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            data = UserFlag.objects.get(user=user)

            data.user = user
            data.flag = False

            data.save()

            return redirect('chat')

        else:
            return render(request, 'Authorization/Authorization.html')
    else:
        return render(request, 'Authorization/Authorization.html')
