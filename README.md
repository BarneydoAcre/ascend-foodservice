# CloudSys

## Build Setup

```bash
# install dependencies
$ pip install django
$ pip install django-cors-headers
$ pip install djoser
$ pip install psycopg2-binary (if linux)
$ pip install reportlab

$ apt install nodejs
$ apt install npm
$ npm install pm2@latest -g
$ pm2 start server.js

$ INSTALED_APPS = [
$    ...
$    'corsheaders',
$    'rest_framework',
$    'rest_framework.authtoken',
$    'rest_framework_simplejwt.token_blacklist',
$    'djoser',
$    ...
$ ]

$ MIDDLEWARE = [
$    ...
$    "corsheaders.middleware.CorsMiddleware",
$    ...
$ ]

$ DATABASES = {
$    'default': {
$        'ENGINE': 'django.db.backends.postgresql_psycopg2',
$        'NAME': 'database',
$        'USER': 'postgres',
$        'PASSWORD': 'postgres',
$        'HOST': 'localhost',
$        'PORT': '5432',
$    }
$ }

$ LANGUAGE_CODE = 'pt-br'
$ TIME_ZONE = 'America/Manaus'

```


# Documentação

## Manipulação de vendas (/sale/)
GET - acessar passando o paramêtro -> ?COMPANY= <-
```
{
	"value": "40",
	"delivery": "5",
	"total": "45",
}
POST - deve seguir o seguindo modelo na requisição passando o TOKEN gerado no login e o paramêtro -> ?COMPANY= <-
```
{
	"value": "40",
	"delivery": "5",
	"total": "45",
	"products": [
		{
			"id": 2,
			"price": 20.0,
			"quantity": 2.0
		}
	]
}
```
PATCH - acessar a url com ID da venda e passando o paramêtro -> ?COMPANY= <- deve-se enviar o parâmetro a ser alterado
Pode se passar qualquer um individualmente

## Manipulação de produtos (/product/)
```
{
    "type": null,
    "name": "",
    "stock": null,
    "cost": null,
    "price": null,
    "company": null,
    "company_worker": null,
    "brand": null,
    "measure": null,
	"product_items": []
}
```
