[CarceresBE](https://github.com/Delor4/CarceresBE)
===================
Backend (REST API) for Parking Management System by SKS
---

RESTful HTTP API using [Flask](https://github.com/pallets/flask), [Flask-Restful](https://github.com/flask-restful/flask-restful) and [SQLAlchemy](https://github.com/zzzeek/sqlalchemy)
-------------------

```
cd app
```

- Install requisite packages:
```shell
$ make install
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
$ make run
```
- List of endpoints:
- `/api/login`
    (Methods: any)
    Authorize user by login/pass. Returns tokens.
- `/api/refresh`
    (Methods: `POST`)
    Authorize user by refresh token. Returns tokens.
- `/api/user`
    (Methods: `GET`, `PUT`)
    Current user's data.
- `/api/client`
    (Methods: `GET`, `PUT`)
    Current client's data.
- `/api/users`
    (Methods: `GET` `POST` `GET /<id>` `PUT /<id>` `DELETE /<id>`)
    User resource.
- `/api/clients`
    (Methods: `GET` `POST` `GET /<id>` `PUT /<id>` `DELETE /<id>`)
    Client resource.
- `/api/cars`
    (Methods: `GET` `POST` `GET /<id>` `PUT /<id>` `DELETE /<id>`)
    Car resource.
- `/api/zones`
    (Methods: `GET` `POST` `GET /<id>` `PUT /<id>` `DELETE /<id>`)
    Zone resource.
- `/api/places`
    (Methods: `GET` `POST` `GET /<id>` `PUT /<id>` `DELETE /<id>`)
    Place resource.
- `/api/subscriptions`
    (Methods: `GET` `POST` `GET /<id>` `PUT /<id>` `DELETE /<id>`)
    Subscription resource.

---
Authorization
-------------------

To authorize send username and password (Basic auth) to `/api/login`.
 ```
$ curl -u user_name:user_pass http://<url>/api/login
```
In response you will get a access and refresh tokens. To authenticate in resources endpoints put access token to `x-access-tokens` header's field.
```
$ curl -H "x-access-tokens: <token>" http://<url>/api/users/1
```
To refresh tokens send a valid refresh token to `/api/refresh`.
```
$ curl -H "Content-Type: application/json" --request POST -d'{refresh_token:"<tok>"}' http://<url>/api/refresh
```

----

Don't forget add `Content-Type: application/json` header to your requests!
All requests (except authorization requests) require a set `x-access-tokens` header.
