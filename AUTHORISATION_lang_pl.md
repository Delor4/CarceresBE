Autoryzacja użytkownika odbywa się przez wysłanie nazwy użytkownika i hasła pod `/api/login` (basic auth). Jeżeli dane się zgadzają z zapisanymi to w odpowiedzi otrzyma się dynamicznie wygenerowane `access_token` i `refresh_token` (tokeny nie są zapisywane w db).
W przypadku gdy użytkownik 5 razy z rzędu poda niewłaściwe hasło możliwość uzyskania tokenów zostaje zablokowana na 10 minut. (ustawienia w pliku konfiguracyjnym, wartości: `AUTOBLOCKADE_ATTEMPTS`, `AUTOBLOCKADE_TIME`)

Przy błędach uwierzytelniania serwer zwraca response code `401 UNAUTHORIZED` (sam nagłówek z pustą zawartością).

Do uzyskania nowych tokenów (acces i refresh) można użyć `POST /api/refresh`  wysyłając w treści `refresh_token`, np:
```
{'refresh_token':'wartość'}
```

W tokenach są zapisane (m. in.) nazwa użytkownika i 'czas życia' tokenu (czas do ustawienia globalnie w pliku konfiguracyjnym, wartości: `SECRET_ACCESS_KEY_EXPIRATION` oraz `SECRET_REFRESH_KEY_EXPIRATION`. Teraz 1h ale docelowo 10 min.).

Przy połączeniach wymagających autoryzacji trzeba dodawać access_token w specjalnym nagłówku (`x-access-tokens`).
Serwer sprawdza wtedy:

- czy token jest obecny
- czy nie ma błędów w tokenie
- czy token nie jest przedawniony

Przy powyższych błędach zwraca response code `401 UNAUTHORIZED` z komunikatem błędu.

Czasami serwer sprawdza też prawa dostępu do danego połączenia (prawa dostępu są zależne od typu użytkownika).
Przy tym błędzie zwraca response code `403 FORBIDDEN`.
