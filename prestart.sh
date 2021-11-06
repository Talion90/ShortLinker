#!/usr/bin/env bash

python manage.py makemigrations
sleep 1;
python manage.py migrate
sleep 1;
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" | python manage.py shell
python manage.py runserver 0.0.0.0:8000