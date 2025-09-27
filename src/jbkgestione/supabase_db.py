"""
Database Manager per Supabase
Sostituisce il vecchio SQLite con Supabase PostgreSQL
"""

import os
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from jbkgestione.supabase_auth import auth_service

class SupabaseDBManager:
    def ottieni_allenamenti_per_categorie(self, categorie: list) -> list:
        """Ottiene tutti gli allenamenti filtrati per categoria (lista di stringhe)"""
        if not self.check_permissions("read"):
            return []
        if not categorie:
            return []
        try:
            # Se la colonna categoria è una stringa, usiamo il filtro IN
            response = self.supabase.table("allenamenti").select("*").in_("categoria", categorie).order("data", desc=True).execute()
            return response.data or []
        except Exception as e:
            print(f"Errore nel recupero allenamenti per categorie: {str(e)}")
            return []
    def __init__(self):
        # Usa lo stesso client Supabase dell'auth service per condividere la sessione
        self.supabase = auth_service.supabase
        
    def check_permissions(self, operation: str = "read") -> bool:
        """
        Controlla i permessi per l'operazione richiesta
        read: tutti gli utenti autenticati
        write: solo amministratori
        """
        print(f"🔐 DEBUG PERMISSIONS: Controllo permessi per operazione '{operation}'")

        if not auth_service.is_authenticated():
            print("🔐 DEBUG PERMISSIONS: Utente non autenticato")
            return False

        print(f"🔐 DEBUG PERMISSIONS: Utente autenticato, ruolo: {auth_service.current_user_role}")

        if operation == "read":
            print("🔐 DEBUG PERMISSIONS: Operazione read - permessa")
            return True  # Tutti gli utenti autenticati possono leggere
        elif operation == "write":
            is_admin = auth_service.is_admin()
            print(f"🔐 DEBUG PERMISSIONS: Operazione write - is_admin: {is_admin}")
            return is_admin  # Solo admin possono scrivere

        print(f"🔐 DEBUG PERMISSIONS: Operazione '{operation}' non riconosciuta")
        return False
    
    # ========================================
    # METODI PER GIOCATORI
    # ========================================
    
    def ottieni_tutti_giocatori(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Ottiene tutti i giocatori"""
        if not self.check_permissions("read"):
            return []
            
        try:
            print(f"🔍 DEBUG SUPABASE: Query giocatori {'(inclusi inattivi)' if include_inactive else '(solo attivi)'}...")
            if include_inactive:
                # Per la vista completa, mostra tutti i giocatori
                response = self.supabase.table("giocatori").select("*").order("cognome").execute()
            else:
                response = self.supabase.table("giocatori").select("*").eq("attivo", True).order("cognome").execute()
            
            giocatori = response.data or []
            print(f"🔍 DEBUG SUPABASE: Response data: {len(giocatori)} giocatori trovati")
            
            if include_inactive:
                attivi = [g for g in giocatori if g.get("attivo") is True]
                inattivi = [g for g in giocatori if g.get("attivo") is not True]
                print(f"🔍 DEBUG SUPABASE: Attivi: {len(attivi)}, Inattivi: {len(inattivi)}")
            
            return giocatori
        except Exception as e:
            print(f"Errore nel recupero giocatori: {str(e)}")
            return []
    
    def ottieni_giocatore_by_id(self, giocatore_id: int) -> Optional[Dict[str, Any]]:
        """Ottiene un giocatore specifico per ID"""
        if not self.check_permissions("read"):
            return None
            
        try:
            response = self.supabase.table("giocatori").select("*").eq("id", giocatore_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Errore nel recupero giocatore {giocatore_id}: {str(e)}")
            return None
    
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
    
    def elimina_giocatore_definitivamente(self, giocatore_id: int) -> bool:
        """Elimina definitivamente un giocatore dal database"""
        print(f"🗑️ DEBUG SUPABASE: Tentativo eliminazione definitiva giocatore ID: {giocatore_id}")
        
        if not self.check_permissions("write"):
            print("🗑️ DEBUG SUPABASE: Permessi insufficienti per eliminare definitivamente giocatori")
            return False
            
        try:
            print("🗑️ DEBUG SUPABASE: Tentativo eliminazione fisica...")
            # Prima prova l'eliminazione fisica
            response = self.supabase.table("giocatori").delete().eq("id", giocatore_id).execute()
            print(f"🗑️ DEBUG SUPABASE: Response DELETE: {response}")
            print(f"🗑️ DEBUG SUPABASE: Response data: {response.data}")
            print(f"🗑️ DEBUG SUPABASE: Response status: {getattr(response, 'status_code', 'N/A')}")
            
            if response.data and len(response.data) > 0:
                print(f"🗑️ DEBUG SUPABASE: Eliminazione fisica riuscita, {len(response.data)} record eliminati")
                return True
            
            # Se l'eliminazione fisica fallisce (probabilmente per RLS), disattiva il giocatore
            print("🗑️ DEBUG SUPABASE: Eliminazione fisica fallita, tentando disattivazione...")
            from datetime import datetime
            update_data = {
                "attivo": False,
                "updated_at": datetime.now().isoformat()
            }
            print(f"🗑️ DEBUG SUPABASE: Update data: {update_data}")
            
            response = self.supabase.table("giocatori").update(update_data).eq("id", giocatore_id).execute()
            print(f"🗑️ DEBUG SUPABASE: Response UPDATE: {response}")
            print(f"🗑️ DEBUG SUPABASE: Response data: {response.data}")
            print(f"🗑️ DEBUG SUPABASE: Response status: {getattr(response, 'status_code', 'N/A')}")
            
            if response.data and len(response.data) > 0:
                print(f"🗑️ DEBUG SUPABASE: Disattivazione riuscita")
                return True
            else:
                print("🗑️ DEBUG SUPABASE: Anche disattivazione fallita")
                return False
                
        except Exception as e:
            print(f"🗑️ DEBUG SUPABASE: Eccezione durante eliminazione: {str(e)}")
            print(f"🗑️ DEBUG SUPABASE: Tipo eccezione: {type(e)}")
            import traceback
            print(f"🗑️ DEBUG SUPABASE: Traceback completo:\n{traceback.format_exc()}")
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
    
    def ottieni_allenamenti_per_data(self, data_str: str) -> List[Dict[str, Any]]:
        """Ottiene gli allenamenti per una data specifica"""
        if not self.check_permissions("read"):
            return []
            
        try:
            response = self.supabase.table("allenamenti").select("*").eq("data", data_str).execute()
            return response.data or []
        except Exception as e:
            print(f"Errore nel recupero allenamenti per data {data_str}: {str(e)}")
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
    
    def ottieni_partite_per_tipologia(self, tipologia: str) -> List[Dict[str, Any]]:
        """Ottiene le partite per tipologia"""
        if not self.check_permissions("read"):
            return []
            
        try:
            response = self.supabase.table("partite").select("*").eq("tipologia", tipologia).order("data", desc=True).execute()
            return response.data or []
        except Exception as e:
            print(f"Errore nel recupero partite per tipologia {tipologia}: {str(e)}")
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
        print(f"🔄 DEBUG SUPABASE: aggiorna_partita chiamato con ID: {partita_id} (tipo: {type(partita_id)})")
        print(f"🔄 DEBUG SUPABASE: dati_partita: {dati_partita}")

        if not self.check_permissions("write"):
            print("Permessi insufficienti per modificare partite")
            return False

        try:
            print(f"🔄 DEBUG SUPABASE: Tentativo update partita {partita_id}")
            print(f"🔄 DEBUG SUPABASE: Query: UPDATE partite SET ... WHERE id = {partita_id}")

            # Prima controlliamo se la partita esiste
            check_response = self.supabase.table("partite").select("id").eq("id", partita_id).execute()
            print(f"🔄 DEBUG SUPABASE: Controllo esistenza partita {partita_id}: {check_response.data}")

            response = self.supabase.table("partite").update(dati_partita).eq("id", partita_id).execute()
            print(f"🔄 DEBUG SUPABASE: Response update: {response}")
            print(f"🔄 DEBUG SUPABASE: Response data: {response.data}")
            print(f"🔄 DEBUG SUPABASE: Response status: {getattr(response, 'status_code', 'N/A')}")

            success = len(response.data) > 0
            print(f"🔄 DEBUG SUPABASE: Update successful: {success}")
            return success
        except Exception as e:
            print(f"Errore nell'aggiornamento partita: {str(e)}")
            import traceback
            traceback.print_exc()
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
    
    def aggiorna_convocati_partita(self, partita_id: int, convocati_data: List[Dict[str, Any]]) -> bool:
        """Aggiorna tutti i convocati per una partita"""
        if not self.check_permissions("write"):
            print("Permessi insufficienti per modificare convocazioni")
            return False
            
        try:
            # Prima elimina tutti i convocati esistenti per questa partita
            self.supabase.table("convocati").delete().eq("partita_id", partita_id).execute()
            
            # Poi inserisce i nuovi convocati
            if convocati_data:
                response = self.supabase.table("convocati").insert(convocati_data).execute()
                return len(response.data) == len(convocati_data)
            return True
        except Exception as e:
            print(f"Errore nell'aggiornamento convocati partita: {str(e)}")
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