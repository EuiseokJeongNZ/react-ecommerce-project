from pathlib import Path
from datetime import timedelta
import os
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# secret key for Render .env when deploy
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key") 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", # input later like your-backend.onrender.com
    "127.0.0.1,localhost"
).split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django REST Framework - provides API functionality (serializers, viewsets, etc.)
    "rest_framework",
    # Handles Cross-Origin Resource Sharing (allows React frontend to access Django API)
    "corsheaders",
    # Custom application for the e-commerce business logic
    "shop",

    # JWT
    "rest_framework_simplejwt",
    
    # Enables S3 file storage support
    "storages",  
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware", # Enables CORS handling
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://127.0.0.1:3000,http://localhost:3000"
).split(",")

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS",
    "http://127.0.0.1:3000,http://localhost:3000"
).split(",")

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-NZ'

TIME_ZONE = 'Pacific/Auckland'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

if DEBUG:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Giving Permission to User Table in the shop
AUTH_USER_MODEL = "shop.User"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=300),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

SESSION_COOKIE_SAMESITE = "None" if not DEBUG else "Lax"
CSRF_COOKIE_SAMESITE = "None" if not DEBUG else "Lax"

# AWS settings
# AWS credentials (loaded from environment variables for security)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")  # Your AWS access key ID
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")  # Your AWS secret access key

# S3 bucket configuration
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")  # Name of your S3 bucket
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")  # AWS region (e.g., ap-northeast-2)

# Use S3 as the default file storage (instead of local filesystem)
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Construct the S3 domain URL
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# Base URL for serving media files from S3
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"

# Disable query string authentication (makes URLs public)
AWS_QUERYSTRING_AUTH = False

# Prevent overwriting files with the same name
AWS_S3_FILE_OVERWRITE = False

# after fix an erro of aws ec2 verification
# # AWS Redis CACHES Setting
# REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/1")

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": REDIS_URL,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }