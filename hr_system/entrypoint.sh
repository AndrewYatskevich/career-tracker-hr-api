python manage.py migrate;
exec gunicorn hr_system.wsgi:application --bind 0.0.0.0:8000;
