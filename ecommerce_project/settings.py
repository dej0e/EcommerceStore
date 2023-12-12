import os
import django_on_heroku

# BASE_DIR refers to the root directory of the Django project.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Secret key used for cryptographic signing, should be kept secret in production.
SECRET_KEY = '56fi&j$1yd33cf$1%tupzhlngah17l(*)n^h8p*oh6icv93(h='

# DEBUG mode is a development setting. It should be set to False in production for security.
DEBUG = True

# ALLOWED_HOSTS defines the host/domain names that this Django site can serve.
ALLOWED_HOSTS = []

# INSTALLED_APPS list all Django applications that are activated in this Django instance.
INSTALLED_APPS = [
    # Default Django apps for admin interface, authentication, etc.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom app for the store
    'store',

    # Third-party apps
    'stripe',  # For payment processing
    'crispy_forms',  # For better form rendering
    "crispy_bootstrap4",  # Bootstrap4 template pack for crispy forms
    'widget_tweaks',  # For tweaking form field rendering in templates
]

# MIDDLEWARE is a list of middleware to be used in the request/response lifecycle.
MIDDLEWARE = [
    # Various Django middleware for security, session management, etc.
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ROOT_URLCONF points to the URL configurations of the ecommerce_project.
ROOT_URLCONF = 'ecommerce_project.urls'

# TEMPLATES configuration, including the template engines to be used.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Directories to search for templates.
        'APP_DIRS': True,  # Whether to look for templates inside installed apps.
        'OPTIONS': {
            'context_processors': [
                # Default context processors.
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Custom context processors for the store.
                'store.context_processors.menu_links',
                'store.context_processors.counter',
            ],
        },
    },
]

# WSGI_APPLICATION points to the WSGI callable that Django should use for serving the project.
WSGI_APPLICATION = 'ecommerce_project.wsgi.application'

# DATABASES configuration. Here, using SQLite as the database.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# AUTH_PASSWORD_VALIDATORS are used for password validation in the auth system.
AUTH_PASSWORD_VALIDATORS = [
    # Various validators for password characteristics.
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

# Internationalization settings.
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True  # Internationalization
USE_L10N = True  # Localization
USE_TZ = True  # Timezone support

# Static files (CSS, JavaScript, Images) configuration.
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')

# Stripe API keys for payment processing.
STRIPE_PUBLISHABLE_KEY = 'pk_test_51OJeLnIQcgxBnKzp3IfQaCLKbXQ2VGjbx6Q3CvGEWtX1Ch7SOQX4nf4zOoozRf9lgUKjDH7XTzQR6QbNhlIPvT3a003m8JajEM'
STRIPE_SECRET_KEY = 'sk_test_51OJeLnIQcgxBnKzpHd5Ae8Q8eYT4TS3yElOxstRDXrOENkR12bfMuFvLP0SFP2qeOD2rjOq0zHbBlZszhTwcHHLt00I7YxHaND'

# Crispy forms configuration.
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Automatically configure Django settings for deployment on Heroku.
django_on_heroku.settings(locals())
