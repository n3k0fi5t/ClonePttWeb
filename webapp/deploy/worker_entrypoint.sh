
APP=/src
DATA=/DATA

exec supervisord -c $APP/deploy/worker_supervisord.conf
