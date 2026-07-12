# FitTracker

Progetto per l'esame di Back-end PPM 2026.

**Studentessa:** Sofia Cassioli

## Tipo di progetto

Full-Stack Web Application

## Framework utilizzato

Django

## Descrizione

FitTracker è un'applicazione per tenere traccia dei propri allenamenti in palestra: si possono
registrare gli esercizi svolti (serie, ripetizioni, peso), impostare obiettivi personali e,
se assegnati a un coach, ricevere feedback sui propri allenamenti. Il progetto prevede tre
ruoli distinti: utente standard, coach e amministratore, ognuno con permessi e funzionalità
diverse.

## Funzionalità implementate

### Utente standard
- Registrazione, login e logout
- Creazione, modifica, visualizzazione ed eliminazione dei propri allenamenti
- Aggiunta di esercizi (nome, serie, ripetizioni, peso) a ciascun allenamento
- Creazione, modifica ed eliminazione dei propri obiettivi
- Visualizzazione del proprio profilo

### Coach
- Dashboard dedicata con l'elenco degli atleti assegnati
- Visualizzazione degli ultimi allenamenti di ogni atleta assegnato
- Possibilità di lasciare un feedback testuale su un allenamento specifico

### Amministratore
- Accesso al pannello di amministrazione Django (`/admin/`)
- Gestione di utenti, allenamenti, esercizi, obiettivi e assegnazioni coach-atleta

## Installazione e avvio in locale
git clone https://github.com/sofiacassioli/fittracker.git

cd fittracker

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

Poi apri il browser su `http://127.0.0.1:8000/`.


## Database

Il repository include il file `db.sqlite3`, già popolato con dati demo tramite il comando
personalizzato `populate_demo`. Se
per qualche motivo servisse rigenerare i dati:

python manage.py populate_demo

## Account demo

| Username   | Password   | Ruolo           |
|------------|------------|-----------------|
| admin_demo | admin12345 | Amministratore  |
| user_demo  | user12345  | Utente standard |
| coach_demo | coach12345 | Coach           |

## Deployment

Il progetto è online al seguente indirizzo:

**https://fittracker-u5aj.onrender.com**

Il servizio è ospitato su un piano gratuito di Render, che "addormenta" il sito dopo un
periodo di inattività: la prima richiesta dopo una pausa può richiedere fino a circa 50
secondi per rispondere, poi torna normale.

## Testing scenario

1. Accedere con `user_demo` / `user12345`
2. Andare su "Allenamenti", creare un nuovo allenamento, poi modificalo ed eliminalo
3. Ripetere lo stesso test con "Obiettivi"
4. Fare logout e accedere con `coach_demo` / `coach12345`
5. Andare su "Coach" e verificare che sia visibile l'atleta assegnato (user_demo) con i suoi allenamenti
6. Lasciare un feedback su uno degli allenamenti visualizzati
7. Provare ad accedere a `/coach/` con l'utente `user_demo`: il permesso deve essere negato correttamente
8. Accedere con `admin_demo` / `admin12345` su `/admin/` per esplorare i dati dal pannello di amministrazione