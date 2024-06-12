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
from django.utils.dateparse import parse_date

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
def add_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(user=request.user, content=content)
            return redirect('message_list')
    return render(request, 'add_message.html')

@login_required
def message_list(request):
    user_filter = request.GET.get('user')
    date_filter = request.GET.get('date')

    messages = Message.objects.all().order_by('-timestamp')

    if user_filter:
        messages = messages.filter(user_id=user_filter)

    if date_filter:
        date = parse_date(date_filter)
        if date:
            messages = messages.filter(timestamp__date=date)

    users = User.objects.all()

    return render(request, 'message_list.html', {'messages': messages, 'users': users})
def not_authorized(request):
    return render(request, 'not_authorized.html')
