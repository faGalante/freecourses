# freecourses

**freecourses** è un'applicazione web sviluppata come progetto per l'esame di Introduzione alle Applicazioni Web, presso il Politecnico di Torino.
Il sistema gestisce un catalogo di corsi accessibili da studenti e docenti, con funzionalità di registrazione, login, creazione di corsi, caricamento di materiale e pubblicazione di avvisi.

## Descrizione

FreeCourses è una piattaforma dove i docenti possono creare corsi, caricare materiale didattico (ad esempio, PDF) e pubblicare avvisi. Gli studenti, invece, possono iscriversi ai corsi, visualizzare il materiale, commentare gli avvisi e interagire con i docenti.

### Requisiti principali:
- Autenticazione tramite registrazione e login per studenti e docenti.
- Creazione e gestione dei corsi da parte dei docenti.
- Iscrizione ai corsi da parte degli studenti.
- Caricamento e download di materiale didattico.
- Pubblicazione di avvisi, con possibilità di commento da parte degli studenti.
- Filtraggio dei corsi per categoria tramite JavaScript.

## Funzionalità principali

### 1. **Autenticazione e gestione utenti**:
   - **Registrazione e login**: Gli utenti si registrano come *docenti* o *studenti* tramite un form di registrazione, con autenticazione gestita da **Flask-Login** e **Flask-Session**.
   - **Gestione sessioni**: Una volta effettuato il login, l'utente è autenticato per tutta la sessione di navigazione.
   
### 2. **Gestione dei corsi**:
   - **Creazione dei corsi**: I docenti possono creare corsi, specificando titolo, descrizione, categoria, immagine e prerequisiti (opzionali).
   - **Caricamento di materiale**: Ogni corso può avere materiale didattico in formato PDF, che i docenti possono caricare direttamente nella sezione *Materiale* del corso.

### 3. **Gestione degli avvisi**:
   - **Pubblicazione avvisi**: I docenti possono inserire avvisi relativi al corso, ciascuno con una data e un testo libero.
   - **Commenti sugli avvisi**: Gli studenti iscritti possono commentare gli avvisi, ma ogni commento può essere modificato o eliminato solo dal suo autore.
   
### 4. **Interazione degli studenti con i corsi**:
   - **Iscrizione ai corsi**: Gli studenti possono iscriversi ai corsi di loro interesse direttamente dalla homepage.
   - **Visualizzazione materiale e avvisi**: Una volta iscritti, gli studenti possono visualizzare il materiale e commentare gli avvisi.

### 5. **Filtraggio dei corsi per categoria**:
   - I corsi sono organizzati per categorie. Gli studenti possono selezionare una categoria dal menu e visualizzare solo i corsi appartenenti a quella categoria, con l'uso di JavaScript per manipolare dinamicamente la visualizzazione.

## Tecnologie utilizzate

- **Frontend**:
  - **HTML5**, **CSS3**
  - **Bootstrap** (personalizzato)
  - **JavaScript** (manipolazione del DOM, day.js per la gestione delle date)
  
- **Backend**:
  - **Python** con **Flask**
  - **Flask-Login** e **Flask-Session** per la gestione dell'autenticazione e delle sessioni
  
- **Database**:
  - **SQLite** per la gestione dei dati relativi agli utenti, corsi, avvisi e materiale didattico

## Come avviare il progetto
   Puoi accedere all'applicazione visitando https://fagalante.eu.pythonanywhere.com/ nel tuo browser.

   - **Docenti**: 
     - Username: `scapola.alata@gmail.com` | Password: `password`
     - Username: `maria.grazia@gmail.com` | Password: `password`
   - **Studenti**:
     - Username: `clodina.costantina@libero.it` | Password: `password`
     - Username: `campobaffo@gmail.com` | Password: `password`

## Struttura del progetto

- **app.py**: Il file principale per l'applicazione Flask.
- **/static**: Contiene i file CSS, JavaScript e le immagini.
- **/templates**: Contiene i file HTML per la visualizzazione dell'interfaccia.
- **requirements.txt**: Elenco delle librerie necessarie per il progetto.
- **/database**: Il file SQLite che memorizza i dati.
