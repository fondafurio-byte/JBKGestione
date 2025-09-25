"""
Schermata di Login per JBK Gestione
Interface di autenticazione con Supabase
"""

import toga
from toga.style.pack import COLUMN, ROW, Pack
from toga.constants import CENTER, LEFT
from .supabase_auth import auth_service

class LoginWindow:
    def __init__(self, app):
        self.app = app
        self.main_window = None
        self.username_input = None
        self.password_input = None
        self.login_button = None
        self.register_button = None
        self.status_label = None
        self.user_role_label = None
        
    def create_login_window(self):
        """Crea la finestra di login"""
        
        # Container principale con sfondo rosso e centraggio completo
        main_container = toga.Box(style=Pack(
            direction=COLUMN,
            alignment=CENTER,
            padding=50,
            background_color="#dc3545",  # Sfondo rosso
            flex=1  # Occupa tutto lo spazio disponibile per centrare meglio
        ))
        
        # Logo/Titolo dell'app con testo bianco
        title_label = toga.Label(
            "🏀 JBK GESTIONE",
            style=Pack(
                font_size=28,
                font_weight="bold",
                color="white",  # Testo bianco
                padding_bottom=10,
                text_align=CENTER
            )
        )
        main_container.add(title_label)
        
        # Sottotitolo con testo bianco
        subtitle_label = toga.Label(
            "Sistema di Gestione Squadra Basket",
            style=Pack(
                font_size=14,
                color="white",  # Testo bianco
                padding_bottom=30,
                text_align=CENTER
            )
        )
        main_container.add(subtitle_label)
        
        # Container per il form di login centrato con sfondo rosso
        login_container = toga.Box(style=Pack(
            direction=COLUMN,
            padding=30,
            background_color="#dc3545",  # Sfondo rosso anche qui
            alignment=CENTER,
            width=400,  # Larghezza fissa per centrare meglio
        ))
        
        # Titolo form login con testo bianco
        login_title = toga.Label(
            "Accedi al Sistema",
            style=Pack(
                font_size=18,
                font_weight="bold",
                color="white",  # Testo bianco
                padding_bottom=20,
                text_align=CENTER
            )
        )
        login_container.add(login_title)
        
        # Campo Username con testo bianco
        username_label = toga.Label(
            "Nome Utente:",
            style=Pack(
                font_size=12,
                color="white",  # Testo bianco
                padding_bottom=5,
                text_align=CENTER  # Centrare le etichette
            )
        )
        login_container.add(username_label)
        
        self.username_input = toga.TextInput(
            placeholder="Inserisci il tuo nome utente",
            style=Pack(
                width=300,
                padding_bottom=15,
                font_size=14,
                text_align=CENTER  # Centrare il testo di input
            )
        )
        login_container.add(self.username_input)
        
        # Campo Password con testo bianco
        password_label = toga.Label(
            "Password:",
            style=Pack(
                font_size=12,
                color="white",  # Testo bianco
                padding_bottom=5,
                text_align=CENTER  # Centrare le etichette
            )
        )
        login_container.add(password_label)
        
        self.password_input = toga.PasswordInput(
            placeholder="Inserisci la tua password",
            style=Pack(
                width=300,
                padding_bottom=20,
                font_size=14,
                text_align=CENTER  # Centrare il testo di input
            )
        )
        login_container.add(self.password_input)
        
        # Container per i pulsanti
        button_container = toga.Box(style=Pack(
            direction=ROW,
            padding_bottom=20
        ))
        
        # Pulsante Login
        self.login_button = toga.Button(
            "🔐 ACCEDI",
            on_press=self.handle_login,
            style=Pack(
                width=140,
                padding=10,
                background_color="#3498db",
                color="#ffffff",
                font_size=12,
                font_weight="bold"
            )
        )
        button_container.add(self.login_button)
        
        # Spacer
        spacer = toga.Box(style=Pack(width=20))
        button_container.add(spacer)
        
        # Pulsante Registrazione
        self.register_button = toga.Button(
            "👤 REGISTRATI",
            on_press=self.handle_register,
            style=Pack(
                width=140,
                padding=10,
                background_color="#27ae60",
                color="#ffffff",
                font_size=12,
                font_weight="bold"
            )
        )
        button_container.add(self.register_button)
        
        login_container.add(button_container)
        
        # Label per messaggi di stato con testo bianco
        self.status_label = toga.Label(
            "",
            style=Pack(
                font_size=12,
                padding_top=10,
                text_align=CENTER,
                color="white"  # Testo bianco per i messaggi di stato
            )
        )
        login_container.add(self.status_label)
        
        # Label per ruolo utente con testo bianco
        self.user_role_label = toga.Label(
            "",
            style=Pack(
                font_size=11,
                padding_top=5,
                text_align=CENTER,
                color="white",  # Testo bianco
                font_style="italic"
            )
        )
        login_container.add(self.user_role_label)
        
        main_container.add(login_container)
        
        return main_container
    
    def handle_login(self, widget):
        """Gestisce il tentativo di login"""
        username = self.username_input.value.strip()
        password = self.password_input.value.strip()
        
        if not username or not password:
            self.show_status("⚠️ Inserisci nome utente e password")
            return
        
        self.show_status("🔄 Accesso in corso...")
        self.login_button.enabled = False
        
        # Tentativo di login
        try:
            print(f"🔐 Tentativo login per utente: {username}")
            result = auth_service.login(username, password)
            print(f"🔐 Risultato login: {result}")
            
            if result["success"]:
                self.show_status(f"✅ {result['message']}")
                self.user_role_label.text = f"Ruolo: {result['role'].upper()}"
                
                # Riabilita il pulsante per evitare che rimanga disabilitato
                self.login_button.enabled = True
                
                # Dopo un breve delay, passa all'app principale
                print("🚀 Programmazione avvio app principale...")
                self.app.add_background_task(self.delayed_app_start)
            else:
                self.show_status(f"❌ {result['message']}")
                self.login_button.enabled = True
        except Exception as e:
            print(f"❌ Errore durante login: {e}")
            self.show_status(f"❌ Errore di connessione: {str(e)}")
            self.login_button.enabled = True
    
    def handle_register(self, widget):
        """Gestisce la registrazione (per ora mostra un messaggio)"""
        self.show_status("📝 Registrazione non implementata in questa demo")
        
        # In una versione completa, apriresti una finestra di registrazione
        # o implementeresti la registrazione direttamente qui
    
    def show_status(self, message: str, color: str = "white"):
        """Mostra un messaggio di stato"""
        self.status_label.text = message
        # Manteniamo sempre il testo bianco per coerenza con il design
        self.status_label.style.color = "white"
    
    async def delayed_app_start(self, widget):
        """Avvia l'app principale dopo un breve delay"""
        print("⏰ Inizio delay prima dell'avvio...")
        import asyncio
        await asyncio.sleep(1.5)  # Aspetta 1.5 secondi
        
        print("🚀 Chiamata start_main_app...")
        try:
            # Chiudi la finestra di login e avvia l'app principale
            self.app.start_main_app()
            print("✅ start_main_app completato")
        except Exception as e:
            print(f"❌ Errore in start_main_app: {e}")
            self.show_status(f"❌ Errore avvio app: {str(e)}")
            self.login_button.enabled = True

class RegisterWindow:
    """Finestra di registrazione (implementazione futura)"""
    def __init__(self, app):
        self.app = app
        
    def create_register_window(self):
        """Crea la finestra di registrazione"""
        # Implementazione futura per registrazione utenti
        pass