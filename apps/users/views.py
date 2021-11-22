from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.urls import reverse
from .forms import LoginForm, CreateUserForm
from apps.storage.models import Order


@transaction.atomic
def register_view(request, order_id=0):

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            if order_id:
                order = Order.objects.get(id=order_id)
                order.user = new_user
                order.save()
                login(request, new_user)
                return HttpResponseRedirect(reverse('order',
                                                    args=[order_id]))
            else:
                return render(request, 'register_done.html', {'new_user': new_user})
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})


def login_view(request, order_id=0):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if order_id:
                        order = Order.objects.get(id=order_id)
                        order.user = user
                        order.save()
                        return HttpResponseRedirect(reverse('order',
                                                            args=[order_id]))
                    else:
                        return HttpResponseRedirect(reverse('main_page'))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login', args=[0]))
