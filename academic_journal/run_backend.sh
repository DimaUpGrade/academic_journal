sleep 3


# prepare init migration
python manage.py makemigrations

# migrate db, so we have the latest db schema
python manage.py migrate

# Creating superuser
# python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL 

# start development server on public ip interface, on port 8000
python manage.py runserver 0.0.0.0:8000