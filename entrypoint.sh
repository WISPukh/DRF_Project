python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 DRF_Project.wsgi
