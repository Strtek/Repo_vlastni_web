from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Message
from .forms import MessageForm

def home(request):
    return render(request, 'home.html', {'name': 'Stanislav Trtek'})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('message_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def message_list(request):
    messages = Message.objects.all()
    form = MessageForm()
    return render(request, 'message_list.html', {'messages': messages, 'form': form})

@login_required
def add_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'add_message.html', {'form': form})
