# 🏀 JBK GESTIONE - Guida Configurazione Supabase

## 📋 Panoramica

JBK Gestione è ora integrato con **Supabase** per offrire:
- ✅ **Autenticazione sicura** con login/logout
- ✅ **Due livelli di accesso**: Amministratore e Utente
- ✅ **Database cloud PostgreSQL** 
- ✅ **Row Level Security (RLS)** per protezione dati
- ✅ **Sincronizzazione real-time** (futura implementazione)

## 🚀 Installazione e Configurazione

### 1. Prerequisiti

- Python 3.8+
- Account Supabase (gratuito)
- Git (opzionale)

### 2. Setup Supabase

#### 2.1 Crea un Progetto Supabase

1. Vai su [https://supabase.com](https://supabase.com)
2. Crea un account gratuito
3. Clicca "New Project"
4. Compila i dettagli:
   - **Nome**: JBK Gestione
   - **Password Database**: (genera una password sicura)
   - **Regione**: Europe West (raccomandato per l'Italia)

#### 2.2 Configura le Credenziali

1. Nel dashboard del progetto, vai in **"Settings" > "API"**
2. Copia i seguenti valori:
   - **Project URL**: `https://your-project.supabase.co`
   - **anon/public key**: `eyJ...` (chiave lunga)

#### 2.3 Importa lo Schema Database

1. Nel dashboard Supabase, vai in **"SQL Editor"**
2. Clicca **"New Query"**
3. Copia e incolla tutto il contenuto del file `supabase_schema.sql`
4. Clicca **"Run"** per eseguire lo script

### 3. Configurazione Applicazione

#### 3.1 Installa le Dipendenze

```bash
# Installa le dipendenze Python
pip install -r requirements.txt
```

#### 3.2 Configura le Variabili d'Ambiente

```bash
# Copia il file di esempio
cp .env.example .env

# Modifica il file .env con i tuoi dati Supabase
nano .env  # o usa il tuo editor preferito
```

Modifica il file `.env`:

```env
# Sostituisci con i tuoi dati reali
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

APP_ENV=development
DEBUG=True
```

### 4. Creazione Primo Utente Amministratore

#### 4.1 Crea Utente tramite Supabase

1. Nel dashboard Supabase, vai in **"Authentication" > "Users"**
2. Clicca **"Add User"**
3. Compila:
   - **Email**: la tua email di amministratore
   - **Password**: password sicura
   - **Email Confirm**: ✅ (già confermato)

#### 4.2 Imposta il Ruolo Admin

1. Vai in **"Database" > "Table Editor"**
2. Seleziona la tabella **"profiles"**
3. Trova l'utente appena creato
4. Modifica il campo **"role"** da `user` a `admin`
5. Salva le modifiche

### 5. Migrazione Dati Esistenti (Opzionale)

Se hai già dati nel database SQLite locale:

```bash
# Esegui lo script di migrazione
python migrate_to_supabase.py
```

**IMPORTANTE**: 
- Devi essere autenticato come admin per la migrazione
- Il script trasferirà tutti i dati esistenti a Supabase
- Mantieni un backup del database SQLite originale

### 6. Avvio Applicazione

```bash
# Avvia l'app
python -m src.jbkgestione.app

# Oppure usa il file di avvio
python run_app.py
```

## 👥 Gestione Utenti

### Ruoli Disponibili

#### 👑 Amministratore
- **Accesso completo** a tutte le funzioni
- Può **modificare, aggiungere, eliminare** dati
- Può gestire convocazioni e statistiche
- Accesso alle funzioni di amministrazione

#### 👤 Utente
- **Solo lettura** dei dati
- Può visualizzare statistiche e dashboard
- Non può modificare dati
- Ideale per giocatori o staff

### Aggiungere Nuovi Utenti

1. **Via Supabase Dashboard**:
   - "Authentication" > "Users" > "Add User"
   - Scegli il ruolo modificando la tabella `profiles`

2. **Via App** (futura implementazione):
   - Gli admin potranno invitare nuovi utenti
   - Sistema di registrazione controllata

## 🔒 Sicurezza

### Row Level Security (RLS)

Tutte le tabelle hanno politiche RLS che garantiscono:
- **Lettura**: Tutti gli utenti autenticati
- **Scrittura**: Solo amministratori
- **Isolamento**: I dati sono protetti a livello database

### Best Practices

1. **Password forti** per tutti gli utenti
2. **Non condividere** le credenziali API
3. **Backup regolari** del database
4. **Monitoring** degli accessi
5. **Aggiornamenti** regolari dell'app

## 📊 Funzionalità Principali

### Dashboard Home
- **Impegni settimanali** con palestre
- **Valutazione media squadra**
- **Statistiche generali**

### Gestione Giocatori
- Anagrafica completa
- Controllo accessi in base al ruolo

### Gestione Partite
- Convocazioni con sistema di rifiuto
- Statistiche individuali
- Risultati e note

### Gestione Allenamenti
- Presenze/assenze
- Calendario allenamenti
- Report presenze

### Sistema Valutazioni
- Calcolo automatico valutazioni
- Peso per presenze, convocazioni, performance
- Penalità per convocazioni rifiutate

## 🔧 Troubleshooting

### Errori Comuni

#### "Non è stato possibile risolvere l'importazione supabase"
```bash
pip install supabase python-dotenv
```

#### "Database connection failed"
- Verifica le credenziali in `.env`
- Controlla la connessione internet
- Verifica che il progetto Supabase sia attivo

#### "Accesso negato"
- Verifica di essere autenticato
- Controlla il ruolo utente nella tabella `profiles`
- Ricontrolla le politiche RLS

#### "Schema not found"
- Ricarica lo schema SQL in Supabase
- Verifica che tutte le tabelle siano create
- Controlla i log di Supabase per errori

### Log e Debug

Abilita il debug nel file `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## 📞 Supporto

- **GitHub Issues**: Per bug e richieste
- **Email**: [inserire email di supporto]
- **Documentazione**: README.md per dettagli tecnici

## 🔄 Roadmap Future

- [ ] Registrazione utenti tramite app
- [ ] Notifiche push per convocazioni
- [ ] Sync real-time tra utenti
- [ ] App mobile native
- [ ] Dashboard avanzate con grafici
- [ ] Esportazione dati (PDF, Excel)
- [ ] Sistema di messaggistica interna
- [ ] Integrazione calendario Google/Outlook

---

**© 2025 JBK Gestione - Sistema di gestione squadra basket con Supabase**