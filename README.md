[CarceresBE](https://github.com/Delor4/CarceresBE)
===================
Backend (REST API) for Parking Management System by SKS
---

Clone repository:
```
git clone https://github.com/Delor4/Carceres.git
cd Carceres
git submodule update --init --recursive
```
RESTful HTTP API using [Flask](https://github.com/pallets/flask), [Flask-Restful](https://github.com/flask-restful/flask-restful) and [SQLAlchemy](https://github.com/zzzeek/sqlalchemy)
-------------------

```
cd app
```

- Install requisite packages:
```shell
$ pip install -r requirements.txt
```
- Config file:
`settings.py` (default) or set env variable `CARCERES_CONFIG` eg:
```shell
$ CARCERES_CONFIG=/path/to/my_config.py
$ export CARCERES_CONFIG
```

- Create tables:
```shell
$ make init_db
```

- Run service:
```shell
$ python app.py
```
- List of endpoints:
- `/api/users`
    (Methods: `GET` `POST` `GET /<id>` `PUT /<id>` `DELETE /<id>`)
- `/api/clients`
    (Methods: `GET` `POST` `GET /<id>` `PUT /<id>` `DELETE /<id>`)
- `/api/cars`
    (Methods: `GET` `POST` `GET /<id>` `PUT /<id>` `DELETE /<id>`)
- `/api/zones`
    (Methods: `GET` `POST` `GET /<id>` `PUT /<id>` `DELETE /<id>`)
- `/api/places`
    (Methods: `GET` `POST` `GET /<id>` `PUT /<id>` `DELETE /<id>`)
- `/api/subscriptions`
    (Methods: `GET` `POST` `GET /<id>` `PUT /<id>` `DELETE /<id>`)
- `/api/login`
    (Methods: any)

---
Authorization
-------------------

To authorize send username and password (Basic auth) to `/api/login`.
 ```
$ curl -u user_name:user_pass http://<url>/api/login
```
In response you will get a token. Send token with request in `x-access-tokens` header.
```
$ curl -H "x-access-tokens: <token>" http://<url>/api/users/1
```

Don't forget add `Content-Type: application/json` header to your request!

