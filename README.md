# chibi
URL shortener with private API without public interface. Ideal for marketing campaigns on own domain when you don't want to rely on 3rd party.


## Installation

Create database
```bash
psql -d postgres -c "CREATE DATABASE chibi;"
python manage.py migrate
```

Create superuser
```bash
python manage.py createsuperuser
```

Run server

```bash
python manage.py runserver
```

Now open you browser on `127.0.0.1:8000/secret/admin/`. This admin url has been chosen because `admin` is misinterpreted
by Django as a redirect slug and not an admin URL. Since it does not redirect to `admin/` url with slash, `secret/admin/` is used instead. 

## API

On endpoint `api/shorten/` is shortening API service.
API token can be created in admin interface. 

Example of authorization header:
```
Authorization: Token <token>
```

`slug` is not required. In case `slug` is missing, it is generated automatically.

Request payload:
```json
{"url":"https://skra.cz?utm_source=githoub.com&utm_campaign=chibi-repo", "slug": "github"}
```

Example request:
```http request
POST http://localhost:8000/api/shorten/
Content-Type: application/json
Authorization: Token <token>

{"url": "https://skra.cz?utm_source=githoub.com&utm_campaign=chibi-repo"}
```


If `SITE_URL` is not defined in settings then `short_address` is equal to `slug`.

Response:
```json
{"url":"https://skra.cz?utm_source=githoub.com&utm_campaign=chibi-repo", "short_address": "http://localhost:8000/github"}
```
