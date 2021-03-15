
APP=/src
DATA=/DATA

mkdir -p $APP/$DATA/log

n=0
while [ $n -lt 5 ]
do
	python manage.py makemigrations &&
    python manage.py migrate --no-input &&
    python manage.py shell &&
    break
    n=$(($n+1))
    echo "Failed to migrate, going to retry..."
    sleep 8
done

exec supervisord -c $APP/deploy/supervisord.conf
