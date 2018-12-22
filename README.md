# pizzastore
Pizza Ordering API with Django Rest Framework

# Setting Up the Project.
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
`python manage.py runserver`</br>
`http://127.0.0.1:8000/api/v1/`

# API Details.
Create Pizza either from django-admin or from the below command line.
`python manage.py create_pizzas`

## Creating order:
`POST http://127.0.0.1:8000/api/v1/orders/`

```
{
	"ordered_by": {
		"customer_name": "Shashank",
		"customer_address": "HSR Layout Bangalore",
		"customer_phone": "9535441964"
	},
	"pizza_list": [{
		"id": 1
	}, {
		"id": 2
	}]
}
```

## Get list of orders
`GET http://127.0.0.1:8000/api/v1/orders/`

```
{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [{
		"ordered_by": {
			"id": 1,
			"customer_name": "shashank",
			"customer_address": "hsr bangalore",
			"customer_phone": "9535441964"
		},
		"status": "confirmed",
		"pizza_list": [{
			"id": 1
		}, {
			"id": 2
		}]
	}]
}
```

