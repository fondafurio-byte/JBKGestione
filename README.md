# 🏀 JBK GESTIONE

Sistema completo di gestione squadra basket con autenticazione cloud e doppio livello di accesso.

## ✨ Caratteristiche Principali

- 🔐 **Autenticazione Sicura** con Supabase
- 👥 **Due Livelli di Accesso**: Amministratore e Utente
- 📊 **Dashboard Completa** con statistiche e impegni
- 🏀 **Gestione Giocatori** con anagrafica e valutazioni
- 📅 **Calendario Partite** e allenamenti
- 📈 **Sistema Valutazioni** automatico con pesi configurabili
- 🏟️ **Gestione Palestre** e sedi
- ☁️ **Database Cloud** PostgreSQL con backup automatico
- 🔒 **Row Level Security** per protezione dati

## 🚀 Tecnologie Utilizzate

- **Python 3.8+**
- **BeeWare/Toga**: Framework per app native cross-platform
- **Supabase**: Database PostgreSQL cloud con autenticazione
- **Row Level Security**: Protezione dati a livello database
- **JWT Authentication**: Sistema di autenticazione sicuro

## 📱 Requisiti

- Python 3.8 o superiore
- Briefcase per il packaging
- Per iOS: Xcode e Apple Developer Account
- Per Android: Android SDK

## 🛠️ Installazione e Setup

### 1. Clona il repository
```bash
git clone <repository-url>
cd "JBK GESTIONE"
```

### 2. Crea un ambiente virtuale
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# oppure
source .venv/bin/activate  # macOS/Linux
```

### 3. Installa le dipendenze
```bash
pip install briefcase toga requests
```

### 4. Esegui l'app

#### Opzione A: Con Briefcase (raccomandato)
```bash
briefcase dev
```

#### Opzione B: Direttamente con Python
```bash
python run_app.py
```

#### Opzione C: Come modulo
```bash
python src/jbkgestione/__main__.py
```

## 📦 Build e Distribuzione

### Per Desktop (Windows/macOS/Linux)
```bash
briefcase create
briefcase build
briefcase package
```

### Per iOS
```bash
briefcase create iOS
briefcase build iOS
briefcase run iOS
```

### Per Android
```bash
briefcase create android
briefcase build android
briefcase run android
```

## 🗂️ Struttura del Progetto

```
JBK GESTIONE/
├── pyproject.toml          # Configurazione del progetto e BeeWare
├── README.md               # Documentazione
├── src/
│   └── jbkgestione/
│       ├── __main__.py     # Entry point dell'applicazione
│       ├── app.py          # Applicazione principale Toga
│       ├── models.py       # Modelli di dati e database
│       └── services.py     # Servizi per la gestione dei dati
├── resources/              # Risorse dell'app (icone, immagini)
└── tests/                  # Test unitari
```

## 💾 Database

L'app utilizza SQLite per memorizzare:

- **Giocatori**: Anagrafica, dati fisici, contatti
- **Partite**: Date, avversari, risultati, formazioni
- **Allenamenti**: Programmazione e presenze
- **Statistiche**: Performance individuali per partita

## 🎯 Funzionalità Principali

### 🪟 **Sistema Multi-Finestra**
- **Finestra principale** con menu di navigazione  
- **Finestre separate** per ogni sezione
- **Gestione intelligente** delle finestre (evita duplicati)
- **Interfaccia moderna** con colori tematici

### 👥 **Gestione Giocatori** (✅ Completata)
- ➕ Aggiunta/modifica/eliminazione giocatori
- 📝 Form completo con validazione
- 📋 Lista giocatori ordinata per numero maglia
- 💾 Persistenza automatica su database SQLite
- 🪟 Finestra dedicata ridimensionabile

### 🏀 **Gestione Partite** (🚧 In Sviluppo)
- 📅 Programmazione partite
- 📊 Inserimento risultati
- 👕 Gestione formazioni
- 📈 Statistiche di partita
- 🗓️ Calendario partite

### 💪 **Gestione Allenamenti** (🚧 In Sviluppo)
- 📋 Pianificazione allenamenti
- ✅ Tracciamento presenze
- 🏃‍♂️ Gestione esercizi
- 📝 Note e obiettivi
- 🗓️ Calendario allenamenti

### 📊 **Statistiche** (🚧 In Sviluppo)
- 🏆 Statistiche individuali giocatori
- 👥 Statistiche di squadra
- 📈 Grafici e analisi performance
- 🔄 Confronti e trend
- 📄 Export dati e report

## 🎨 Personalizzazione

### Colori del tema
- Primario: #1f4e79 (Blu JBK)
- Giocatori: #2e7d32 (Verde)
- Partite: #d32f2f (Rosso)
- Allenamenti: #f57c00 (Arancione)
- Statistiche: #7b1fa2 (Viola)

### Icone
L'app utilizza emoji per un'interfaccia moderna e cross-platform:
- 👥 Giocatori
- 🏀 Partite
- 💪 Allenamenti
- 📊 Statistiche

## 🧪 Test

Esegui i test con:
```bash
python -m pytest tests/
```

## 📄 Licenza

BSD License - Vedi file LICENSE per i dettagli.

## 👥 Contributi

I contributi sono benvenuti! Per favore:

1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Committa le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Pusha il branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 🆘 Supporto

Per supporto e domande, apri un issue nel repository GitHub.

## 🔄 Roadmap

- [x] Setup base BeeWare
- [x] Gestione giocatori base
- [ ] Gestione partite completa
- [ ] Gestione allenamenti
- [ ] Statistiche avanzate
- [ ] Export/Import dati
- [ ] Sincronizzazione cloud
- [ ] Notifiche push
- [ ] Modalità offline avanzata