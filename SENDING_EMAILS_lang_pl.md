
Wysyłanie powiadomień emailowych działa po ustawieniu połączenia z serwerem mail (patrz plik `settings.py`).

Warunki wysłania powiadomienia:
- user ma wpisany email (`user.email != null`)
- do końca rezerwacji jest mniej niż godzina (`subscription.end < (now + 1 hour)`)
- brak flagi wysłania (`subscription.notification_sended == false`)

TODO:
  dodanie możliwości blokowania wysyłania emaili przez użytkownika
