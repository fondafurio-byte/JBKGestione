"""
Servizio di autenticazione Supabase per JBK Gestione
Gestisce login, logout, registrazione e controllo ruoli
"""

import os
from typing import Optional, Dict, Any
import json
from supabase import create_client, Client
import asyncio
from datetime import datetime, timedelta

class SupabaseAuthService:
    def __init__(self):
        # Configurazione Supabase (dovrai inserire le tue credenziali)
        self.supabase_url = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY", "your-anon-key-here")
        
        # Inizializza il client Supabase
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
        # Stato dell'utente corrente
        self.current_user = None
        self.current_user_role = None
        self.session = None
        
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Effettua il login con username e password
        Returns: {success: bool, user: dict, role: str, message: str}
        """
        try:
            # Prima trova l'email associata allo username
            profile_response = self.supabase.table("profiles").select("email").eq("username", username).execute()
            
            if not profile_response.data:
                return {
                    "success": False,
                    "user": None,
                    "role": None,
                    "message": "Username non trovato"
                }
            
            email = profile_response.data[0]['email']
            
            # Tentativo di login con email
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                self.current_user = response.user
                self.session = response.session
                # Ottieni ruolo e categorie dal profilo
                profile_response = self.supabase.table("profiles").select("*").eq("id", response.user.id).execute()
                if profile_response.data:
                    self.current_user_role = profile_response.data[0]['role']
                    self.current_user_categories = profile_response.data[0].get('categories', '[]')
                    return {
                        "success": True,
                        "user": response.user,
                        "role": self.current_user_role,
                        "categories": self.current_user_categories,
                        "message": f"Benvenuto! Accesso come {self.current_user_role}"
                    }
                else:
                    # Crea profilo se non esiste (primo accesso)
                    username = response.user.user_metadata.get("username", response.user.email.split('@')[0])
                    role = response.user.user_metadata.get("role", "user")
                    categories = response.user.user_metadata.get("categories", "[]")
                    self.supabase.table("profiles").insert({
                        "id": response.user.id,
                        "email": response.user.email,
                        "username": username,
                        "full_name": response.user.user_metadata.get("full_name", ""),
                        "role": role,
                        "categories": categories
                    }).execute()
                    self.current_user_role = role
                    self.current_user_categories = categories
                    return {
                        "success": True,
                        "user": response.user,
                        "role": role,
                        "categories": categories,
                        "message": f"Primo accesso - Profilo creato come {role}"
                    }
            
            return {
                "success": False,
                "user": None,
                "role": None,
                "message": "Credenziali non valide"
            }
            
        except Exception as e:
            return {
                "success": False,
                "user": None,
                "role": None,
                "message": f"Errore durante il login: {str(e)}"
            }
    
    def logout(self) -> bool:
        """Effettua il logout"""
        try:
            self.supabase.auth.sign_out()
            self.current_user = None
            self.current_user_role = None
            self.session = None
            return True
        except Exception as e:
            print(f"Errore durante il logout: {str(e)}")
            return False
    
    def register(self, username: str, email: str, password: str, full_name: str = "", role: str = "user", categories=None) -> Dict[str, Any]:
        """
        Registra un nuovo utente con ruolo e categorie
        Returns: {success: bool, message: str}
        """
        try:
            # Verifica che lo username non esista già
            existing_profile = self.supabase.table("profiles").select("username").eq("username", username).execute()
            if existing_profile.data:
                return {
                    "success": False,
                    "message": "Username già esistente"
                }
            if categories is None:
                categories = []
            # Limita a massimo 3 categorie per i coach
            if role == "coach" and len(categories) > 3:
                return {
                    "success": False,
                    "message": "Un coach può selezionare al massimo 3 categorie."
                }
            categories_json = json.dumps(categories)
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "username": username,
                        "full_name": full_name,
                        "role": role,
                        "categories": categories_json
                    }
                }
            })
            if response.user:
                # Il profilo verrà creato automaticamente al primo login
                return {
                    "success": True,
                    "message": "Registrazione completata! Controlla la tua email per confermare l'account."
                }
            else:
                return {
                    "success": False,
                    "message": "Errore durante la registrazione"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Errore durante la registrazione: {str(e)}"
            }
    
    def is_authenticated(self) -> bool:
        """Verifica se l'utente è autenticato"""
        return self.current_user is not None and self.session is not None
    
    def is_admin(self) -> bool:
        """Verifica se l'utente corrente è un amministratore"""
        return self.is_authenticated() and self.current_user_role == "admin"
    
    def is_user(self) -> bool:
        """Verifica se l'utente corrente è un utente normale"""
        return self.is_authenticated() and self.current_user_role == "user"
    
    def get_current_user_info(self) -> Optional[Dict[str, Any]]:
        """Ottiene le informazioni dell'utente corrente"""
        if not self.is_authenticated():
            return None
            
        return {
            "id": self.current_user.id,
            "email": self.current_user.email,
            "role": self.current_user_role,
            "full_name": self.current_user.user_metadata.get("full_name", "")
        }
    
    def check_session(self) -> bool:
        """Controlla se la sessione è ancora valida e ripristina i dati utente"""
        try:
            session = self.supabase.auth.get_session()
            if session and session.access_token:
                self.session = session
                self.current_user = session.user
                
                # Ripristina il ruolo dell'utente dal profilo
                if session.user:
                    profile_response = self.supabase.table("profiles").select("*").eq("id", session.user.id).execute()
                    if profile_response.data:
                        self.current_user_role = profile_response.data[0]['role']
                    else:
                        # Se non c'è profilo, imposta ruolo default
                        self.current_user_role = "user"
                
                return True
            else:
                self.logout()
                return False
        except Exception as e:
            print(f"Errore nel controllo sessione: {str(e)}")
            self.logout()
            return False
    
    def change_user_role(self, user_id: str, new_role: str) -> Dict[str, Any]:
        """
        Cambia il ruolo di un utente (solo per admin)
        """
        if not self.is_admin():
            return {
                "success": False,
                "message": "Accesso negato: solo gli amministratori possono modificare i ruoli"
            }
        
        try:
            response = self.supabase.table("profiles").update({
                "role": new_role
            }).eq("id", user_id).execute()
            
            return {
                "success": True,
                "message": f"Ruolo aggiornato a {new_role}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Errore nell'aggiornamento del ruolo: {str(e)}"
            }
    
    def get_all_users(self) -> Dict[str, Any]:
        """
        Ottiene tutti gli utenti (solo per admin)
        """
        if not self.is_admin():
            return {
                "success": False,
                "data": [],
                "message": "Accesso negato: solo gli amministratori possono visualizzare tutti gli utenti"
            }
        
        try:
            response = self.supabase.table("profiles").select("*").execute()
            return {
                "success": True,
                "data": response.data,
                "message": "Utenti caricati con successo"
            }
        except Exception as e:
            return {
                "success": False,
                "data": [],
                "message": f"Errore nel caricamento utenti: {str(e)}"
            }

# Istanza globale del servizio di autenticazione
auth_service = SupabaseAuthService()