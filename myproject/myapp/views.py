from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import CustomUser, Message
from django.utils import timezone
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
                if CustomUser.objects.filter(username=email).exists():
                    messages.error(request, 'Uživatel s tímto emailem již existuje.')
                else:
                    user = CustomUser.objects.create_user(username=email, email=email, password=password)
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

    if request.user.is_admin:
        messages_query = Message.objects.all()
        if user_filter:
            messages_query = messages_query.filter(user__id=user_filter)
    else:
        messages_query = Message.objects.filter(user=request.user)

    if date_filter:
        date = parse_date(date_filter)
        if date:
            messages_query = messages_query.filter(timestamp__date=date)

    # Pro admina přidáme seznam uživatelů pro možnost filtrování
    users = CustomUser.objects.all() if request.user.is_admin else CustomUser.objects.none()

    return render(request, 'message_list.html', {'messages': messages_query, 'users': users})

def not_authorized(request):
    return render(request, 'not_authorized.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Neplatné uživatelské jméno nebo heslo.')
    return render(request, 'login.html')