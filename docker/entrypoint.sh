#!/bin/bash
NAME="plum"
DJANGODIR=/code/plum/src
NUM_WORKERS=10
DJANGO_SETTINGS_MODULE=plum.settings
DJANGO_WSGI_MODULE=plum.wsgi

cd $DJANGODIR

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

if [ ! -d /data/logs ]; then
    mkdir /data/logs;
fi
if [ ! -d /data/media ]; then
    mkdir /data/media;
fi

if [ "$1" == "init" ]; then
	python3 manage.py collectstatic --noinput
	python3 manage.py compress
	exit 0
fi

if [ "$1" == "web" ]; then
	python3 manage.py migrate --noinput
    exec gunicorn ${DJANGO_WSGI_MODULE}:application \
        --name $NAME \
        --workers $NUM_WORKERS \
        --max-requests 120 \
        --log-level=info \
        --bind=0.0.0.0:80
fi

if [ "$1" == "shell" ]; then
    exec python3 manage.py shell
fi

if [ "$1" == "manage.py" ]; then
    exec python3 $*
fi

echo "Specify argument: init|web|shell|manage.py"
exit 1
