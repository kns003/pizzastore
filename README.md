# pizzastore
Pizza Ordering API with Django Rest Framework

# Setting Up Project.
`git clone https://github.com/kns003/pizzastore.git`

## Activate virtualenv with python3
`cd ..`</br>
`virtualenv -p /usr/bin/python3 moberries_env`</br>
`source moberries_env/bin/activate/`

## Install the dependencies
`pip install -r requirements.txt`

## Setup Postgresql database. Follow the steps
`sudo -u postgres psql`</br>
`CREATE DATABASE pizza;`</br>
`CREATE USER moberries WITH PASSWORD 'moberries@098';`</br>
`ALTER ROLE myprojectuser SET client_encoding TO 'utf8';`</br>
`ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';`</br>
`ALTER ROLE myprojectuser SET timezone TO 'UTC';`</br>
`GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;`</br>
`\q`

## Migrate the db fields
`python manage.py migrate`

## Collectstatic
`python manage.py collectstatic`

## Create Super user
`python manage.py createsuperuser`
add the required credentials

## Runserver and view the DRF Browsable API on browser
`python manage.py runserver`
`http://127.0.0.1:8000/api/v1/`

# API Details.
Create Pizzaz either from django-admin or from api.

## To create pizza from api
