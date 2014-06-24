"""
Local Django project settings.  On deploy, this is overwritten by Ansible.
These are dev machine settings
"""

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')2_rz^&37bs42f_ygj2wg%3!q*50h)!_*&qmm@xj3yh^+p0=wc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'legcowatch',
        'USER': 'legcowatchdb',
        'PASSWORD': 'e8aVqxwaKVXMfBT',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = '/tmp/static/'
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

SCRAPYD_SERVER = 'http://localhost:6800'
# Path to the JSONLines files with scraped items
SCRAPYD_ITEMS_PATH = '/var/legco-watch/scrapyd/items'
# Path to the folder where files are downloaded
SCRAPYD_FILES_PATH = '/var/legco-watch/scrapyd/files'

