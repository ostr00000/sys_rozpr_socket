### Napisać aplikację typu chat (5 pkt.)
- Klienci łączą się serwerem przez protokół TCP
- Serwer przyjmuje wiadomości od każdego klienta i rozsyła je do pozostałych (wraz z id/nickiem klienta)
- Serwer jest wielowątkowy – każde połączenie od klienta powinno mieć swój wątek
- Proszę zwrócić uwagę na poprawną obsługę wątków
### Dodać dodatkowy kanał UDP (3 pkt.)
- Serwer oraz każdy klient otwierają dodatkowy kanał UDP (ten sam numer portu jak przy TCP)
- Po wpisaniu komendy ‘U’ u klienta przesyłana jest wiadomość przez UDP na serwer, który rozsyła ją do pozostałych klientów
- Wiadomość symuluje dane multimedialne (można np. wysłać ASCII Art)
### Zaimplementować powyższy punkt w wersji multicast (2 pkt.)
- Nie zamiast, tylko jako alternatywna opcja do wyboru (komenda ‘M’)
- Multicast przesyła bezpośrednio do wszystkich przez adres grupowy (serwer może, ale nie musi odbierać)
### Uwagi
- Zadanie można oddać w dowolnym języku programowania
- Nie wolno korzystać z frameworków do komunikacji sieciowej – tylko gniazda!
- Nie wolno też korzystać z Akka
### Przy oddawaniu należy:
- zademonstrować działanie aplikacji (serwer + min. 2 klientów)
- omówić kod źródłowy
### Proszę zwrócić uwagę na:
- Poprawność rozwiązania (np. unikanie wysyłania wiadomości dla nadawcy)
- Wydajność rozwiązania (np. pula wątków)
