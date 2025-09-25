"""
Database Manager per Supabase
Sostituisce il vecchio SQLite con Supabase PostgreSQL
"""

import os
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from .supabase_auth import auth_service

class SupabaseDBManager:
    def __init__(self):
        # Configurazione Supabase
        self.supabase_url = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY", "your-anon-key-here")
        
        # Inizializza il client Supabase
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
    def check_permissions(self, operation: str = "read") -> bool:
        """
        Controlla i permessi per l'operazione richiesta
        read: tutti gli utenti autenticati
        write: solo amministratori
        """
        if not auth_service.is_authenticated():
            return False
            
        if operation == "read":
            return True  # Tutti gli utenti autenticati possono leggere
        elif operation == "write":
            return auth_service.is_admin()  # Solo admin possono scrivere
        
        return False
    
    # ========================================
    # METODI PER GIOCATORI
    # ========================================
    
    def ottieni_tutti_giocatori(self) -> List[Dict[str, Any]]:
        """Ottiene tutti i giocatori"""
        if not self.check_permissions("read"):
            return []
            
        try:
            response = self.supabase.table("giocatori").select("*").eq("attivo", True).order("cognome").execute()
            return response.data or []
        except Exception as e:
            print(f"Errore nel recupero giocatori: {str(e)}")
            return []
    
    def aggiungi_giocatore(self, dati_giocatore: Dict[str, Any]) -> bool:
        """Aggiunge un nuovo giocatore"""
        if not self.check_permissions("write"):
            print("Permessi insufficienti per aggiungere giocatori")
            return False
            
        try:
            response = self.supabase.table("giocatori").insert(dati_giocatore).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Errore nell'aggiunta giocatore: {str(e)}")
            return False
    
    def aggiorna_giocatore(self, giocatore_id: int, dati_giocatore: Dict[str, Any]) -> bool:
        """Aggiorna un giocatore esistente"""
        if not self.check_permissions("write"):
            print("Permessi insufficienti per modificare giocatori")
            return False
            
        try:
            response = self.supabase.table("giocatori").update(dati_giocatore).eq("id", giocatore_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Errore nell'aggiornamento giocatore: {str(e)}")
            return False
    
    def elimina_giocatore(self, giocatore_id: int) -> bool:
        """Elimina (disattiva) un giocatore"""
        if not self.check_permissions("write"):
            print("Permessi insufficienti per eliminare giocatori")
            return False
            
        try:
            # Soft delete: imposta attivo = False
            response = self.supabase.table("giocatori").update({"attivo": False}).eq("id", giocatore_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Errore nell'eliminazione giocatore: {str(e)}")
            return False
    
    # ========================================
    # METODI PER ALLENAMENTI
    # ========================================
    
    def ottieni_tutti_allenamenti(self) -> List[Dict[str, Any]]:
        """Ottiene tutti gli allenamenti"""
        if not self.check_permissions("read"):
            return []
            
        try:
            response = self.supabase.table("allenamenti").select("*").order("data", desc=True).execute()
            return response.data or []
        except Exception as e:
            print(f"Errore nel recupero allenamenti: {str(e)}")
            return []
    
    def aggiungi_allenamento(self, dati_allenamento: Dict[str, Any]) -> bool:
        """Aggiunge un nuovo allenamento"""
        if not self.check_permissions("write"):
            print("Permessi insufficienti per aggiungere allenamenti")
            return False
            
        try:
            response = self.supabase.table("allenamenti").insert(dati_allenamento).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Errore nell'aggiunta allenamento: {str(e)}")
            return False
    
    def aggiorna_allenamento(self, allenamento_id: int, dati_allenamento: Dict[str, Any]) -> bool:
        """Aggiorna un allenamento esistente"""
        if not self.check_permissions("write"):
            print("Permessi insufficienti per modificare allenamenti")
            return False
            
        try:
            response = self.supabase.table("allenamenti").update(dati_allenamento).eq("id", allenamento_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Errore nell'aggiornamento allenamento: {str(e)}")
            return False
    
    def elimina_allenamento(self, allenamento_id: int) -> bool:
        """Elimina un allenamento"""
        if not self.check_permissions("write"):
            print("Permessi insufficienti per eliminare allenamenti")
            return False
            
        try:
            response = self.supabase.table("allenamenti").delete().eq("id", allenamento_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Errore nell'eliminazione allenamento: {str(e)}")
            return False
    
    # ========================================
    # METODI PER PARTITE
    # ========================================
    
    def ottieni_tutte_partite(self) -> List[Dict[str, Any]]:
        """Ottiene tutte le partite"""
        if not self.check_permissions("read"):
            return []
            
        try:
            response = self.supabase.table("partite").select("*").order("data", desc=True).execute()
            return response.data or []
        except Exception as e:
            print(f"Errore nel recupero partite: {str(e)}")
            return []
    
    def aggiungi_partita(self, dati_partita: Dict[str, Any]) -> Optional[int]:
        """Aggiunge una nuova partita e ritorna l'ID"""
        if not self.check_permissions("write"):
            print("Permessi insufficienti per aggiungere partite")
            return None
            
        try:
            response = self.supabase.table("partite").insert(dati_partita).execute()
            if response.data:
                return response.data[0]['id']
            return None
        except Exception as e:
            print(f"Errore nell'aggiunta partita: {str(e)}")
            return None
    
    def aggiorna_partita(self, partita_id: int, dati_partita: Dict[str, Any]) -> bool:
        """Aggiorna una partita esistente"""
        if not self.check_permissions("write"):
            print("Permessi insufficienti per modificare partite")
            return False
            
        try:
            response = self.supabase.table("partite").update(dati_partita).eq("id", partita_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Errore nell'aggiornamento partita: {str(e)}")
            return False
    
    def elimina_partita(self, partita_id: int) -> bool:
        """Elimina una partita"""
        if not self.check_permissions("write"):
            print("Permessi insufficienti per eliminare partite")
            return False
            
        try:
            response = self.supabase.table("partite").delete().eq("id", partita_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Errore nell'eliminazione partita: {str(e)}")
            return False
    
    # ========================================
    # METODI PER CONVOCATI
    # ========================================
    
    def ottieni_convocati_partita(self, partita_id: int) -> List[Dict[str, Any]]:
        """Ottiene i convocati per una partita"""
        if not self.check_permissions("read"):
            return []
            
        try:
            response = self.supabase.table("convocati").select("""
                *,
                giocatori (
                    id,
                    nome,
                    cognome,
                    numero_maglia
                )
            """).eq("partita_id", partita_id).execute()
            return response.data or []
        except Exception as e:
            print(f"Errore nel recupero convocati: {str(e)}")
            return []
    
    def aggiorna_convocazione(self, partita_id: int, giocatore_id: int, dati_convocazione: Dict[str, Any]) -> bool:
        """Aggiorna o inserisce una convocazione"""
        if not self.check_permissions("write"):
            print("Permessi insufficienti per modificare convocazioni")
            return False
            
        try:
            # Upsert: aggiorna se esiste, inserisce se non esiste
            dati_convocazione.update({
                "partita_id": partita_id,
                "giocatore_id": giocatore_id
            })
            
            response = self.supabase.table("convocati").upsert(dati_convocazione).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Errore nell'aggiornamento convocazione: {str(e)}")
            return False
    
    # ========================================
    # METODI PER STATISTICHE
    # ========================================
    
    def ottieni_statistiche_partita(self, partita_id: int) -> List[Dict[str, Any]]:
        """Ottiene le statistiche di una partita"""
        if not self.check_permissions("read"):
            return []
            
        try:
            response = self.supabase.table("statistiche_giocatori").select("""
                *,
                giocatori (
                    id,
                    nome,
                    cognome,
                    numero_maglia
                )
            """).eq("partita_id", partita_id).execute()
            return response.data or []
        except Exception as e:
            print(f"Errore nel recupero statistiche: {str(e)}")
            return []
    
    def aggiorna_statistiche_giocatore(self, partita_id: int, giocatore_id: int, dati_statistiche: Dict[str, Any]) -> bool:
        """Aggiorna o inserisce le statistiche di un giocatore"""
        if not self.check_permissions("write"):
            print("Permessi insufficienti per modificare statistiche")
            return False
            
        try:
            dati_statistiche.update({
                "partita_id": partita_id,
                "giocatore_id": giocatore_id
            })
            
            response = self.supabase.table("statistiche_giocatori").upsert(dati_statistiche).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Errore nell'aggiornamento statistiche: {str(e)}")
            return False
    
    def ottieni_tutte_statistiche_giocatore(self, giocatore_id: int) -> List[Dict[str, Any]]:
        """Ottiene tutte le statistiche di un giocatore"""
        if not self.check_permissions("read"):
            return []
            
        try:
            response = self.supabase.table("statistiche_giocatori").select("""
                *,
                partite (
                    id,
                    data,
                    avversario,
                    risultato_nostro,
                    risultato_avversario
                )
            """).eq("giocatore_id", giocatore_id).order("partite(data)", desc=True).execute()
            return response.data or []
        except Exception as e:
            print(f"Errore nel recupero statistiche giocatore: {str(e)}")
            return []

# Istanza globale del database manager
db_manager = SupabaseDBManager()