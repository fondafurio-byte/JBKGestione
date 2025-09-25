"""
Servizi per la gestione dei dati dell'app JBK Gestione
"""

import sqlite3
import json
from typing import List, Optional, Dict
from .models import DatabaseManager, Giocatore, Partita, Allenamento, StatisticheGiocatore


class GiocatoriService:
    """Servizio per la gestione dei giocatori"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def aggiungi_giocatore(self, giocatore: Giocatore) -> bool:
        """Aggiunge un nuovo giocatore al database"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO giocatori 
                (nome, cognome, numero_maglia, data_nascita, idoneita_sportiva, data_scadenza_idoneita, attivo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                giocatore.nome, giocatore.cognome, giocatore.numero_maglia,
                giocatore.data_nascita, giocatore.idoneita_sportiva, 
                giocatore.data_scadenza_idoneita, giocatore.attivo
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nell'aggiunta del giocatore: {e}")
            return False
    
    def ottieni_tutti_giocatori(self) -> List[Dict]:
        """Ottiene tutti i giocatori dal database"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM giocatori WHERE attivo = 1 ORDER BY numero_maglia")
        rows = cursor.fetchall()
        
        giocatori = []
        for row in rows:
            giocatore = {
                'id': row[0],
                'nome': row[1],
                'cognome': row[2],
                'numero_maglia': row[3],
                'posizione': row[4],
                'data_nascita': row[5],
                'altezza': row[6],
                'peso': row[7],
                'telefono': row[8],
                'email': row[9],
                'indirizzo': row[10],
                'attivo': row[11],
                'data_inserimento': row[12],
                'data_scadenza_idoneita': row[13],
                'idoneita_sportiva': row[14] if len(row) > 14 else False  # Colonna aggiunta dopo
            }
            giocatori.append(giocatore)
        
        conn.close()
        return giocatori
    
    def ottieni_giocatore_per_id(self, giocatore_id: int) -> Optional[Dict]:
        """Ottiene un giocatore specifico per ID"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM giocatori WHERE id = ?", (giocatore_id,))
        row = cursor.fetchone()
        
        if row:
            giocatore = {
                'id': row[0],
                'nome': row[1],
                'cognome': row[2],
                'numero_maglia': row[3],
                'posizione': row[4],
                'data_nascita': row[5],
                'altezza': row[6],
                'peso': row[7],
                'telefono': row[8],
                'email': row[9],
                'indirizzo': row[10],
                'attivo': row[11],
                'data_inserimento': row[12],
                'data_scadenza_idoneita': row[13],
                'idoneita_sportiva': row[14] if len(row) > 14 else False
            }
            conn.close()
            return giocatore
        
        conn.close()
        return None
    
    def aggiorna_giocatore(self, giocatore_id: int, dati: Dict) -> bool:
        """Aggiorna i dati di un giocatore"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE giocatori SET
                nome = ?, cognome = ?, numero_maglia = ?, posizione = ?,
                data_nascita = ?, altezza = ?, peso = ?, telefono = ?,
                email = ?, indirizzo = ?
                WHERE id = ?
            """, (
                dati['nome'], dati['cognome'], dati['numero_maglia'],
                dati['posizione'], dati['data_nascita'], dati['altezza'],
                dati['peso'], dati['telefono'], dati['email'],
                dati['indirizzo'], giocatore_id
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nell'aggiornamento del giocatore: {e}")
            return False
    
    def elimina_giocatore(self, giocatore_id: int) -> bool:
        """Disattiva un giocatore (soft delete)"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE giocatori SET attivo = 0 WHERE id = ?", (giocatore_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nell'eliminazione del giocatore: {e}")
            return False
    
    def create(self, data: Dict) -> bool:
        """Crea un nuovo giocatore da dizionario"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO giocatori 
                (nome, cognome, numero_maglia, data_nascita, idoneita_sportiva, data_scadenza_idoneita, attivo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('nome', ''),
                data.get('cognome', ''),
                data.get('numero_maglia'),
                data.get('data_nascita'),
                data.get('idoneita_sportiva', False),
                data.get('data_scadenza_idoneita'),
                data.get('attivo', True)
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nella creazione del giocatore: {e}")
            return False
    
    def get_all(self) -> List[Dict]:
        """Ottiene tutti i giocatori"""
        return self.ottieni_tutti_giocatori()
    
    def get_by_id(self, id: int) -> Optional[Dict]:
        """Ottiene un giocatore per ID"""
        return self.ottieni_giocatore_per_id(id)
    
    def update(self, id: int, data: Dict) -> bool:
        """Aggiorna un giocatore"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE giocatori 
                SET nome = ?, cognome = ?, numero_maglia = ?, 
                    data_nascita = ?, idoneita_sportiva = ?, data_scadenza_idoneita = ?
                WHERE id = ?
            """, (
                data.get('nome', ''),
                data.get('cognome', ''),
                data.get('numero_maglia'),
                data.get('data_nascita'),
                data.get('idoneita_sportiva', False),
                data.get('data_scadenza_idoneita'),
                id
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nell'aggiornamento del giocatore: {e}")
            return False
    
    def delete(self, id: int) -> bool:
        """Elimina un giocatore (soft delete)"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE giocatori SET attivo = 0 WHERE id = ?", (id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nell'eliminazione del giocatore: {e}")
            return False


class PartiteService:
    """Servizio per la gestione delle partite"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def aggiungi_partita(self, partita: Partita) -> bool:
        """Aggiunge una nuova partita al database"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO partite 
                (data, ora, avversario, luogo, in_casa, tipologia, risultato_nostro,
                 risultato_avversario, formazione, statistiche, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                partita.data, partita.ora, partita.avversario, partita.luogo,
                partita.in_casa, partita.tipologia, partita.risultato_nostro, partita.risultato_avversario,
                json.dumps(partita.formazione), json.dumps(partita.statistiche), partita.note
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nell'aggiunta della partita: {e}")
            return False
    
    def ottieni_tutte_partite(self) -> List[Dict]:
        """Ottiene tutte le partite dal database"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM partite ORDER BY data DESC, ora DESC")
        rows = cursor.fetchall()
        
        partite = []
        for row in rows:
            partita = {
                'id': row[0],
                'data': row[1],
                'ora': row[2],
                'avversario': row[3],
                'luogo': row[4],
                'in_casa': row[5],
                'risultato_nostro': row[6] if len(row) > 6 else None,
                'risultato_avversario': row[7] if len(row) > 7 else None,
                'formazione': json.loads(row[8]) if len(row) > 8 and row[8] else [],
                'statistiche': json.loads(row[9]) if len(row) > 9 and row[9] else {},
                'note': row[10] if len(row) > 10 else '',
                'tipologia': row[12] if len(row) > 12 and row[12] else 'stagione regolare'
            }
            partite.append(partita)
        
        conn.close()
        return partite
    
    def aggiorna_partita(self, partita_id: int, partita: Partita) -> bool:
        """Aggiorna una partita esistente nel database"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE partite 
                SET data=?, ora=?, avversario=?, luogo=?, in_casa=?, tipologia=?, 
                    risultato_nostro=?, risultato_avversario=?, formazione=?, 
                    statistiche=?, note=?
                WHERE id=?
            """, (
                partita.data, partita.ora, partita.avversario, partita.luogo,
                partita.in_casa, partita.tipologia, partita.risultato_nostro, 
                partita.risultato_avversario, json.dumps(partita.formazione), 
                json.dumps(partita.statistiche), partita.note, partita_id
            ))
            
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Errore nell'aggiornamento della partita: {e}")
            return False
    
    def ottieni_partita_per_id(self, partita_id: int) -> Dict:
        """Ottiene una partita specifica per ID"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM partite WHERE id = ?", (partita_id,))
            row = cursor.fetchone()
            
            if row:
                partita = {
                    'id': row[0],
                    'data': row[1],
                    'ora': row[2],
                    'avversario': row[3],
                    'luogo': row[4],
                    'in_casa': row[5],
                    'risultato_nostro': row[6] if len(row) > 6 else None,
                    'risultato_avversario': row[7] if len(row) > 7 else None,
                    'formazione': json.loads(row[8]) if len(row) > 8 and row[8] else [],
                    'statistiche': json.loads(row[9]) if len(row) > 9 and row[9] else {},
                    'note': row[10] if len(row) > 10 else '',
                    'tipologia': row[12] if len(row) > 12 and row[12] else 'stagione regolare'
                }
                conn.close()
                return partita
            
            conn.close()
            return None
        except Exception as e:
            print(f"Errore nel recupero della partita: {e}")
            return None
    
    def ottieni_partite_per_tipologia(self, tipologia: str) -> List[Dict]:
        """Ottiene le partite filtrate per tipologia"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM partite WHERE tipologia = ? ORDER BY data DESC, ora DESC", (tipologia,))
        rows = cursor.fetchall()
        
        partite = []
        for row in rows:
            partita = {
                'id': row[0],
                'data': row[1],
                'ora': row[2],
                'avversario': row[3],
                'luogo': row[4],
                'in_casa': row[5],
                'risultato_nostro': row[6] if len(row) > 6 else None,
                'risultato_avversario': row[7] if len(row) > 7 else None,
                'formazione': json.loads(row[8]) if len(row) > 8 and row[8] else [],
                'statistiche': json.loads(row[9]) if len(row) > 9 and row[9] else {},
                'note': row[10] if len(row) > 10 else '',
                'tipologia': row[12] if len(row) > 12 and row[12] else 'stagione regolare'
            }
            partite.append(partita)
        
        conn.close()
        return partite


class AllenamentiService:
    """Servizio per la gestione degli allenamenti"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def aggiungi_allenamento(self, allenamento: Allenamento) -> bool:
        """Aggiunge un nuovo allenamento al database"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO allenamenti 
                (data, ora_inizio, ora_fine, luogo, tipo, descrizione, presenze, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                allenamento.data, allenamento.ora_inizio, allenamento.ora_fine,
                allenamento.luogo, allenamento.tipo, allenamento.descrizione,
                json.dumps(allenamento.presenze), allenamento.note
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nell'aggiunta dell'allenamento: {e}")
            return False
    
    def ottieni_tutti_allenamenti(self) -> List[Dict]:
        """Ottiene tutti gli allenamenti dal database"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM allenamenti ORDER BY data DESC, ora_inizio DESC")
        rows = cursor.fetchall()
        
        allenamenti = []
        for row in rows:
            allenamento = {
                'id': row[0],
                'data': row[1],
                'ora_inizio': row[2],
                'ora_fine': row[3],
                'luogo': row[4],
                'tipo': row[5],
                'descrizione': row[6],
                'presenze': json.loads(row[7]) if row[7] else [],
                'note': row[8]
            }
            allenamenti.append(allenamento)
        
        conn.close()
        return allenamenti
    
    def ottieni_allenamenti_per_data(self, data: str) -> List[Dict]:
        """Ottiene gli allenamenti per una data specifica"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM allenamenti WHERE data = ? ORDER BY ora_inizio", (data,))
        rows = cursor.fetchall()
        
        allenamenti = []
        for row in rows:
            allenamento = {
                'id': row[0],
                'data': row[1],
                'ora_inizio': row[2],
                'ora_fine': row[3],
                'luogo': row[4],
                'tipo': row[5],
                'descrizione': row[6],
                'presenze': json.loads(row[7]) if row[7] else [],
                'note': row[8]
            }
            allenamenti.append(allenamento)
        
        conn.close()
        return allenamenti


class StatisticheService:
    """Servizio per la gestione delle statistiche"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def aggiungi_statistiche_giocatore(self, stats: StatisticheGiocatore) -> bool:
        """Aggiunge le statistiche di un giocatore per una partita"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO statistiche_giocatori 
                (giocatore_id, partita_id, minuti_giocati, punti, rimbalzi, assist,
                 palle_rubate, palle_perse, falli, tiri_liberi_tentati, tiri_liberi_segnati,
                 tiri_due_tentati, tiri_due_segnati, tiri_tre_tentati, tiri_tre_segnati)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                stats.giocatore_id, stats.partita_id, stats.minuti_giocati,
                stats.punti, stats.rimbalzi, stats.assist, stats.palle_rubate,
                stats.palle_perse, stats.falli, stats.tiri_liberi_tentati,
                stats.tiri_liberi_segnati, stats.tiri_due_tentati, stats.tiri_due_segnati,
                stats.tiri_tre_tentati, stats.tiri_tre_segnati
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nell'aggiunta delle statistiche: {e}")
            return False
    
    def ottieni_statistiche_giocatore(self, giocatore_id: int) -> List[Dict]:
        """Ottiene tutte le statistiche di un giocatore"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.*, p.data, p.avversario 
            FROM statistiche_giocatori s
            JOIN partite p ON s.partita_id = p.id
            WHERE s.giocatore_id = ?
            ORDER BY p.data DESC
        """, (giocatore_id,))
        
        rows = cursor.fetchall()
        
        statistiche = []
        for row in rows:
            stat = {
                'id': row[0],
                'giocatore_id': row[1],
                'partita_id': row[2],
                'minuti_giocati': row[3],
                'punti': row[4],
                'rimbalzi': row[5],
                'assist': row[6],
                'palle_rubate': row[7],
                'palle_perse': row[8],
                'falli': row[9],
                'tiri_liberi_tentati': row[10],
                'tiri_liberi_segnati': row[11],
                'tiri_due_tentati': row[12],
                'tiri_due_segnati': row[13],
                'tiri_tre_tentati': row[14],
                'tiri_tre_segnati': row[15],
                'data_partita': row[16],
                'avversario': row[17]
            }
            statistiche.append(stat)
        
        conn.close()
        return statistiche


class ConvocatiService:
    """Servizio per la gestione dei convocati"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def ottieni_convocati_partita(self, partita_id: int) -> List[Dict]:
        """Ottiene i convocati per una partita specifica"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.id, c.partita_id, c.giocatore_id, c.titolare, c.rifiutata, c.data_convocazione,
                   g.nome, g.cognome, g.numero_maglia
            FROM convocati c
            JOIN giocatori g ON c.giocatore_id = g.id
            WHERE c.partita_id = ?
            ORDER BY c.titolare DESC, g.numero_maglia
        """, (partita_id,))
        
        rows = cursor.fetchall()
        
        convocati = []
        for row in rows:
            convocato = {
                'id': row[0],
                'partita_id': row[1],
                'giocatore_id': row[2],
                'titolare': bool(row[3]),
                'rifiutata': bool(row[4]),
                'data_convocazione': row[5],
                'nome': row[6],
                'cognome': row[7],
                'numero_maglia': row[8]
            }
            convocati.append(convocato)
        
        conn.close()
        return convocati
    
    def aggiungi_convocato(self, partita_id: int, giocatore_id: int, titolare: bool = False, rifiutata: bool = False) -> bool:
        """Aggiunge un giocatore ai convocati di una partita"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO convocati (partita_id, giocatore_id, titolare, rifiutata)
                VALUES (?, ?, ?, ?)
            """, (partita_id, giocatore_id, titolare, rifiutata))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nell'aggiunta del convocato: {e}")
            return False
    
    def rimuovi_convocato(self, partita_id: int, giocatore_id: int) -> bool:
        """Rimuove un giocatore dai convocati di una partita"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM convocati 
                WHERE partita_id = ? AND giocatore_id = ?
            """, (partita_id, giocatore_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nella rimozione del convocato: {e}")
            return False
    
    def aggiorna_convocati_partita(self, partita_id: int, giocatori_convocati: List[Dict]) -> bool:
        """Aggiorna tutti i convocati per una partita"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            # Rimuovi tutti i convocati esistenti per questa partita
            cursor.execute("DELETE FROM convocati WHERE partita_id = ?", (partita_id,))
            
            # Aggiungi i nuovi convocati
            for giocatore in giocatori_convocati:
                cursor.execute("""
                    INSERT INTO convocati (partita_id, giocatore_id, titolare, rifiutata)
                    VALUES (?, ?, ?, ?)
                """, (partita_id, giocatore['id'], giocatore.get('titolare', False), giocatore.get('rifiutata', False)))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nell'aggiornamento dei convocati: {e}")
            return False
    
    def conta_convocati_partita(self, partita_id: int) -> int:
        """Conta il numero di convocati per una partita"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM convocati WHERE partita_id = ?", (partita_id,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def aggiorna_stato_rifiutata(self, partita_id: int, giocatore_id: int, rifiutata: bool) -> bool:
        """Aggiorna lo stato rifiutata di una convocazione"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE convocati 
                SET rifiutata = ?
                WHERE partita_id = ? AND giocatore_id = ?
            """, (rifiutata, partita_id, giocatore_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nell'aggiornamento stato rifiutata: {e}")
            return False


class StatisticheIndividualiService:
    """Servizio per la gestione delle statistiche individuali dei giocatori"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def ottieni_statistiche_partita(self, partita_id: int) -> List[Dict]:
        """Ottiene tutte le statistiche per una partita"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT sg.*, g.nome, g.cognome, g.numero_maglia
            FROM statistiche_giocatori sg
            JOIN giocatori g ON sg.giocatore_id = g.id
            WHERE sg.partita_id = ?
            ORDER BY g.numero_maglia
        """, (partita_id,))
        
        rows = cursor.fetchall()
        statistiche = []
        
        for row in rows:
            # Gestione dinamica dei campi per compatibilità
            columns = [desc[0] for desc in cursor.description]
            row_dict = dict(zip(columns, row))
            
            statistica = {
                'id': row_dict.get('id', 0),
                'giocatore_id': row_dict.get('giocatore_id', 0),
                'partita_id': row_dict.get('partita_id', 0),
                'minuti_giocati': row_dict.get('minuti_giocati', 0),
                'punti': row_dict.get('punti', 0),
                'palle_perse': row_dict.get('palle_perse', 0),
                'palle_recuperate': row_dict.get('palle_recuperate', row_dict.get('palle_rubate', 0)),
                'stoppate': row_dict.get('stoppate', 0),
                'rimbalzi': row_dict.get('rimbalzi', 0),
                'assist': row_dict.get('assist', 0),
                'valutazione': row_dict.get('valutazione', 0),
                'plus_minus': row_dict.get('plus_minus', 0),
                'nome': row_dict.get('nome', ''),
                'cognome': row_dict.get('cognome', ''),
                'numero_maglia': row_dict.get('numero_maglia', 0)
            }
            statistiche.append(statistica)
        
        conn.close()
        return statistiche
    
    def salva_statistica_giocatore(self, partita_id: int, giocatore_id: int, stats: Dict) -> bool:
        """Salva o aggiorna le statistiche di un giocatore per una partita"""
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            # Controlla se già esistono statistiche per questo giocatore in questa partita
            cursor.execute("""
                SELECT id FROM statistiche_giocatori 
                WHERE giocatore_id = ? AND partita_id = ?
            """, (giocatore_id, partita_id))
            
            existing = cursor.fetchone()
            
            if existing:
                # Aggiorna statistiche esistenti
                cursor.execute("""
                    UPDATE statistiche_giocatori SET
                        punti = ?, palle_perse = ?, palle_recuperate = ?, 
                        stoppate = ?, rimbalzi = ?, assist = ?, 
                        valutazione = ?, plus_minus = ?
                    WHERE giocatore_id = ? AND partita_id = ?
                """, (
                    stats.get('punti', 0), stats.get('palle_perse', 0),
                    stats.get('palle_recuperate', 0), stats.get('stoppate', 0),
                    stats.get('rimbalzi', 0), stats.get('assist', 0),
                    stats.get('valutazione', 0), stats.get('plus_minus', 0),
                    giocatore_id, partita_id
                ))
            else:
                # Inserisci nuove statistiche
                cursor.execute("""
                    INSERT INTO statistiche_giocatori 
                    (giocatore_id, partita_id, punti, palle_perse, palle_recuperate, 
                     stoppate, rimbalzi, assist, valutazione, plus_minus)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    giocatore_id, partita_id, stats.get('punti', 0), 
                    stats.get('palle_perse', 0), stats.get('palle_recuperate', 0),
                    stats.get('stoppate', 0), stats.get('rimbalzi', 0), 
                    stats.get('assist', 0), stats.get('valutazione', 0),
                    stats.get('plus_minus', 0)
                ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Errore nel salvataggio statistiche: {e}")
            return False
    
    def ottieni_convocati_partita(self, partita_id: int) -> List[Dict]:
        """Ottiene i giocatori convocati per una partita"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT g.id, g.nome, g.cognome, g.numero_maglia
            FROM convocati c
            JOIN giocatori g ON c.giocatore_id = g.id
            WHERE c.partita_id = ?
            ORDER BY g.numero_maglia
        """, (partita_id,))
        
        rows = cursor.fetchall()
        convocati = []
        
        for row in rows:
            convocato = {
                'id': row[0],
                'nome': row[1],
                'cognome': row[2],
                'numero_maglia': row[3]
            }
            convocati.append(convocato)
        
        conn.close()
        return convocati