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

## Retrieve a particular order
`GET http://127.0.0.1:8000/api/v1/orders/1/`

```
{
	"ordered_by": {
		"id": 1,
		"customer_name": "shashank",
		"customer_address": "hsr bangalore",
		"customer_phone": "9535441964"
	},
	"status": "out_for_delivery",
	"pizza_list": [{
			"id": 1
		},
		{
			"id": 2
		}
	]
}
```

## Update an order.

In updating the order, there is an option to add/remove a pizza. hence we need to specify `action` inside the `pizza_list` of each `pizzas`

The `action` can be 'add' or 'remove'

`PUT http://127.0.0.1:8000/api/v1/orders/1/`

```
{
	"ordered_by": {
		"id": 1
	},
	"status": "confirmed",
	"pizza_list": [{
			"id": 1,
			"action": "remove"
		},
		{
			"id": 3,
			"action": "add"
		}
	]
}
```

There is an option of updating only the status. This is usually done from the restuarant end (assumption). In this case, the restuarant cannot add or remove a pizza. hence the `action` can be sent as `do_nothing`

`PUT http://127.0.0.1:8000/api/v1/orders/1/`

```
{
	"ordered_by": {
		"id": 1
	},
	"status": "out_for_delivery",
	"pizza_list": [{
			"id": 1,
			"action": "do_nothing"
		},
		{
			"id": 3,
			"action": "do_nothing"
		}
	]
}
```

Following Validations are added:

1. A order status cannot be changed if the status of the order is Cancelled/Delivered

2. When the order status is `out_for_delivery` , no more pizzas can be added or removed.

## Remove an order

`DELETE http://127.0.0.1:8000/api/v1/orders/1/`

We perform a soft delete here and set the status of the order to `cancelled`

## Filter provided:
### for orders:
filter by customer name
`http://127.0.0.1:8000/api/v1/orders/?customer_name=shashank`<\br>
filter by pizza size
`http://127.0.0.1:8000/api/v1/orders/?size=regular`</br>
filter by status
`http://127.0.0.1:8000/api/v1/orders/?status=confirmed`</br>

# To run tests

`python manage.py test orders.tests.test_views`





