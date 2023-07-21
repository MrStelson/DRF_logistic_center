# DRF_logistic_center
## Information about Frameworks:
- Django==4.2.3
- djangorestframework
---
### Start project
```
python -m venv venv
```
```
venv\Scripts\activate
```
```
pip install pip-tools
```
```
pip-sync
```
```
python manage.py runserver
```

### Use Api Root in localhost: http://127.0.0.1:8000/ or requests:

---
### GET REQUEST 
- get all users in http://127.0.0.1:8000/users/
- get all storage in http://127.0.0.1:8000/storages/
- get all products in http://127.0.0.1:8000/products/
- get last five orders in http://127.0.0.1:8000/order/
- get products in storage http://127.0.0.1:8000/storages/<id>/products
- get orders in storage http://127.0.0.1:8000/storages/1/orders

---
### POST REQUEST
---
#### Create user in http://127.0.0.1:8000/users/ </br>
##### Body:
```
{
    "username": "<username>", 
    "email": "<email>", 
    "password": "<password>", 
    "type_user": "consumer" / "provider"
}
```
---
#### Get user token for create storage, product, order in http://127.0.0.1:8000/api-token-auth/ </br>
##### Body:
```
{
    "username": "consumer", 
    "password": "123123"
}
```
---
#### Create storage in http://127.0.0.1:8000/storages/ </br>
##### Body:
```
{
    "name": "<storage name>", 
}
```
##### Headers:
```
{
    "Authorization": "Token <your token>"
}
```
---
#### Create product in http://127.0.0.1:8000/products/ </br>
##### Body:
```
{
    "name": "<product name>",
    "price": "<product price>",
    "amount": <product amount>,
    "storage": <id storage>
}
```
##### Headers:
```
{
    "Authorization": "Token <your token>"
}
```
---
#### Create order in http://127.0.0.1:8000/order/ </br>
##### Body:
```
{
    "amount_product": <amount product>,
    "storage": <id storage>,
    "product": <id product>
}
```
##### Headers:
```
{
    "Authorization": "Token <your token>"
}
```
note: provider user add product to storage; consumer user take products from storage