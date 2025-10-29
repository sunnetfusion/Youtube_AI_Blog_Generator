web: mkdir -p staticfiles && python manage.py collectstatic --noinput && python manage.py migrate --noinput && gunicorn ai_blog_app.wsgi --bind 0.0.0.0:$PORT --timeout 300 --workers 2 --log-file -
