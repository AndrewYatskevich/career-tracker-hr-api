python manage.py migrate;
python manage.py collectstatic --no-input;
exec gunicorn hr_system.wsgi:application --bind 0.0.0.0:8000;
