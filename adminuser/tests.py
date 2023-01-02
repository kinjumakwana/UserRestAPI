from django.test import TestCase

# Create your tests here.
# Migrate SQL to Postgresql

#step1: python manage.py dumpdata > datadump.json
# pwd:admin123
# port:5432

# step2&3: download and install
# 1)postgresql 2)pgadmin

# step4
# setting.py
# DATABASES = {
#     'default': {
#          'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'DATABASE NAME',
#         'USER': 'DATABASE USER',
#         'PASSWORD': 'DATABASE PASSWORD',
#         'HOST': 'localhost',
#         'PORT': '5432'
#     }
# }
# step 5: 
# pip install psycopg2
# python manage.py migrate --run-syncdb
# python manage.py loaddata datadump.json