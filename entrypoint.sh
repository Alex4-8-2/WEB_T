set -e

sleep 3

python app/manage.py migrate --noinput
python app/manage.py collectstatic --noinput || true


exec "$@"
