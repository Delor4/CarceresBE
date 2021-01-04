ENDPOINTY
====

Metody dostępne przy endpointach (jeżeli nie zaznaczono inaczej):
- `GET`, `GET /<id>` dane wszystkich/pojedyńczego obiektu
- `POST` dodanie obiektu
- `PUT /<id>` uaktualnienie danych obiektu
- `DELETE /<id>` usunięcie obiektu
- `HEAD`, `HEAD /<id>` informacje o endpoint'cie

----

`/api/users`  użytkownicy systemu

Parametry:
- `    'id': Integer,`
- `    'name': String,` UQ login
- `    'user_type': Integer,` 1 - admin, 2 - mod, 3 - klient, 4 - inne
- `    'email': String`,
- `    'password': String` WO
- `    'failed_logins' Integer,` RO, aktualna liczba nieudanych logowań
- `    'blocked_since' DateTime,` RO, do kiedy zablokowane logowanie (null jeżeli nie było blokad)
- `    'client': (client_fields),` RO
- `    'uri': Url` RO

----

`/api/clients` klienci

Parametry:
- `'id': Integer,`
- `    'name': String,` Imię, 
- `    'surname': String`,
- `    'address': String`,
- `    'city': String`,
- `    'phone': String`,
- `    'birthday': Date`,
- `    'cars': (car_fields)`, RO
- `    'user_id' Integer`,
- `    'user' (user_fields) `, RO
- `    'uri': Url`, RO

---
`/api/cars` samochody

Parametry:
- ` 'id': Integer,`
- `    'plate': String,`
- `    'brand': String`,
- `    'client_id': Integer,`
- `    'client': (client_fields),` RO
- `    'uri': Url,` RO

----
`/api/zones` strefy parkowania

  Parametry:
- `  'id': Integer,`
- `    'name': String,`
- `    'bkg_file': String,`
- `    'places':place_fields,` RO
- `    'uri': Url,` RO

---
`/api/places` miejsca parkowania

Parametry:
- ` 'id': Integer,`
- `   'nr': Integer,` NN
- `    'zone_id': Integer,` NN
- `    'name': String,`
- `    'pos_x': Float,`
- `    'pos_y': Float,`
- `    'occupied' Boolean,` RO
- `    'uri': Url,`RO

---
`/api/subscriptions` subskrypcje
  
Parametry:
- `    'id': Integer,`
- `    'start': DateTime,`
- `    'end': DateTime,`
- `    'type': Integer,`
- `    'place_id': Integer,`
- `    'place':place_fields,` RO
- `    'car_id': Integer,`
- `    'car': (car_fields)`, RO
- `    'payment': (payment_fields)`, RO
- `    'uri': Url,`RO

---
`/api/payments` płatności

Parametry:
- `    'id': Integer,`
-  `   'price': Integer,` cena netto (w groszach)
- `   'tax': Integer,`podatek (w procentach)
-  `   'value': Integer,` RO, cena brutto (w groszach)
-  `   'sale_date': DateTime,` data sprzedaży
-  `   'paid_type': Integer,` rodzaj płatności (0-brak, 1-na miejscu, 2-online)
-  `   'paid_date': DateTime,` data płatności
-  `   'paid': Boolean,` RO
-  `   'subscription_id': Integer,`
- `    'uri': Url,`RO

---
`/api/zones/<id>/info` statystyki strefy parkowania

Dozwolone metody: `GET /<id>`

  Parametry:
- `    'all': Integer,` RO, całkowita ilość miejsc parkingowych w strefie
- `    'free': Integer,` RO, wolne miejsca
- `    'occupied': Integer,` RO, zajęte miejsca
- `    'zone_id': Integer,` RO

---

Lista endpointów z ograniczonym dostępem
---
(dane tylko aktualnie autoryzowanego użytkowanika/klienta) 


---
`/api/user` dane użytkownika

Dozwolone metody: `GET`, `PUT`

---
`/api/client` dane klienta

Dozwolone metody: `GET`, `PUT`

---
`/api/client/subscriptions` dane rezerwacji klienta

Dozwolone metody: `GET`, `POST`

---
`/api/client/payments` płatności klienta

Dozwolone metody: `GET`, `GET /<id>`, `PUT /<id>`
(po wywołaniu `PUT /<id>` status zostaje ustawiony na `zapłacono online` z aktualną datą)

---
`/api/client/cars/` samochody klienta

Dozwolone metody: `GET`, `GET /<id>`

---

Legenda:
- RO - Read Only
- WO - Write Only
- UQ - Unique
- NN - Not Null
