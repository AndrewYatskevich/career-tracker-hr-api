python manage.py migrate;
gunicorn hr_system.wsgi:application --bind 0.0.0.0:8000;
