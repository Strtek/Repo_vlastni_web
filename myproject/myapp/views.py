from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Message
from .forms import MessageForm
from .forms import UserRegistrationForm
from django.contrib import messages
from django.db import IntegrityError

def home(request):
    current_time = timezone.now()
    context = {
        'name': 'Stanislav Trtek',
        'current_time': current_time,
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            try:
                if User.objects.filter(username=email).exists():
                    messages.error(request, 'Uživatel s tímto emailem již existuje.')
                else:
                    user = User.objects.create_user(username=email, email=email, password=password)
                    user.first_name = name
                    user.save()
                    messages.success(request, 'Registrace úspěšná. Nyní se můžete přihlásit.')
                    return redirect('login')
            except IntegrityError:
                messages.error(request, 'Došlo k chybě při registraci. Zkuste to prosím znovu.')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def message_list(request):
    user_id = request.GET.get('user')
    if user_id:
        messages = Message.objects.filter(user_id=user_id)
    else:
        messages = Message.objects.all()
    users = User.objects.all()
    form = MessageForm()
    return render(request, 'message_list.html', {'messages': messages, 'form': form, 'users': users, 'selected_user': user_id})

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

def not_authorized(request):
    return render(request, 'not_authorized.html')
