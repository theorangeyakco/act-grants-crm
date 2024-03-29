import contextlib
import os

import dj_database_url
from dotenv import load_dotenv

with contextlib.suppress(Exception):
	load_dotenv()

# Core Settings
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ROOT_URLCONF = 'backend.urls'
WSGI_APPLICATION = 'backend.wsgi.application'

SECRET_KEY = os.environ.get('SECRET_KEY')

ADMINS = [
	('ACT Grants Administration', 'actgrants.developers@gmail.com')
]

MANAGERS = [
	('ACT Grants Administration', 'actgrants.developers@gmail.com')
]

AUTH_USER_MODEL = 'main.User'

# Security Settings
DEBUG = True if os.environ.get('DEBUG', '0') == '1' else False

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['*']
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

SECURE_CONTENT_TYPE_NOSNIFF = \
	SECURE_HSTS_INCLUDE_SUBDOMAINS = \
	SECURE_HSTS_PRELOAD = \
	SECURE_BROWSER_XSS_FILTER = \
	SECURE_SSL_REDIRECT = \
	SESSION_COOKIE_SECURE = \
	CSRF_COOKIE_SECURE = not DEBUG

if not DEBUG:
	X_FRAME_OPTIONS = 'DENY'
	SECURE_REFERRER_POLICY = 'same-origin'
	SECURE_HSTS_SECONDS = 31536000
	SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Database Settings
# set true if you don't want to use a preconfigured database
if os.environ.get('NO_DATABASE') == 'True':
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME'  : 'mydatabase'
		}
	}
else:
	DATABASES = {
		'default': dj_database_url.config(
				conn_max_age=600,
				default=os.environ.get('DATABASE_URL')
		)
	}

# AWS Settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
	'CacheControl': 'max-age=86400',
}

AWS_S3_ENDPOINT_URL = 'https://s3.ap-south-1.amazonaws.com'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'ap-south-1'

AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = None
AWS_MEDIA_LOCATION = 'media'
AWS_PRIVATE_MEDIA_LOCATION = 'media/private'

S3DIRECT_DESTINATIONS = {
	'issues': {
		# "key" [required] The location to upload file
		#       1. String: folder path to upload to
		#       2. Function: generate folder path + filename using a function
		'key'    : 'uploads/issues/',

		# "auth" [optional] Limit to specfic Django users
		#        Function: ACL function
		'auth'   : lambda u: u.is_staff,

		# "allowed" [optional] Limit to specific mime types
		#           List: list of mime types
		'allowed': ['application/pdf']
	}
}

# Static files
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, 'static')]

if DEBUG:
	STATIC_URL = '/static/'
	STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
	WHITENOISE_MAX_AGE = 31536000  # Cache static files for one year
else:
	STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
	STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media File Storage
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)
MEDIA_ROOT = MEDIA_URL

DEFAULT_FILE_STORAGE = 'backend.media_storages.PublicMediaStorage'
PRIVATE_FILE_STORAGE = 'backend.media_storages.PrivateMediaStorage'

# Internalization Settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Email Settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'actgrants.developers@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('MAILER_PASSWORD')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'ACT Grants <actgrants.developers@gmail.com>'
SERVER_EMAIL = 'ACT Grants <actgrants.developers@gmail.com>'

CORS_ORIGIN_ALLOW_ALL = True

# Applications and middleware
INSTALLED_APPS = [
	'whitenoise.runserver_nostatic',  # Needs to be first

	'rest_framework',
	'rest_framework.authtoken',
	'rest_auth',

	'jazzmin',

	# Django apps
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites',
	'django.contrib.sitemaps',
	'django.contrib.humanize',

	# Allauth apps
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'allauth.socialaccount.providers.google',
	'allauth.socialaccount.providers.facebook',
	# 'allauth.socialaccount.providers.microsoft',
	# 'allauth.socialaccount.providers.twitter',

	# Installed Apps
	# 'storages',
	'crispy_forms',
	# 'phonenumber_field',
	# 'ckeditor',
	# 'ckeditor_uploader',
	# 'taggit',
	# 's3direct',
	# 'django_filters',
	# 'corsheaders',
	# 'django_countries',

	# custom apps
	'main.apps.MainConfig',
	'donations.apps.DonationsConfig'
]

# Allauth settings
SITE_ID = 2
SITE_NAME = 'crm.actgrants.in'

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # Either can be used to login
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http' if DEBUG else 'https'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[ACT Grants CRM] '
ACCOUNT_EMAIL_VERIFICATION = 'none'

ACCOUNT_FORMS = {
	'login'                  : 'allauth.account.forms.LoginForm',
	'signup'                 : 'allauth.account.forms.SignupForm',
	'add_email'              : 'allauth.account.forms.AddEmailForm',
	'change_password'        : 'allauth.account.forms.ChangePasswordForm',
	'set_password'           : 'allauth.account.forms.SetPasswordForm',
	'reset_password'         : 'allauth.account.forms.ResetPasswordForm',
	'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
	'disconnect'             : 'allauth.socialaccount.forms.DisconnectForm',
}

if DEBUG:
	INSTALLED_APPS += [
		'django_extensions',
	]

MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
	{
		'BACKEND' : 'django.template.backends.django.DjangoTemplates',
		'DIRS'    : [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS' : {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.template.context_processors.csrf',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
			'debug'             : DEBUG,
		},
	},
]

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_PASSWORD_VALIDATORS = [
	{'NAME':
		 'django.contrib.auth.password_validation'
		 '.UserAttributeSimilarityValidator'},
	{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
	{'NAME':
		 'django.contrib.auth.password_validation.CommonPasswordValidator'},
	{'NAME':
		 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': [
		# 'rest_framework.authentication.BasicAuthentication',
		'rest_framework.authentication.TokenAuthentication',
	],

	'DEFAULT_RENDERER_CLASSES': [
		'rest_framework.renderers.JSONRenderer',
		'rest_framework.renderers.BrowsableAPIRenderer',
	],

	'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
	'PAGE_SIZE'               : 100,

	'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']

}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'main.serializers.UserSerializer',
}

# External Application Settings

# django taggit settings
TAGGIT_CASE_INSENSITIVE = True

# ckeditor settings
CKEDITOR_UPLOAD_PATH = 'media/public/ckeditor/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
	'full'   : {
		'toolbar': 'full',
	},
	'default': {
		'toolbar'           : 'Custom',
		'toolbar_Custom'    : [
			['Bold', 'Italic', 'Underline'],
			['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-'],
			['Image']
		],
		'height'            : '50%',
		'width'             : '100%',
		'toolbarCanCollapse': True,
	},
	'minimal': {
		'toolbar'           : 'Custom',
		'toolbar_Custom'    : [
			['Bold', 'Italic', 'Underline'],
			['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-',
			 'JustifyLeft', 'JustifyCenter',
			 'JustifyRight', 'JustifyBlock'],
			['Image']
		],
		'height'            : '100%',
		'width'             : '100%',
		'toolbarCanCollapse': True,
	},
}

JAZZMIN_SETTINGS = {
	'site_title'     : 'ACT Grants App Administration',
	'site_header'    : 'ACT Grants App Administration',
	'site_logo'      : 'common/img/act_logo.png',
	'welcome_sign'   : 'Welcome to ACT GRants App Management',
	'copyright'      : 'The Orange Yak Co.',
	'search_model'   : 'main.User',

	'topmenu_links'  : [{'name': 'Site Home', 'url': 'index'}],

	'icons'          : {
		'accounts.User': 'fas fa-users-cog',
	},

	'usermenu_links' : [
		{'name': 'Call 9871587593 for Support', 'icon': 'fa fa-phone'}
	],
	"show_ui_builder": False,
}
