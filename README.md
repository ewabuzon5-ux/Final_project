# System Zarządzania Projektami

Aplikacja webowa do zarządzania projektami, zadaniami i budżetem, stworzona w Django. System wspiera koordynację projektów finansowanych z dotacji i grantów z pełnym monitoringiem budżetu wieloletniego.

## Cel projektu

Aplikacja umożliwia:
- Koordynację wieloosobowych zespołów projektowych
- Śledzenie postępu realizacji zadań
- Zarządzanie budżetem wieloletnim ze szczegółową kalkulacją kosztów
- Monitorowanie rezultatów i celów projektu

## Funkcjonalności

### Rejestracja i logowanie
- Rejestracja nowych użytkowników z wyborem roli (koordynator/wykonawca)
- Logowanie i wylogowanie
- Walidacja unikalności adresu email
- Automatyczne tworzenie profilu użytkownika

### Zarządzanie projektami
- Tworzenie, edycja i usuwanie projektów
- Statusy: Rozpoczęty, W trakcie, Zakończony
- Terminy realizacji (data rozpoczęcia i zakończenia)
- Przypisywanie koordynatora i członków zespołu
- Automatyczne liczenie postępu realizacji
- Walidacja dat (zakończenie musi być po rozpoczęciu)

### Zarządzanie zadaniami
- Pełny CRUD zadań w ramach projektów
- Przypisywanie zadań do wielu osób
- Priorytety (niski, średni, wysoki) i statusy
- Terminy wykonania
- Śledzenie kosztów zadań

### Zarządzanie budżetem
- Źródła finansowania: dotacja, wkład własny finansowy i niefinansowy, przychody od odbiorców
- Szczegółowa kalkulacja kosztów z podziałem na:
  - Kategorie (koszty realizacji działań, koszty administracyjne)
  - Jednostka miary, koszt jednostkowy, liczba jednostek
  - Podział na lata (wieloletnie planowanie budżetu)
- Automatyczne liczenie wartości całkowitej i sum
- Walidacja budżetu (suma źródeł musi równać się budżetowi całkowitemu)

### Rezultaty projektu
- Definiowanie celów i rezultatów projektu
- Wartości docelowe (planowany poziom osiągnięcia)
- Sposób monitorowania i źródła informacji
- Statusy: Nie rozpoczęty, W trakcie, Osiągnięty

### System ról i uprawnień
- **Koordynator:** pełna kontrola nad swoimi projektami, tworzenie i edycja projektów, zadań, budżetu, zarządzanie zespołem
- **Wykonawca:** dostęp do przypisanych projektów, edycja własnych zadań, przeglądanie budżetu (tylko odczyt)

### Dashboard
- Statystyki: wszystkie projekty, zakończone, w trakcie
- Liczba przypisanych zadań
- Ostatnie projekty użytkownika
- Paski postępu realizacji zadań i wykorzystania budżetu

## REST API

Aplikacja udostępnia RESTful API dla wszystkich głównych modeli danych.

### Dostępne endpointy:

- GET /api/ - lista wszystkich dostępnych endpointów
- GET/POST /api/projects/ - lista projektów, tworzenie nowego projektu
- GET/PUT/PATCH/DELETE /api/projects/{id}/ - szczegóły, edycja, usuwanie projektu
- GET/POST /api/tasks/ - lista zadań, tworzenie nowego zadania
- GET/PUT/PATCH/DELETE /api/tasks/{id}/ - szczegóły, edycja, usuwanie zadania
- GET/POST /api/budget-items/ - lista pozycji budżetowych
- GET/PUT/PATCH/DELETE /api/budget-items/{id}/ - szczegóły, edycja, usuwanie pozycji
- GET/POST /api/results/ - lista rezultatów
- GET/PUT/PATCH/DELETE /api/results/{id}/ - szczegóły, edycja, usuwanie rezultatu

### Autentykacja

API wymaga uwierzytelnienia. Użyj sesji Django.

### Uprawnienia

- Koordynatorzy: pełen dostęp do swoich projektów (CRUD)
- Wykonawcy: odczyt projektów, edycja przypisanych zadań
- Użytkownicy widzą tylko dane z projektów, do których mają dostęp

## Walidacja formularzy

Aplikacja zawiera walidację danych:
- Unikalność adresu email przy rejestracji
- Data zakończenia projektu musi być późniejsza niż data rozpoczęcia
- Suma źródeł finansowania musi równać się budżetowi całkowitemu
- Wyświetlanie czytelnych komunikatów błędów

## Docker

Aplikacja jest w pełni skonteneryzowana i gotowa do uruchomienia w Docker.

### Struktura Docker:
- Dockerfile - definicja obrazu aplikacji Django
- docker-compose.yml - orkiestracja kontenerów (web + PostgreSQL)
- Automatyczne migracje przy starcie kontenera
- Volume dla PostgreSQL - trwałe przechowywanie danych
- Health checks - sprawdzanie gotowości bazy danych

### Komendy Docker:

Budowanie i uruchomienie:
```bash
docker-compose up --build
```

Uruchomienie w tle:
```bash
docker-compose up -d
```

Sprawdzenie logów:
```bash
docker-compose logs -f web
```

Zatrzymanie:
```bash
docker-compose down
```

Usunięcie z danymi:
```bash
docker-compose down -v
```

## Technologie

- Backend: Python 3.13, Django 6.0
- Frontend: HTML5, CSS3, Bootstrap 5, Font Awesome
- Baza danych: SQLite (lokalne uruchomienie), PostgreSQL (Docker)
- API: Django REST Framework
- Autentykacja: Django Authentication System
- Konteneryzacja: Docker, Docker Compose
- Narzędzia: Git, VS Code

## Modele danych

- User / UserProfile - użytkownicy z rolami (koordynator/wykonawca)
- Project - projekty z budżetem, terminami, zespołem
- Task - zadania przypisane do projektów i osób
- BudgetItem - szczegółowe pozycje budżetowe z podziałem na lata
- Result - rezultaty i cele projektów z monitoringiem

## Instalacja i uruchomienie

### Metoda 1: Docker (zalecana)

#### Wymagania
- Docker
- Docker Compose

#### Kroki:

1. Sklonuj repozytorium:
```bash
git clone https://github.com/ewabuzon5-ux/Final_project.git
cd Final_project
```

2. Uruchom aplikację:
```bash
docker-compose up --build
```

3. Stwórz superużytkownika (w nowym terminalu):
```bash
docker-compose exec web python manage.py createsuperuser
```

4. Otwórz przeglądarkę:
```
http://localhost:8000/
```

5. Zatrzymanie:
```bash
docker-compose down
```

Uwaga: Dane w PostgreSQL są przechowywane w volume postgres_data i pozostają nawet po zatrzymaniu kontenerów.

### Metoda 2: Lokalne uruchomienie (bez Dockera)

#### Wymagania
- Python 3.8 lub nowszy
- pip

#### Kroki:

1. Sklonuj repozytorium:
```bash
git clone https://github.com/ewabuzon5-ux/Final_project.git
cd Final_project
```

2. Stwórz wirtualne środowisko:
```bash
python -m venv venv
```

3. Aktywuj środowisko:
- Windows (Git Bash): source venv/Scripts/activate
- Linux/Mac: source venv/bin/activate

4. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

5. Wykonaj migracje:
```bash
python manage.py migrate
```

6. Stwórz superużytkownika:
```bash
python manage.py createsuperuser
```

7. Uruchom serwer:
```bash
python manage.py runserver
```

8. Otwórz przeglądarkę:
```
http://127.0.0.1:8000/
```

## Autor

Projekt stworzony jako praca końcowa na kurs Python/Django.

Ewa - System Zarządzania Projektami

## Licencja

Projekt edukacyjny - wykorzystanie do celów nauki i rozwoju.

---

Status projektu: Ukończony
Data: Marzec 2026