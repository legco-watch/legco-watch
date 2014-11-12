"""
Settings local to the machine.
"""
SECRET_KEY = ')2_rz^&37bs42f_ygj2wg%3!q*50h)!_*&qmm@xj3yh^+p0=wc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

DEBUG_TOOLBAR_PATCH_SETTINGS = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'legcowatch',
        'USER': 'legcowatchdb',
        'PASSWORD': 'e8aVqxwaKVXMfBT',
        'HOST': 'db',
        'PORT': '5432'
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = '/legcowatch/.app/static/'
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# SCRAPYD_SERVER = '{{ scrapyd.address }}'
# Path to the JSONLines files with scraped items
# SCRAPYD_ITEMS_PATH = '{{ scrapyd.items_dir }}'
# Path to the folder where files are downloaded
# SCRAPYD_FILES_PATH = '{{ scrapyd.files_dir }}'
