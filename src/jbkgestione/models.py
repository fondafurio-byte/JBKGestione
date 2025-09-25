"""
Modelli di dati per l'app JBK Gestione
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional


class DatabaseManager:
    """Gestisce il database SQLite per l'app"""
    
    def __init__(self, db_path: str = "jbk_gestione.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inizializza le tabelle del database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabella giocatori
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS giocatori (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cognome TEXT NOT NULL,
                anno_nascita INTEGER,
                idoneita_sportiva BOOLEAN DEFAULT 0,
                data_scadenza_idoneita TEXT,
                numero_maglia INTEGER UNIQUE,
                attivo BOOLEAN DEFAULT 1,
                data_inserimento TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabella allenamenti
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS allenamenti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                ora_inizio TEXT NOT NULL,
                ora_fine TEXT,
                luogo TEXT,
                tipo TEXT,
                descrizione TEXT,
                presenze TEXT,
                note TEXT,
                data_inserimento TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Migrazione: aggiungi colonna data_scadenza_idoneita se non esiste
        try:
            cursor.execute("ALTER TABLE giocatori ADD COLUMN data_scadenza_idoneita TEXT")
        except sqlite3.OperationalError:
            # La colonna esiste già
            pass
        
        # Migrazione: aggiungi colonna idoneita_sportiva se non esiste
        try:
            cursor.execute("ALTER TABLE giocatori ADD COLUMN idoneita_sportiva BOOLEAN DEFAULT 0")
        except sqlite3.OperationalError:
            # La colonna esiste già
            pass
        
        # Migrazione: aggiungi colonna tipologia se non esiste
        try:
            cursor.execute("ALTER TABLE partite ADD COLUMN tipologia TEXT DEFAULT 'stagione regolare'")
        except sqlite3.OperationalError:
            # La colonna esiste già
            pass
        
        # Tabella partite
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS partite (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                ora TEXT NOT NULL,
                avversario TEXT NOT NULL,
                luogo TEXT,
                in_casa BOOLEAN DEFAULT 1,
                tipologia TEXT DEFAULT 'stagione regolare',
                risultato_nostro INTEGER,
                risultato_avversario INTEGER,
                formazione TEXT,
                statistiche TEXT,
                note TEXT,
                data_inserimento TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabella statistiche giocatori
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistiche_giocatori (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                giocatore_id INTEGER,
                partita_id INTEGER,
                minuti_giocati INTEGER DEFAULT 0,
                punti INTEGER DEFAULT 0,
                palle_perse INTEGER DEFAULT 0,
                palle_recuperate INTEGER DEFAULT 0,
                stoppate INTEGER DEFAULT 0,
                rimbalzi INTEGER DEFAULT 0,
                assist INTEGER DEFAULT 0,
                valutazione INTEGER DEFAULT 0,
                plus_minus INTEGER DEFAULT 0,
                tiri_liberi_tentati INTEGER DEFAULT 0,
                tiri_liberi_segnati INTEGER DEFAULT 0,
                tiri_due_tentati INTEGER DEFAULT 0,
                tiri_due_segnati INTEGER DEFAULT 0,
                tiri_tre_tentati INTEGER DEFAULT 0,
                tiri_tre_segnati INTEGER DEFAULT 0,
                falli INTEGER DEFAULT 0,
                data_inserimento TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (giocatore_id) REFERENCES giocatori (id),
                FOREIGN KEY (partita_id) REFERENCES partite (id),
                UNIQUE(giocatore_id, partita_id)
            )
        """)
        
        # Tabella convocati
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS convocati (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                partita_id INTEGER NOT NULL,
                giocatore_id INTEGER NOT NULL,
                titolare BOOLEAN DEFAULT 0,
                rifiutata BOOLEAN DEFAULT 0,
                data_convocazione TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (partita_id) REFERENCES partite (id),
                FOREIGN KEY (giocatore_id) REFERENCES giocatori (id),
                UNIQUE(partita_id, giocatore_id)
            )
        """)
        
        # Migrazione per aggiungere campi mancanti alla tabella statistiche_giocatori
        self._migrate_statistiche_table(cursor)
        
        # Migrazione per aggiungere campo rifiutata alla tabella convocati
        self._migrate_convocati_table(cursor)
        
        conn.commit()
        conn.close()
    
    def _migrate_statistiche_table(self, cursor):
        """Migrazione per aggiungere campi mancanti alla tabella statistiche"""
        # Lista dei campi da aggiungere se non esistono
        new_columns = [
            ('palle_recuperate', 'INTEGER DEFAULT 0'),
            ('stoppate', 'INTEGER DEFAULT 0'),
            ('valutazione', 'INTEGER DEFAULT 0'),
            ('plus_minus', 'INTEGER DEFAULT 0'),
            ('data_inserimento', 'TEXT DEFAULT CURRENT_TIMESTAMP')
        ]
        
        # Verifica colonne esistenti
        cursor.execute("PRAGMA table_info(statistiche_giocatori)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        # Aggiungi colonne mancanti
        for column_name, column_def in new_columns:
            if column_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE statistiche_giocatori ADD COLUMN {column_name} {column_def}")
                except sqlite3.OperationalError:
                    pass  # Colonna già esistente o altro errore
        
        # Rinomina palle_rubate in palle_recuperate se necessario
        if 'palle_rubate' in existing_columns and 'palle_recuperate' not in existing_columns:
            try:
                cursor.execute("ALTER TABLE statistiche_giocatori ADD COLUMN palle_recuperate INTEGER DEFAULT 0")
                cursor.execute("UPDATE statistiche_giocatori SET palle_recuperate = palle_rubate")
            except sqlite3.OperationalError:
                pass
    
    def _migrate_convocati_table(self, cursor):
        """Migrazione per aggiungere campo rifiutata alla tabella convocati"""
        try:
            cursor.execute("ALTER TABLE convocati ADD COLUMN rifiutata BOOLEAN DEFAULT 0")
        except sqlite3.OperationalError:
            # La colonna esiste già
            pass


class Giocatore:
    """Modello per un giocatore"""
    
    def __init__(self, nome: str, cognome: str, numero_maglia: int = None, 
                 data_nascita: str = None, idoneita_sportiva: bool = False,
                 data_scadenza_idoneita: str = None):
        self.nome = nome
        self.cognome = cognome
        self.numero_maglia = numero_maglia
        self.data_nascita = data_nascita
        self.idoneita_sportiva = idoneita_sportiva
        self.data_scadenza_idoneita = data_scadenza_idoneita
        self.attivo = True
    
    def nome_completo(self) -> str:
        return f"{self.nome} {self.cognome}"
    
    def to_dict(self) -> Dict:
        return {
            'nome': self.nome,
            'cognome': self.cognome,
            'numero_maglia': self.numero_maglia,
            'anno_nascita': self.anno_nascita,
            'idoneita_sportiva': self.idoneita_sportiva,
            'data_scadenza_idoneita': self.data_scadenza_idoneita,
            'attivo': self.attivo
        }
    
    def is_idoneita_scaduta(self) -> bool:
        """Controlla se l'idoneità sportiva è scaduta"""
        if not self.idoneita_sportiva or not self.data_scadenza_idoneita:
            return False
        
        try:
            from datetime import datetime
            # Prova prima il formato italiano GG/MM/AAAA
            try:
                data_scadenza = datetime.strptime(self.data_scadenza_idoneita, '%d/%m/%Y')
            except ValueError:
                # Fallback al formato ISO per compatibilità
                data_scadenza = datetime.strptime(self.data_scadenza_idoneita, '%Y-%m-%d')
            return datetime.now().date() > data_scadenza.date()
        except (ValueError, TypeError):
            return False
    
    def get_stato_idoneita(self) -> str:
        """Restituisce lo stato dell'idoneità sportiva"""
        if not self.idoneita_sportiva:
            return "Non Idoneo"
        elif self.is_idoneita_scaduta():
            return "Scaduto"
        else:
            return "Idoneo"


class Partita:
    """Modello per una partita"""
    
    def __init__(self, data: str, ora: str, avversario: str, 
                 luogo: str = "", in_casa: bool = True, 
                 tipologia: str = "stagione regolare"):
        self.data = data
        self.ora = ora
        self.avversario = avversario
        self.luogo = luogo
        self.in_casa = in_casa
        self.tipologia = tipologia
        self.risultato_nostro = None
        self.risultato_avversario = None
        self.formazione = []
        self.statistiche = {}
        self.note = ""
    
    def to_dict(self) -> Dict:
        return {
            'data': self.data,
            'ora': self.ora,
            'avversario': self.avversario,
            'luogo': self.luogo,
            'in_casa': self.in_casa,
            'tipologia': self.tipologia,
            'risultato_nostro': self.risultato_nostro,
            'risultato_avversario': self.risultato_avversario,
            'formazione': json.dumps(self.formazione),
            'statistiche': json.dumps(self.statistiche),
            'note': self.note
        }


class Allenamento:
    """Modello per un allenamento"""
    
    def __init__(self, data: str, ora_inizio: str, ora_fine: str = "", 
                 luogo: str = "", tipo: str = "", descrizione: str = ""):
        self.data = data
        self.ora_inizio = ora_inizio
        self.ora_fine = ora_fine
        self.luogo = luogo
        self.tipo = tipo
        self.descrizione = descrizione
        self.presenze = []
        self.note = ""
    
    def to_dict(self) -> Dict:
        return {
            'data': self.data,
            'ora_inizio': self.ora_inizio,
            'ora_fine': self.ora_fine,
            'luogo': self.luogo,
            'tipo': self.tipo,
            'descrizione': self.descrizione,
            'presenze': json.dumps(self.presenze),
            'note': self.note
        }


class StatisticheGiocatore:
    """Modello per le statistiche di un giocatore in una partita"""
    
    def __init__(self, giocatore_id: int, partita_id: int):
        self.giocatore_id = giocatore_id
        self.partita_id = partita_id
        self.minuti_giocati = 0
        self.punti = 0
        self.rimbalzi = 0
        self.assist = 0
        self.palle_rubate = 0
        self.palle_perse = 0
        self.falli = 0
        self.tiri_liberi_tentati = 0
        self.tiri_liberi_segnati = 0
        self.tiri_due_tentati = 0
        self.tiri_due_segnati = 0
        self.tiri_tre_tentati = 0
        self.tiri_tre_segnati = 0
    
    def percentuale_tiri_liberi(self) -> float:
        if self.tiri_liberi_tentati == 0:
            return 0.0
        return (self.tiri_liberi_segnati / self.tiri_liberi_tentati) * 100
    
    def percentuale_tiri_due(self) -> float:
        if self.tiri_due_tentati == 0:
            return 0.0
        return (self.tiri_due_segnati / self.tiri_due_tentati) * 100
    
    def percentuale_tiri_tre(self) -> float:
        if self.tiri_tre_tentati == 0:
            return 0.0
        return (self.tiri_tre_segnati / self.tiri_tre_tentati) * 100
    
    def to_dict(self) -> Dict:
        return {
            'giocatore_id': self.giocatore_id,
            'partita_id': self.partita_id,
            'minuti_giocati': self.minuti_giocati,
            'punti': self.punti,
            'rimbalzi': self.rimbalzi,
            'assist': self.assist,
            'palle_rubate': self.palle_rubate,
            'palle_perse': self.palle_perse,
            'falli': self.falli,
            'tiri_liberi_tentati': self.tiri_liberi_tentati,
            'tiri_liberi_segnati': self.tiri_liberi_segnati,
            'tiri_due_tentati': self.tiri_due_tentati,
            'tiri_due_segnati': self.tiri_due_segnati,
            'tiri_tre_tentati': self.tiri_tre_tentati,
            'tiri_tre_segnati': self.tiri_tre_segnati
        }