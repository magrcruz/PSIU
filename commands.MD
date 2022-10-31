py manage.py makemigrations
py manage.py migrate
py manage.py migrate --run-syncdb
py manage.py loaddata .\psiu\fixtures\starterUsers.yaml
py manage.py loaddata .\psiu\fixtures\starterData.yaml 
py manage.py runserver