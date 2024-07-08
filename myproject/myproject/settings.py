import os
from pathlib import Path

# Definice BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Vygenerovaný tajný klíč
SECRET_KEY = 'fawq$&8z9%m0xph@&f4-j9-mijj_b%wsj(47^h&(-bqppn0wd3'

# Zapnutí režimu ladění
DEBUG = True

# Nastavení povolených hostitelů
ALLOWED_HOSTS = ['stanislavtrtek.cz', 'www.stanislavtrtek.cz','80.211.202.17','127.0.0.1']

# Aplikace Django
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    # Přidání aplikace myapp
]
AUTH_USER_MODEL = 'myapp.CustomUser'  # Správně nastavte cestu k vašemu uživatelskému modelu
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'  # Přidání ROOT_URLCONF

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'myapp.context_processors.current_datetime',  # Přidání vlastního kontextového procesoru
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# Databáze
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# Jazyk a časová zóna
LANGUAGE_CODE = 'cs-cz'
TIME_ZONE = 'Europe/Prague'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Statické soubory (CSS, JavaScript, obrázky)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'myapp/static']

STATIC_ROOT = '/root/aplikaceStepIT/myproject/myapp/static/css/'
MEDIA_ROOT = '/root/aplikaceStepIT/myproject/myapp/static/img/'

# Výchozí primární klíčové pole
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Přesměrování po přihlášení a odhlášení
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
