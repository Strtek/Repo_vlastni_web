from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date
from django.db import IntegrityError
from django.utils import timezone
from .forms import MessageForm
from .forms import UserRegistrationForm
from .models import CustomUser, Message

User = get_user_model()

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
                    user.is_active = False  # deaktivace do potvrzení
                    user.save()

                    current_site = get_current_site(request)
                    subject = 'Potvrďte svou registraci'
                    message = render_to_string('activation_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })
                    user.email_user(subject, message)

                    messages.success(request, 'Registrace proběhla úspěšně. Zkontrolujte svůj e-mail pro potvrzení registrace.')
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

def activate(request, uidb64, token):
    from django.utils.encoding import force_str
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Registrace potvrzena, nyní se můžete přihlásit.')
        return redirect('login')
    else:
        return render(request, 'activation_invalid.html')