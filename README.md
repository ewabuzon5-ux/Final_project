System Zarządzania Projektami

Webowa aplikacja do zarządzania projektami, zadaniami i budżetem, stworzona z wykorzystaniem Django. System wspiera koordynację projektów finansowanych z dotacji/grantów z pełnym monitoringiem budżetu wieloletniego i zespołem projektowym.

Cel projektu

Aplikacja umożliwia kompleksowe zarządzanie projektami z funkcjami:
- Koordynacji wieloosobowych zespołów projektowych
- Śledzenia postępu realizacji zadań
- Zarządzania budżetem wieloletnim ze szczegółową kalkulacją kosztów
- Monitorowania rezultatów i celów projektu

Funkcjonalności

Zarządzanie projektami
- Tworzenie, edycja i usuwanie projektów
- Statusy: Rozpoczęty / W trakcie / Zakończony
- Określanie terminów realizacji (data rozpoczęcia i zakończenia)
- Przypisywanie koordynatora i członków zespołu
- Automatyczne liczenie postępu realizacji

Zarządzanie zadaniami
- Pełny CRUD zadań w ramach projektów
- Przypisywanie zadań do wielu osób
- Priorytety (niski, średni, wysoki) i statusy
- Terminy wykonania (deadlines)
- Śledzenie kosztów zadań

Zarządzanie budżetem
- **Źródła finansowania:**
  - Dotacja
  - Wkład własny finansowy
  - Wkład własny niefinansowy
  - Przychody od odbiorców
- **Szczegółowa kalkulacja kosztów:**
  - Kategorie: Koszty realizacji działań / Koszty administracyjne
  - Jednostka miary, koszt jednostkowy, liczba jednostek
  - Podział na lata (wieloletnie planowanie budżetu)
  - Automatyczne liczenie wartości całkowitej i sum

Rezultaty projektu
- Definiowanie celów i rezultatów projektu
- Wartości docelowe (planowany poziom osiągnięcia)
- Sposób monitorowania i źródła informacji
- Statusy: Nie rozpoczęty / W trakcie / Osiągnięty

System ról i uprawnień
- **Koordynator:**
  - Pełna kontrola nad swoimi projektami
  - Tworzenie i edycja projektów, zadań, budżetu
  - Zarządzanie zespołem
- **Wykonawca:**
  - Dostęp do przypisanych projektów
  - Edycja własnych zadań
  - Przeglądanie budżetu (tylko odczyt)

Dashboard
- Statystyki: wszystkie projekty, zakończone, w trakcie
- Liczba przypisanych zadań
- Ostatnie projekty użytkownika
- Paski postępu realizacji zadań i wykorzystania budżetu

REST API

Aplikacja udostępnia RESTful API dla wszystkich głównych modeli danych.

Dostępne endpointy:

- **`GET /api/`** - Lista wszystkich dostępnych endpointów
- **`GET/POST /api/projects/`** - Lista projektów / Tworzenie nowego projektu
- **`GET/PUT/PATCH/DELETE /api/projects/{id}/`** - Szczegóły/edycja/usuwanie projektu
- **`GET/POST /api/tasks/`** - Lista zadań / Tworzenie nowego zadania
- **`GET/PUT/PATCH/DELETE /api/tasks/{id}/`** - Szczegóły/edycja/usuwanie zadania
- **`GET/POST /api/budget-items/`** - Lista pozycji budżetowych
- **`GET/PUT/PATCH/DELETE /api/budget-items/{id}/`** - Szczegóły/edycja/usuwanie pozycji
- **`GET/POST /api/results/`** - Lista rezultatów
- **`GET/PUT/PATCH/DELETE /api/results/{id}/`** - Szczegóły/edycja/usuwanie rezultatu

Autentykacja:

API wymaga uwierzytelnienia. Użyj sesji Django lub tokenu uwierzytelniającego.

Uprawnienia:

- **Koordynatorzy:** Pełen dostęp do swoich projektów (CRUD)
- **Wykonawcy:** Odczyt projektów, edycja przypisanych zadań
- Użytkownicy widzą tylko dane z projektów, do których mają dostęp

Technologie

- **Backend:** Python 3.13, Django 6.0
- **Frontend:** HTML5, CSS3, Bootstrap 5, Font Awesome
- **Baza danych:** SQLite (development)
- **API:** Django REST Framework
- **Autentykacja:** Django Authentication System
- **Narzędzia:** Git, VS Code

Modele danych

- **User / UserProfile** - użytkownicy z rolami (koordynator/wykonawca)
- **Project** - projekty z budżetem, terminami, zespołem
- **Task** - zadania przypisane do projektów i osób
- **BudgetItem** - szczegółowe pozycje budżetowe z podziałem na lata
- **Result** - rezultaty/cele projektów z monitoringiem

Instalacja i uruchomienie

Wymagania
- Python 3.8+
- pip

Kroki instalacji

1. **Sklonuj repozytorium:**
```bash
git clone <url-repozytorium>
cd Final_project
```

2. **Stwórz wirtualne środowisko:**
```bash
python -m venv venv
```

3. **Aktywuj środowisko:**
- Windows (Git Bash): `source venv/Scripts/activate`
- Linux/Mac: `source venv/bin/activate`

4. **Zainstaluj zależności:**
```bash
pip install django djangorestframework psycopg2-binary
```

5. **Wykonaj migracje:**
```bash
python manage.py migrate
```

6. **Stwórz superużytkownika:**
```bash
python manage.py createsuperuser
```

7. **Uruchom serwer:**
```bash
python manage.py runserver
```

8. **Otwórz przeglądarkę:**
```
http://127.0.0.1:8000/
```

## 👤 Autor

Projekt stworzony jako praca końcowa na kurs Python/Django.

**Ewa** - System Zarządzania Projektami

## 📝 Licencja

Projekt edukacyjny.

---

**Status projektu:** ✅ Ukończony  
**Data:** Marzec 2026