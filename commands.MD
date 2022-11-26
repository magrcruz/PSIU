py manage.py makemigrations
py manage.py migrate
py manage.py migrate --run-syncdb
python manage.py runscript createAdmin
py manage.py loaddata .\psiu\fixtures\starterUsers.yaml
py manage.py loaddata .\psiu\fixtures\starterData.yaml 
py manage.py runserver
pip install -r requirements.txt
py manage.py createsuperuser
admin
admin@gmail.com
admin
admin
y
venv\Scripts\activate.bat