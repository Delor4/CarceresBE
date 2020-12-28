Stronicowanie wyników
---

Do zapytań zwracających listy (endpointy `GET /api/<model>s` ) można dodawać argumenty ograniczające ilość wyników (parametry zapytania `GET`).

- `start` => wyznacza startowy element listy (domyślnie `1`)
- `limit` => wyznacza maksymalną ilość zwróconych elementów (domyślnie wartość `config["DEFAULT_PAGE_LIMIT"]` lub `25`)

Zwracane wartości to:

- `start`: startowy element zwróconej listy
- `limit`: określony limit
- `count`: całkowitą ilość wyników
- `results`: właściwa lista wyników
- `previous`: url do poprzedniej strony z wynikami (puste jeżeli brak poprzedniej)
- `next`: url do następnej strony z wynikami (puste jeżeli brak następnej)
Przykład:
`/api/places?start=109&limit=20`
```js
{
    "count": 110,
    "limit": 20,
    "next": "",
    "previous": "http://localhost:43343/api/places?start=89&limit=20",
    "results": [
        {
            "id": 109,
            "name": null,
            "nr": 51,
            "pos_x": 38.0,
            "pos_y": 82.0,
            "uri": "http://localhost:43343/api/places/109",
            "zone_id": 2
        },
        {
            "id": 110,
            "name": null,
            "nr": 52,
            "pos_x": 41.0,
            "pos_y": 86.0,
            "uri": "http://localhost:43343/api/places/110",
            "zone_id": 2
        }
    ],
    "start": 109
}
```

Gdy parametry wyjdą poza dozwolony zakres zostanie zwrócony kod `404 NOT FOUND` i odpowiedni komunikat.
Np:

```
{
    "message": "Pagination start outside allowed values. Expected: 1 - 110. Provided: 116"
}

{
    "message": "Pagination limit outside allowed values. Expected more than 0. Provided: -1"
}
```

---

[Sortowanie wyników](#sortowanie):
---
Dodając parametr `sort_by` można sortować po polach poszczególnych tabel (uwaga, to nie muszą być pola widoczne w wynikach).
Określanie kierunku sortowania: `desc(pole)`, `asc(pole)`.
Sortując po wielu polach nazwy oddzielamy przecinkiem.

Przykład:
`/api/places?sort_by=asc(zone),desc(pos_y),nr`
