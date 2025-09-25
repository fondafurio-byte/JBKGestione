"""
Applicazione principale JBK Gestione - App per la gestione di una squadra di basket
Versione Supabase con autenticazione
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, LEFT, RIGHT
from datetime import datetime, timedelta
import calendar
import sqlite3
import json
import os

# Import per autenticazione Supabase
from .supabase_auth import auth_service
from .supabase_db import db_manager
from .login_window import LoginWindow

# Import per compatibilità (da sostituire gradualmente)
from .models import DatabaseManager, Giocatore, Partita, Allenamento
from .services import GiocatoriService, PartiteService, AllenamentiService, StatisticheService, ConvocatiService, StatisticheIndividualiService


class JBKGestione(toga.App):
    """Applicazione principale per la gestione della squadra di basket"""
    
    def __init__(self):
        """Inizializza l'applicazione con nome formale"""
        super().__init__(
            formal_name="JBK Gestione",
            app_id="com.jbk.gestione",
            app_name="JBK Gestione",
            description="Applicazione per la gestione della squadra di basket JBK",
            version="1.0.0"
        )
    
    def setup_responsive_config(self):
        """Configura le dimensioni responsive per diverse piattaforme"""
        # Configurazione elegante per desktop/tablet con font ridotti
        self.config = {
            'sidebar_width': 280,
            'button_height': 45,     # Ridotto per eleganza
            'button_font_size': 12,  # Ridotto per eleganza
            'title_font_size': 16,   # Ridotto per eleganza
            'label_font_size': 11,   # Ridotto per eleganza
            'padding_large': 12,     # Ridotto per compattezza
            'padding_medium': 8,     # Ridotto per compattezza
            'padding_small': 5,      # Ridotto per compattezza
            'touch_target_min': 40,  # Ridotto ma mantenendo usabilità
            'row_height': 50,        # Ridotto per compattezza
            'header_height': 65,     # Ridotto per eleganza
            'content_padding': 10    # Ridotto per compattezza
        }
        
        # Rileva se siamo su mobile/iOS (approssimazione basata su dimensioni)
        try:
            # Per iOS/mobile, aumentiamo le dimensioni dei touch target
            import platform
            if platform.system() == 'iOS' or hasattr(self, 'is_mobile'):
                self.config.update({
                    'sidebar_width': 300,     # Ridotto per eleganza
                    'button_height': 50,      # Ridotto per eleganza
                    'button_font_size': 14,   # Ridotto per eleganza
                    'title_font_size': 18,    # Ridotto per eleganza
                    'label_font_size': 13,    # Ridotto per eleganza
                    'padding_large': 15,      # Ridotto per compattezza
                    'padding_medium': 10,     # Ridotto per compattezza
                    'padding_small': 8,       # Ridotto per compattezza
                    'touch_target_min': 45,   # Ridotto mantenendo usabilità
                    'row_height': 55,         # Ridotto per compattezza
                    'header_height': 70,      # Ridotto per eleganza
                    'content_padding': 12     # Ridotto per compattezza
                })
        except:
            pass  # Mantieni configurazione desktop se non possiamo rilevare
    
    def create_responsive_button(self, text, on_press, bg_color="#2196f3", text_color="#ffffff", width_full=False):
        """Crea un pulsante con dimensioni responsive"""
        width = None if width_full else self.config['sidebar_width'] - 30
        return toga.Button(
            text,
            on_press=on_press,
            style=Pack(
                padding=self.config['padding_medium'],
                width=width,
                height=self.config['button_height'],
                background_color=bg_color,
                color=text_color,
                font_size=self.config['button_font_size']
            )
        )
    
    def create_responsive_label(self, text, font_size_type='normal', color="#000000", **style_kwargs):
        """Crea una label con dimensioni responsive"""
        font_sizes = {
            'title': self.config['title_font_size'],
            'subtitle': self.config['label_font_size'] + 2,
            'normal': self.config['label_font_size'],
            'small': self.config['label_font_size'] - 2
        }
        
        default_style = Pack(
            font_size=font_sizes.get(font_size_type, self.config['label_font_size']),
            color=color,
            padding=self.config['padding_small']
        )
        
        # Merge con stili personalizzati
        for key, value in style_kwargs.items():
            setattr(default_style, key, value)
        
        return toga.Label(text, style=default_style)
    
    def startup(self):
        """Inizializza l'applicazione con autenticazione"""
        print("🚀 Avvio JBK Gestione con autenticazione Supabase...")
        
        # Controlla se l'utente ha già una sessione valida
        if not auth_service.check_session():
            print("❌ Nessuna sessione valida - Mostrando schermata di login")
            self.show_login_screen()
            return
        
        print("✅ Sessione valida trovata - Avvio app principale")
        self.start_main_app()
    
    def show_login_screen(self):
        """Mostra la schermata di login"""
        print("🔐 Creazione schermata di login...")
        
        # Configurazione dimensioni per login
        self.setup_responsive_config()
        
        # Crea la finestra di login
        self.login_window = LoginWindow(self)
        login_content = self.login_window.create_login_window()
        
        # Imposta il contenuto della finestra principale
        self.main_window = toga.MainWindow(title="JBK Gestione - Accesso")
        self.main_window.content = login_content
        self.main_window.show()
    
    def start_main_app(self):
        """Avvia l'interfaccia principale dell'app dopo l'autenticazione"""
        print("🏀 Avvio interfaccia principale...")
        
        # Verifica autenticazione
        if not auth_service.is_authenticated():
            print("❌ Utente non autenticato - Tornando al login")
            self.show_login_screen()
            return
        
        # Ottieni informazioni utente
        user_info = auth_service.get_current_user_info()
        print(f"👤 Utente autenticato: {user_info['email']} (Ruolo: {user_info['role']})")
        
        # Inizializza il database e i servizi
        print("🗄️ Inizializzazione servizi database...")
        
        # Per ora manteniamo compatibilità con il vecchio sistema
        # TODO: Migrare completamente ai servizi Supabase
        self.db_manager = DatabaseManager()
        self.giocatori_service = GiocatoriService(self.db_manager)
        self.partite_service = PartiteService(self.db_manager)
        self.convocati_service = ConvocatiService(self.db_manager)
        self.allenamenti_service = AllenamentiService(self.db_manager)
        self.statistiche_service = StatisticheService(self.db_manager)
        self.statistiche_individuali_service = StatisticheIndividualiService(self.db_manager)
        
        # Riferimento ai servizi Supabase
        self.supabase_db = db_manager
        
        # Variabile per tracciare la pagina corrente
        self.pagina_corrente = "home"
        
        # Configurazione dimensioni adattive per iOS/mobile
        self.setup_responsive_config()
        
        # Container principale dell'app con layout adattivo
        self.main_container = toga.Box(style=Pack(direction=ROW))
        
        # Menu di navigazione laterale con dimensioni responsive
        self.sidebar = toga.Box(
            style=Pack(
                direction=COLUMN,
                width=self.config['sidebar_width'],
                background_color="#d32f2f",
                padding=0
            )
        )
        
        # Header del menu con dimensioni responsive
        header_sidebar = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=self.config['padding_medium'],
                background_color="#d32f2f"
            )
        )
        
        logo_label = toga.Label(
            "🏀 JBK",
            style=Pack(
                font_size=self.config['title_font_size'],
                font_weight="bold",
                color="#ffffff",
                text_align=CENTER,
                padding=(self.config['padding_small'], 0)
            )
        )
        
        subtitle_label = toga.Label(
            "GESTIONE SQUADRA",
            style=Pack(
                font_size=self.config['label_font_size'] - 2,
                color="#ecf0f1",
                text_align=CENTER,
                padding=(0, self.config['padding_small'])
            )
        )
        
        header_sidebar.add(logo_label)
        header_sidebar.add(subtitle_label)
        self.sidebar.add(header_sidebar)

        # Menu items
        menu_items = toga.Box(style=Pack(direction=COLUMN, padding=10))        # Pulsante Home con dimensioni responsive
        self.btn_home = toga.Button(
            "🏠 HOME",
            on_press=self.mostra_home,
            style=Pack(
                padding=self.config['padding_medium'],
                width=self.config['sidebar_width'] - 30,
                height=self.config['button_height'],
                background_color="#34495e",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                text_align=LEFT
            )
        )
        
        # Pulsante Giocatori con dimensioni responsive
        self.btn_giocatori = toga.Button(
            "👥 GIOCATORI",
            on_press=self.mostra_giocatori,
            style=Pack(
                padding=self.config['padding_medium'],
                width=self.config['sidebar_width'] - 30,
                height=self.config['button_height'],
                background_color="#2e7d32",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                text_align=LEFT
            )
        )
        
        # Pulsante Partite con dimensioni responsive
        self.btn_partite = toga.Button(
            "🏀 PARTITE",
            on_press=self.mostra_partite,
            style=Pack(
                padding=self.config['padding_medium'],
                width=self.config['sidebar_width'] - 30,
                height=self.config['button_height'],
                background_color="#ffc107",
                color="#000000",
                font_size=self.config['button_font_size'],
                text_align=LEFT
            )
        )
        
        # Pulsante Allenamenti con dimensioni responsive
        self.btn_allenamenti = toga.Button(
            "💪 ALLENAMENTI",
            on_press=self.mostra_allenamenti,
            style=Pack(
                padding=self.config['padding_medium'],
                width=self.config['sidebar_width'] - 30,
                height=self.config['button_height'],
                background_color="#f57c00",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                text_align=LEFT
            )
        )
        
        # Pulsante Statistiche con dimensioni responsive
        self.btn_statistiche = toga.Button(
            "📊 STATISTICHE",
            on_press=self.mostra_statistiche,
            style=Pack(
                padding=self.config['padding_medium'],
                width=self.config['sidebar_width'] - 30,
                height=self.config['button_height'],
                background_color="#7b1fa2",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                text_align=LEFT
            )
        )
        
        # Spazio flessibile
        spacer = toga.Box(style=Pack(flex=1))
        
        # Footer del menu
        footer_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        version_label = toga.Label(
            "v0.0.1",
            style=Pack(
                font_size=10,
                color="#95a5a6",
                text_align=CENTER
            )
        )
        footer_box.add(version_label)
        
        menu_items.add(self.btn_home)
        menu_items.add(self.btn_giocatori)
        menu_items.add(self.btn_partite)
        menu_items.add(self.btn_allenamenti)
        menu_items.add(self.btn_statistiche)
        
        # Sezione utente e controlli
        user_section = self.create_user_section()
        menu_items.add(user_section)
        
        menu_items.add(spacer)
        menu_items.add(footer_box)
        
        self.sidebar.add(menu_items)
        
        # Area principale per il contenuto
        self.content_area = toga.Box(
            style=Pack(
                direction=COLUMN,
                flex=1,
                background_color="#ecf0f1",
                padding=0
            )
        )
        
        # Rimuoviamo l'header delle pagine - il titolo è ora nel sidebar
        
        # Contenuto dinamico con scroll e dimensioni responsive
        self.dynamic_content = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=self.config['content_padding'],
                background_color="#ffffff"
            )
        )
        
        # Container scroll per il contenuto dinamico
        self.scroll_container = toga.ScrollContainer(
            content=self.dynamic_content,
            style=Pack(
                flex=1,
                background_color="#ffffff",
                height=600  # Altezza minima per riempire l'area contenuto
            )
        )
        
        # Aggiungi direttamente il contenuto scroll all'area contenuti
        self.content_area.add(self.scroll_container)
        
        # Crea la top bar con il tasto hamburger
        self.top_bar = self.crea_top_bar()
        
        # Container principale che include top bar e contenuto (senza sidebar inizialmente)
        self.app_container = toga.Box(
            style=Pack(direction=COLUMN)
        )
        self.app_container.add(self.top_bar)
        self.app_container.add(self.content_area)
        
        # Container overlay per la sidebar (inizialmente nascosta)
        self.overlay_container = None
        
        # Variabile per tracciare lo stato della sidebar (inizialmente nascosta)
        self.sidebar_visible = False
        
        # Crea la finestra principale
        self.main_window = toga.MainWindow(title=self.formal_name, size=(1200, 800))
        self.main_window.content = self.app_container
        self.main_window.show()
        
        # Mostra la home di default
        self.mostra_home(None)
    
    def create_user_section(self):
        """Crea la sezione informazioni utente nel menu"""
        user_info = auth_service.get_current_user_info()
        
        user_container = toga.Box(style=Pack(
            direction=COLUMN,
            padding=10,
            background_color="#34495e"
        ))
        
        # Separatore
        separator = toga.Box(style=Pack(
            height=1,
            background_color="#7f8c8d",
            padding_bottom=10
        ))
        user_container.add(separator)
        
        # Informazioni utente
        user_name = toga.Label(
            f"👤 {user_info['email'][:20]}{'...' if len(user_info['email']) > 20 else ''}",
            style=Pack(
                font_size=10,
                color="#ecf0f1",
                text_align=CENTER,
                padding_bottom=5
            )
        )
        user_container.add(user_name)
        
        # Ruolo utente con colore distintivo
        role_color = "#e74c3c" if user_info['role'] == 'admin' else "#3498db"
        role_icon = "👑" if user_info['role'] == 'admin' else "👤"
        
        user_role = toga.Label(
            f"{role_icon} {user_info['role'].upper()}",
            style=Pack(
                font_size=9,
                color=role_color,
                text_align=CENTER,
                font_weight="bold",
                padding_bottom=10
            )
        )
        user_container.add(user_role)
        
        # Pulsante Logout
        logout_button = toga.Button(
            "🚪 ESCI",
            on_press=self.handle_logout,
            style=Pack(
                width=self.config['sidebar_width'] - 50,
                height=35,
                background_color="#e74c3c",
                color="#ffffff",
                font_size=10,
                text_align=CENTER
            )
        )
        user_container.add(logout_button)
        
        # Mostra permessi solo per admin
        if auth_service.is_admin():
            admin_note = toga.Label(
                "Accesso completo",
                style=Pack(
                    font_size=8,
                    color="#f39c12",
                    text_align=CENTER,
                    padding_top=5,
                    font_style="italic"
                )
            )
            user_container.add(admin_note)
        else:
            user_note = toga.Label(
                "Solo lettura",
                style=Pack(
                    font_size=8,
                    color="#95a5a6",
                    text_align=CENTER,
                    padding_top=5,
                    font_style="italic"
                )
            )
            user_container.add(user_note)
        
        return user_container
    
    def handle_logout(self, widget):
        """Gestisce il logout"""
        print("🚪 Logout richiesto...")
        
        # Effettua il logout
        if auth_service.logout():
            print("✅ Logout completato - Tornando al login")
            # Ricrea la finestra di login
            self.show_login_screen()
        else:
            print("❌ Errore durante il logout")
    
    def crea_top_bar(self):
        """Crea la barra superiore con il tasto hamburger"""
        top_bar = toga.Box(
            style=Pack(
                direction=ROW,
                padding=10,
                background_color="#2c3e50",
                height=50
            )
        )
        
        # Tasto hamburger per mostrare/nascondere la sidebar
        self.hamburger_button = toga.Button(
            "☰",  # Icona tre linee
            on_press=self.toggle_sidebar,
            style=Pack(
                width=50,
                height=30,
                background_color="#34495e",
                color="#ffffff",
                font_size=16,
                padding=5
            )
        )
        
        # Titolo dinamico della pagina nella top bar
        self.top_bar_title = toga.Label(
            "� HOME",
            style=Pack(
                flex=1,
                font_size=16,
                font_weight="bold",
                color="#ffffff",
                padding=(5, 15), 
                text_align=CENTER
            )
        )
        
        # Spazio per bilanciare il layout
        spacer = toga.Box(style=Pack(width=50))
        
        top_bar.add(self.hamburger_button)
        top_bar.add(self.top_bar_title)
        top_bar.add(spacer)
        
        return top_bar
    
    def toggle_sidebar(self, widget):
        """Mostra/nasconde la sidebar come overlay"""
        print(f"🍔 DEBUG TOGGLE: toggle_sidebar chiamato, stato attuale: {self.sidebar_visible}")
        print(f"🍔 DEBUG TOGGLE: Pagina corrente: {getattr(self, 'pagina_corrente', 'non definita')}")
        
        try:
            if self.sidebar_visible:
                print("🍔 DEBUG TOGGLE: Nascondendo sidebar overlay...")
                # Ricrea l'app_container con il contenuto aggiornato
                self.ricostruisci_app_container()
                self.main_window.content = self.app_container
                self.overlay_container = None
                self.sidebar_visible = False
                print("🍔 DEBUG TOGGLE: Sidebar overlay nascosta, app_container ricostruito")
                print(f"🍔 DEBUG TOGGLE: Finestra ora mostra: {type(self.main_window.content).__name__}")
                print(f"🍔 DEBUG TOGGLE: dynamic_content ha {len(self.dynamic_content.children) if hasattr(self.dynamic_content, 'children') else 'N/A'} figli")
                
                # Forza un refresh del layout per assicurarsi che il contenuto sia visibile
                try:
                    self.main_window.content.refresh()
                    print("🍔 DEBUG TOGGLE: Layout refreshed")
                except:
                    print("🍔 DEBUG TOGGLE: Refresh non supportato, continuo...")
            else:
                print("🍔 DEBUG TOGGLE: Mostrando sidebar overlay...")
                # Mostra la sidebar come overlay
                self.crea_sidebar_overlay()
                self.sidebar_visible = True
                print("🍔 DEBUG TOGGLE: Sidebar overlay mostrata e attiva")
                
        except Exception as e:
            print(f"🍔 DEBUG TOGGLE: ERRORE in toggle_sidebar: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def ricostruisci_app_container(self):
        """Ricostruisce l'app_container con il contenuto aggiornato"""
        print("🔄 DEBUG REBUILD: Ricostruzione app_container iniziata")
        
        # Crea un nuovo container
        self.app_container = toga.Box(
            style=Pack(direction=COLUMN)
        )
        
        # Aggiungi la top bar
        self.app_container.add(self.top_bar)
        
        # Aggiungi il content_area che contiene il contenuto aggiornato
        self.app_container.add(self.content_area)
        
        print(f"🔄 DEBUG REBUILD: App_container ricostruito con content_area")
        print(f"🔄 DEBUG REBUILD: dynamic_content ha {len(self.dynamic_content.children) if hasattr(self.dynamic_content, 'children') else 'N/A'} elementi")
    
    def crea_sidebar_overlay(self):
        """Crea l'overlay della sidebar sopra il contenuto reale"""
        print("🎯 DEBUG MENU: Creazione sidebar overlay iniziata")
        
        # Container principale per l'overlay
        overlay_main = toga.Box(
            style=Pack(direction=COLUMN)
        )
        
        # Aggiungi sempre la top bar
        overlay_main.add(self.top_bar)
        
        # Container che mostra sidebar e contenuto reale affiancati
        overlay_content = toga.Box(
            style=Pack(direction=ROW, flex=1)
        )
        
        # Sidebar con sfondo rosso originale
        sidebar_overlay = toga.Box(
            style=Pack(
                direction=COLUMN,
                width=self.config['sidebar_width'],
                background_color="#d32f2f",  # Sfondo rosso originale
                padding=0
            )
        )
        
        # Ricrea il contenuto della sidebar per l'overlay
        self.crea_contenuto_sidebar(sidebar_overlay)
        
        # Area contenuto reale con velo semi-trasparente
        content_with_veil = toga.Box(
            style=Pack(
                direction=COLUMN,
                flex=1,
                background_color="#ecf0f1",  # Colore di base del contenuto
                padding=0
            )
        )
        

        
        # Contenuto reale della pagina (visibile ma con velo sopra)
        content_with_veil.add(self.content_area)
        
        # Assembla l'overlay
        overlay_content.add(sidebar_overlay)
        overlay_content.add(content_with_veil)
        
        overlay_main.add(overlay_content)
        
        # Sostituisce completamente il contenuto della finestra
        self.overlay_container = overlay_main
        self.main_window.content = overlay_main
        print("🎯 DEBUG MENU: Sidebar overlay creata e applicata alla finestra")
    
    def chiudi_overlay(self, widget):
        """Chiude l'overlay della sidebar"""
        print("🎯 DEBUG MENU: Tentativo di chiusura overlay")
        if self.sidebar_visible:
            print("🎯 DEBUG MENU: Overlay era visibile, chiudendo...")
            # Ripristina il contenuto originale senza sidebar
            self.main_window.content = self.app_container
            self.overlay_container = None
            self.sidebar_visible = False
            print("� DEBUG MENU: Overlay chiuso e contenuto ripristinato")
        else:
            print("🎯 DEBUG MENU: Overlay non era visibile, nessuna azione necessaria")
    
    def crea_contenuto_sidebar(self, container):
        """Crea il contenuto della sidebar nel container specificato"""
        print("🎯 DEBUG MENU: Creazione contenuto sidebar iniziata")
        
        # Header sidebar (il container principale ha già lo sfondo rosso)
        header_sidebar = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=self.config['padding_medium'],
                background_color="transparent"  # Trasparente per usare il rosso del container
            )
        )
        
        logo_label = toga.Label(
            "🏀 JBK",
            style=Pack(
                font_size=self.config['title_font_size'],
                font_weight="bold",
                color="#ffffff",
                text_align=CENTER,
                padding=(self.config['padding_small'], 0)
            )
        )
        
        subtitle_label = toga.Label(
            "GESTIONE SQUADRA",
            style=Pack(
                font_size=self.config['label_font_size'] - 2,
                color="#ecf0f1",
                text_align=CENTER,
                padding=(0, self.config['padding_small'])
            )
        )
        
        header_sidebar.add(logo_label)
        header_sidebar.add(subtitle_label)
        container.add(header_sidebar)
        
        # Menu items con sfondo trasparente per mantenere il rosso
        menu_items = toga.Box(
            style=Pack(
                direction=COLUMN, 
                padding=10,
                background_color="transparent"
            )
        )
        
        # Pulsanti menu (ricreati per l'overlay)
        btn_home_overlay = toga.Button(
            "🏠 HOME",
            on_press=self.mostra_home_e_chiudi,
            style=Pack(
                padding=self.config['padding_medium'],
                width=self.config['sidebar_width'] - 30,
                height=self.config['button_height'],
                background_color="#5d6d7e" if self.pagina_corrente == "home" else "#34495e",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                text_align=LEFT
            )
        )
        
        btn_giocatori_overlay = toga.Button(
            "👥 GIOCATORI",
            on_press=self.mostra_giocatori_e_chiudi,
            style=Pack(
                padding=self.config['padding_medium'],
                width=self.config['sidebar_width'] - 30,
                height=self.config['button_height'],
                background_color="#4caf50" if self.pagina_corrente == "giocatori" else "#2e7d32",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                text_align=LEFT
            )
        )
        
        btn_partite_overlay = toga.Button(
            "🏀 PARTITE",
            on_press=self.mostra_partite_e_chiudi,
            style=Pack(
                padding=self.config['padding_medium'],
                width=self.config['sidebar_width'] - 30,
                height=self.config['button_height'],
                background_color="#ffc107",
                color="#000000" if self.pagina_corrente == "partite" else "#000000",
                font_size=self.config['button_font_size'],
                text_align=LEFT
            )
        )
        
        btn_allenamenti_overlay = toga.Button(
            "💪 ALLENAMENTI",
            on_press=self.mostra_allenamenti_e_chiudi,
            style=Pack(
                padding=self.config['padding_medium'],
                width=self.config['sidebar_width'] - 30,
                height=self.config['button_height'],
                background_color="#ff9800" if self.pagina_corrente == "allenamenti" else "#f57c00",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                text_align=LEFT
            )
        )
        
        btn_statistiche_overlay = toga.Button(
            "📊 STATISTICHE",
            on_press=self.mostra_statistiche_e_chiudi,
            style=Pack(
                padding=self.config['padding_medium'],
                width=self.config['sidebar_width'] - 30,
                height=self.config['button_height'],
                background_color="#9c27b0" if self.pagina_corrente == "statistiche" else "#7b1fa2",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                text_align=LEFT
            )
        )
        
        menu_items.add(btn_home_overlay)
        menu_items.add(btn_giocatori_overlay)
        menu_items.add(btn_partite_overlay)
        menu_items.add(btn_allenamenti_overlay)
        menu_items.add(btn_statistiche_overlay)
        
        container.add(menu_items)
        print(f"🎯 DEBUG MENU: Contenuto sidebar creato con {len(menu_items.children) if hasattr(menu_items, 'children') else '5'} pulsanti")
    
    def mostra_home_e_chiudi(self, widget):
        """Mostra home e chiude l'overlay"""
        print("🏠 DEBUG MENU: Navigazione a HOME dall'overlay")
        # Prima chiudo l'overlay, poi navigo con contenuto aggiornato
        if self.sidebar_visible:
            print("🏠 DEBUG MENU: Chiusura overlay prima della navigazione")
            self.toggle_sidebar(None)
        print("🏠 DEBUG MENU: Chiamata mostra_home")
        self.mostra_home(widget)
    
    def mostra_giocatori_e_chiudi(self, widget):
        """Mostra giocatori e chiude l'overlay"""
        print("👥 DEBUG MENU: Navigazione a GIOCATORI dall'overlay")
        # Prima chiudo l'overlay, poi navigo con contenuto aggiornato
        if self.sidebar_visible:
            print("👥 DEBUG MENU: Chiusura overlay prima della navigazione")
            self.toggle_sidebar(None)
        print("👥 DEBUG MENU: Chiamata mostra_giocatori")
        self.mostra_giocatori(widget)
    
    def mostra_partite_e_chiudi(self, widget):
        """Mostra partite e chiude l'overlay"""
        print("🏀 DEBUG MENU: Navigazione a PARTITE dall'overlay")
        # Prima chiudo l'overlay, poi navigo con contenuto aggiornato
        if self.sidebar_visible:
            print("🏀 DEBUG MENU: Chiusura overlay prima della navigazione")
            self.toggle_sidebar(None)
        print("🏀 DEBUG MENU: Chiamata mostra_partite")
        self.mostra_partite(widget)
    
    def mostra_allenamenti_e_chiudi(self, widget):
        """Mostra allenamenti e chiude l'overlay"""
        print("💪 DEBUG MENU: Navigazione a ALLENAMENTI dall'overlay")
        # Prima chiudo l'overlay, poi navigo
        if self.sidebar_visible:
            print("💪 DEBUG MENU: Chiusura overlay prima della navigazione")
            self.toggle_sidebar(None)
        print("💪 DEBUG MENU: Chiamata mostra_allenamenti")
        self.mostra_allenamenti(widget)
    
    def mostra_statistiche_e_chiudi(self, widget):
        """Mostra statistiche e chiude l'overlay"""
        print("📊 DEBUG MENU: Navigazione a STATISTICHE dall'overlay")
        # Prima chiudo l'overlay, poi navigo
        if self.sidebar_visible:
            print("📊 DEBUG MENU: Chiusura overlay prima della navigazione")
            self.toggle_sidebar(None)
        print("📊 DEBUG MENU: Chiamata mostra_statistiche")
        self.mostra_statistiche(widget)
    
    def aggiorna_menu_attivo(self, pagina):
        """Aggiorna lo stile del menu per evidenziare la pagina attiva"""
        # Reset tutti i pulsanti allo stile normale
        buttons = [
            (self.btn_home, "#34495e"),
            (self.btn_giocatori, "#2e7d32"),
            (self.btn_partite, "#ffc107"),
            (self.btn_allenamenti, "#f57c00"),
            (self.btn_statistiche, "#7b1fa2")
        ]
        
        for btn, color in buttons:
            btn.style.background_color = color
            # Reset colore testo per pulsante partite
            if btn == self.btn_partite:
                btn.style.color = "#000000"
            else:
                btn.style.color = "#ffffff"
        
        # Evidenzia il pulsante attivo
        if pagina == "home":
            self.btn_home.style.background_color = "#5d6d7e"
        elif pagina == "giocatori":
            self.btn_giocatori.style.background_color = "#4caf50"
        elif pagina == "partite":
            self.btn_partite.style.background_color = "#ffeb3b"
        elif pagina == "allenamenti":
            self.btn_allenamenti.style.background_color = "#ff9800"
        elif pagina == "statistiche":
            self.btn_statistiche.style.background_color = "#9c27b0"
    
    def mostra_home(self, widget):
        """Mostra la pagina home"""
        print("🏠 DEBUG NAV: Inizio caricamento pagina HOME")
        self.pagina_corrente = "home"
        self.aggiorna_menu_attivo("home")
        self.top_bar_title.text = "🏠 HOME"
        print("🏠 DEBUG NAV: Titolo aggiornato, caricamento contenuto...")
        
        # Pulisce il contenuto
        self.dynamic_content.clear()
        
        # Dashboard Home
        dashboard_container = toga.Box(style=Pack(direction=COLUMN, padding=15))
        
        # Titolo Dashboard
        dashboard_title = toga.Label(
            "🏀 DASHBOARD JBK",
            style=Pack(
                font_size=self.config['title_font_size'],
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                padding=(0, 0, 15, 0)
            )
        )
        dashboard_container.add(dashboard_title)
        
        # Container per sezioni della dashboard
        sections_container = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        # SEZIONE 1: Impegni Settimanali (parte superiore)
        impegni_section = self.crea_sezione_impegni_settimanali()
        sections_container.add(impegni_section)
        
        # SEZIONE 2: Container orizzontale per Valutazione e Statistiche
        row_container = toga.Box(style=Pack(direction=ROW, padding=5))
        
        # Valutazione Media Squadra (colonna sinistra)
        valutazione_section = self.crea_sezione_valutazione_squadra()
        row_container.add(valutazione_section)
        
        # Statistiche Totali Squadra (colonna destra)
        statistiche_section = self.crea_sezione_statistiche_squadra()
        row_container.add(statistiche_section)
        
        sections_container.add(row_container)
        
        dashboard_container.add(sections_container)
        self.dynamic_content.add(dashboard_container)
        print("🏠 DEBUG NAV: Dashboard HOME aggiunta a dynamic_content")

    def crea_sezione_impegni_settimanali(self):
        """Crea la sezione degli impegni settimanali"""
        section = toga.Box(style=Pack(
            direction=COLUMN,
            padding=10,
            background_color="#ffffff"
        ))
        
        # Titolo sezione
        title = toga.Label(
            "📅 IMPEGNI SETTIMANALI",
            style=Pack(
                font_size=16,
                font_weight="bold",
                color="#2c3e50",
                padding=8,
                background_color="#ecf0f1",
                text_align=CENTER
            )
        )
        section.add(title)
        
        # Container per impegni
        impegni_container = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        try:
            # Prossimi allenamenti (prossimi 7 giorni)
            from datetime import datetime, timedelta
            oggi = datetime.now()
            settimana_prossima = oggi + timedelta(days=7)
            
            allenamenti_service = AllenamentiService(self.db_manager)
            partite_service = PartiteService(self.db_manager)
            
            tutti_allenamenti = allenamenti_service.ottieni_tutti_allenamenti()
            tutte_partite = partite_service.ottieni_tutte_partite()
            
            # Filtra allenamenti nella prossima settimana
            impegni_settimana = []
            
            for allenamento in tutti_allenamenti:
                try:
                    data_allenamento = datetime.strptime(allenamento['data'], '%Y-%m-%d')
                    if oggi <= data_allenamento <= settimana_prossima:
                        impegni_settimana.append({
                            'tipo': '🏃 ALLENAMENTO',
                            'data': allenamento['data'],
                            'ora': allenamento.get('ora', ''),
                            'luogo': allenamento.get('luogo', 'Palestra')
                        })
                except:
                    pass
            
            # Filtra partite nella prossima settimana
            for partita in tutte_partite:
                try:
                    data_partita = datetime.strptime(partita['data'], '%Y-%m-%d')
                    if oggi <= data_partita <= settimana_prossima:
                        impegni_settimana.append({
                            'tipo': '⚽ PARTITA',
                            'data': partita['data'],
                            'ora': partita.get('ora', ''),
                            'luogo': partita.get('luogo', ''),
                            'avversario': partita.get('avversario', 'TBD')
                        })
                except:
                    pass
            
            # Se non ci sono partite nella prossima settimana, mostra le prossime 3 partite future
            if not any(imp['tipo'] == '⚽ PARTITA' for imp in impegni_settimana):
                partite_future = []
                for partita in tutte_partite:
                    try:
                        data_partita = datetime.strptime(partita['data'], '%Y-%m-%d')
                        if data_partita >= oggi:
                            partite_future.append((data_partita, partita))
                    except:
                        pass
                
                # Ordina per data e prendi le prime 3
                partite_future.sort(key=lambda x: x[0])
                for data_partita, partita in partite_future[:2]:  # Mostra max 2 partite future
                    impegni_settimana.append({
                        'tipo': '⚽ PARTITA',
                        'data': partita['data'],
                        'ora': partita.get('ora', ''),
                        'luogo': partita.get('luogo', ''),
                        'avversario': partita.get('avversario', 'TBD')
                    })
            
            # Ordina per data
            impegni_settimana.sort(key=lambda x: x['data'])
            
            if impegni_settimana:
                for impegno in impegni_settimana[:5]:  # Mostra max 5 impegni
                    impegno_text = f"{impegno['tipo']} - {impegno['data']}"
                    if impegno.get('ora'):
                        impegno_text += f" ore {impegno['ora']}"
                    if impegno.get('luogo'):
                        impegno_text += f" @ {impegno['luogo']}"
                    if impegno.get('avversario'):
                        impegno_text += f" vs {impegno['avversario']}"
                    
                    impegno_label = toga.Label(
                        impegno_text,
                        style=Pack(
                            font_size=12,
                            color="#34495e",
                            padding=3,
                            text_align=CENTER
                        )
                    )
                    impegni_container.add(impegno_label)
            else:
                no_impegni = toga.Label(
                    "Nessun impegno nei prossimi 7 giorni",
                    style=Pack(
                        font_size=12,
                        color="#7f8c8d",
                        padding=10,
                        font_style="italic",
                        text_align=CENTER
                    )
                )
                impegni_container.add(no_impegni)
                
        except Exception as e:
            error_label = toga.Label(
                f"Errore caricamento impegni: {str(e)[:50]}...",
                style=Pack(
                    font_size=10, 
                    color="#e74c3c", 
                    padding=5,
                    text_align=CENTER
                )
            )
            impegni_container.add(error_label)
        
        section.add(impegni_container)
        return section

    def crea_sezione_valutazione_squadra(self):
        """Crea la sezione della valutazione media squadra"""
        section = toga.Box(style=Pack(
            direction=COLUMN,
            padding=10,
            flex=1,  # Prende metà dello spazio orizzontale
            background_color="#ffffff"
        ))
        
        # Titolo sezione
        title = toga.Label(
            "⭐ VALUTAZIONE MEDIA SQUADRA",
            style=Pack(
                font_size=16,
                font_weight="bold",
                color="#2c3e50",
                padding=8,
                background_color="#e8f5e8"
            )
        )
        section.add(title)
        
        # Container per valutazione
        valutazione_container = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        try:
            # Calcola valutazione media di tutti i giocatori
            giocatori_service = GiocatoriService(self.db_manager)
            tutti_giocatori = giocatori_service.ottieni_tutti_giocatori()
            
            if tutti_giocatori:
                valutazioni_giocatori = []
                giocatori_valutati = 0
                
                for giocatore in tutti_giocatori:
                    statistiche = self.calcola_statistiche_giocatore(giocatore['id'])
                    valutazione = self.calcola_valutazione_media(statistiche)
                    if valutazione > 0:
                        valutazioni_giocatori.append(valutazione)
                        giocatori_valutati += 1
                
                if valutazioni_giocatori:
                    valutazione_media = sum(valutazioni_giocatori) / len(valutazioni_giocatori)
                    
                    # Valutazione principale
                    val_label = toga.Label(
                        f"VALUTAZIONE: {valutazione_media:.1f}/10.0",
                        style=Pack(
                            font_size=18,
                            font_weight="bold",
                            color="#27ae60" if valutazione_media >= 6 else "#e74c3c",
                            text_align=CENTER,
                            padding=10
                        )
                    )
                    valutazione_container.add(val_label)
                    
                    # Dettagli
                    dettagli = toga.Label(
                        f"Basata su {giocatori_valutati} giocatori attivi",
                        style=Pack(
                            font_size=12,
                            color="#7f8c8d",
                            text_align=CENTER,
                            padding=5
                        )
                    )
                    valutazione_container.add(dettagli)
                else:
                    no_val = toga.Label(
                        "Nessuna valutazione disponibile",
                        style=Pack(font_size=12, color="#7f8c8d", padding=10)
                    )
                    valutazione_container.add(no_val)
            else:
                no_giocatori = toga.Label(
                    "Nessun giocatore registrato",
                    style=Pack(font_size=12, color="#7f8c8d", padding=10)
                )
                valutazione_container.add(no_giocatori)
                
        except Exception as e:
            error_label = toga.Label(
                f"Errore calcolo valutazione: {str(e)[:50]}...",
                style=Pack(font_size=10, color="#e74c3c", padding=5)
            )
            valutazione_container.add(error_label)
        
        section.add(valutazione_container)
        return section

    def crea_sezione_statistiche_squadra(self):
        """Crea la sezione delle statistiche totali squadra"""
        section = toga.Box(style=Pack(
            direction=COLUMN,
            padding=10,
            flex=1,  # Prende metà dello spazio orizzontale
            background_color="#ffffff"
        ))
        
        # Titolo sezione
        title = toga.Label(
            "📊 STATISTICHE TOTALI SQUADRA",
            style=Pack(
                font_size=16,
                font_weight="bold",
                color="#2c3e50",
                padding=8,
                background_color="#fff3e0"
            )
        )
        section.add(title)
        
        # Container per statistiche
        stats_container = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        try:
            # Raccogli statistiche totali
            giocatori_service = GiocatoriService(self.db_manager)
            allenamenti_service = AllenamentiService(self.db_manager)
            partite_service = PartiteService(self.db_manager)
            
            # Conteggi base
            totale_giocatori = len(giocatori_service.ottieni_tutti_giocatori())
            totale_allenamenti = len(allenamenti_service.ottieni_tutti_allenamenti())
            totale_partite = len(partite_service.ottieni_tutte_partite())
            
            # Statistiche aggregate
            stats_text = f"""📈 RIEPILOGO GENERALE:
            
👥 Giocatori Registrati: {totale_giocatori}
🏃 Allenamenti Programmati: {totale_allenamenti}  
⚽ Partite in Calendario: {totale_partite}

📊 PERFORMANCE SQUADRA:"""
            
            # Calcola statistiche aggregate
            presenze_totali = 0
            assenze_totali = 0
            convocazioni_totali = 0
            
            tutti_giocatori = giocatori_service.ottieni_tutti_giocatori()
            for giocatore in tutti_giocatori:
                statistiche = self.calcola_statistiche_giocatore(giocatore['id'])
                presenze_totali += statistiche['presenze']
                assenze_totali += statistiche['assenze']
                convocazioni_totali += statistiche.get('convocazioni', 0)
            
            if totale_allenamenti > 0 and totale_giocatori > 0:
                percentuale_presenze_media = (presenze_totali / (totale_allenamenti * totale_giocatori)) * 100
                stats_text += f"\n🏃 Presenze Medie: {percentuale_presenze_media:.1f}%"
            
            if totale_partite > 0 and totale_giocatori > 0:
                percentuale_convocazioni_media = (convocazioni_totali / (totale_partite * totale_giocatori)) * 100
                stats_text += f"\n⚽ Convocazioni Medie: {percentuale_convocazioni_media:.1f}%"
            
            stats_label = toga.Label(
                stats_text,
                style=Pack(
                    font_size=12,
                    color="#2c3e50",
                    padding=10
                )
            )
            stats_container.add(stats_label)
            
        except Exception as e:
            error_label = toga.Label(
                f"Errore caricamento statistiche: {str(e)[:50]}...",
                style=Pack(font_size=10, color="#e74c3c", padding=5)
            )
            stats_container.add(error_label)
        
        section.add(stats_container)
        return section
    
    def mostra_giocatori(self, widget):
        """Mostra la pagina gestione giocatori"""
        print("👥 DEBUG NAV: Inizio caricamento pagina GIOCATORI")
        self.pagina_corrente = "giocatori"
        self.aggiorna_menu_attivo("giocatori")
        self.top_bar_title.text = "👥 GESTIONE GIOCATORI"
        print("👥 DEBUG NAV: Titolo aggiornato, caricamento contenuto...")
        
        # Pulisce il contenuto
        self.dynamic_content.clear()
        
        # Crea l'interfaccia giocatori
        self.dynamic_content.add(self.crea_interfaccia_giocatori())
    
    def crea_interfaccia_giocatori(self):
        """Crea l'interfaccia per la gestione giocatori"""
        container = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        
        # Pulsanti azioni con dimensioni responsive
        actions_box = toga.Box(style=Pack(direction=ROW, padding=self.config['padding_medium']))
        btn_aggiungi = toga.Button(
            "➕ Aggiungi Giocatore",
            on_press=self.apri_dialog_giocatore,
            style=Pack(
                padding=self.config['padding_medium'], 
                height=self.config['button_height'],
                background_color="#4caf50", 
                color="#ffffff",
                font_size=self.config['button_font_size'],
                flex=1
            )
        )
        btn_lista = toga.Button(
            "📋 Lista Giocatori",
            on_press=self.mostra_lista_giocatori,
            style=Pack(
                padding=self.config['padding_medium'], 
                height=self.config['button_height'],
                background_color="#2196f3", 
                color="#ffffff",
                font_size=self.config['button_font_size'],
                flex=1
            )
        )
        actions_box.add(btn_aggiungi)
        actions_box.add(btn_lista)
        container.add(actions_box)
        
        # Area contenuto dinamica
        self.giocatori_content = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        # Container scroll per i giocatori
        self.giocatori_scroll = toga.ScrollContainer(
            content=self.giocatori_content,
            style=Pack(flex=1, height=500)  # Altezza minima per riempire la pagina
        )
        container.add(self.giocatori_scroll)
        
        # Mostra lista giocatori di default
        self.aggiorna_lista_giocatori()
        
        # Controlla idoneità scadute
        self.controlla_idoneita_scadute()
        
        return container
    

    def mostra_lista_giocatori(self, widget):
        """Mostra la lista dei giocatori"""
        self.aggiorna_lista_giocatori()
    
    def aggiorna_lista_giocatori(self):
        """Aggiorna la lista dei giocatori nell'interfaccia"""
        self.giocatori_content.clear()
        
        # Ottieni lista giocatori
        giocatori = self.giocatori_service.get_all()
        
        if not giocatori:
            self.giocatori_content.add(toga.Label(
                "Nessun giocatore registrato.",
                style=Pack(padding=20, font_size=14, color="#666666")
            ))
            return
        
        # Crea tabella giocatori
        for giocatore in giocatori:
            player_box = toga.Box(
                style=Pack(
                    direction=ROW,
                    padding=self.config['padding_medium'],
                    background_color="#f5f5f5",
                    height=self.config['row_height']  # Altezza fissa per righe più grandi
                )
            )
            
            numero_text = f"#{giocatore['numero_maglia']}" if giocatore['numero_maglia'] else "N/A"
            data_nascita_text = f"Data: {giocatore['data_nascita']}" if giocatore.get('data_nascita') else "Data: N/A"
            
            # Determina stato idoneità con controllo scadenza
            stato_idoneita = self.get_stato_idoneita_giocatore(giocatore)
            if stato_idoneita == "Idoneo":
                idoneita_text = "✅ Idoneo"
                idoneita_color = "#4caf50"
            elif stato_idoneita == "Scaduto":
                idoneita_text = "⚠️ Scaduto"
                idoneita_color = "#ff9800"
            else:
                idoneita_text = "❌ Non idoneo"
                idoneita_color = "#f44336"
            
            info_text = f"{numero_text} - {giocatore['nome']} {giocatore['cognome']} - {data_nascita_text} - {idoneita_text}"
            
            info_label = toga.Label(
                info_text,
                style=Pack(
                    flex=1, 
                    padding=self.config['padding_small'],
                    font_size=self.config['label_font_size']
                )
            )
            
            btn_modifica = toga.Button(
                "✏️",
                on_press=lambda w, id=giocatore['id']: self.apri_dialog_giocatore(None, id),
                style=Pack(padding=2, background_color="#2196f3", color="#ffffff", width=40)
            )
            
            btn_elimina = toga.Button(
                "🗑️",
                on_press=lambda w, id=giocatore['id']: self.elimina_giocatore(id),
                style=Pack(padding=2, background_color="#f44336", color="#ffffff", width=40)
            )
            
            player_box.add(info_label)
            player_box.add(btn_modifica)
            player_box.add(btn_elimina)
            self.giocatori_content.add(player_box)
    
    def get_stato_idoneita_giocatore(self, giocatore):
        """Determina lo stato dell'idoneità di un giocatore"""
        if not giocatore.get('idoneita_sportiva', False):
            return "Non Idoneo"
        
        if not giocatore.get('data_scadenza_idoneita'):
            return "Idoneo"  # Se non c'è data di scadenza, è idoneo
        
        try:
            from datetime import datetime
            # Prova prima il formato italiano GG/MM/AAAA
            try:
                data_scadenza = datetime.strptime(giocatore['data_scadenza_idoneita'], '%d/%m/%Y')
            except ValueError:
                # Fallback al formato ISO per compatibilità
                data_scadenza = datetime.strptime(giocatore['data_scadenza_idoneita'], '%Y-%m-%d')
            
            if datetime.now().date() > data_scadenza.date():
                return "Scaduto"
            else:
                return "Idoneo"
        except (ValueError, TypeError):
            return "Idoneo"  # In caso di errore nel parsing, considera idoneo
    
    def controlla_idoneita_scadute(self):
        """Controlla e notifica idoneità scadute"""
        giocatori = self.giocatori_service.get_all()
        scadute = []
        
        for giocatore in giocatori:
            if self.get_stato_idoneita_giocatore(giocatore) == "Scaduto":
                scadute.append(f"{giocatore['nome']} {giocatore['cognome']}")
        
        if scadute:
            nomi_scaduti = ", ".join(scadute)
            self.mostra_avviso(f"⚠️ Idoneità scadute per: {nomi_scaduti}")
    
    def apri_dialog_giocatore(self, widget, giocatore_id=None):
        """Apre un dialog per aggiungere/modificare un giocatore"""
        # Se stiamo modificando, carica i dati esistenti
        giocatore_data = None
        if giocatore_id:
            giocatore_data = self.giocatori_service.get_by_id(giocatore_id)
        
        # Crea una nuova finestra dialog
        dialog = toga.Window(
            title="Modifica Giocatore" if giocatore_id else "Nuovo Giocatore",
            size=(400, 500)
        )
        
        # Container principale del dialog
        dialog_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        
        # Campi del form
        nome_input = toga.TextInput(
            placeholder="Nome", 
            value=giocatore_data.get('nome', '') if giocatore_data else '',
            style=Pack(padding=5, width=300)
        )
        cognome_input = toga.TextInput(
            placeholder="Cognome", 
            value=giocatore_data.get('cognome', '') if giocatore_data else '',
            style=Pack(padding=5, width=300)
        )
        numero_input = toga.NumberInput(
            value=giocatore_data.get('numero_maglia') if giocatore_data and giocatore_data.get('numero_maglia') else None,
            style=Pack(padding=5, width=150)
        )
        anno_nascita_input = toga.NumberInput(
            value=giocatore_data.get('anno_nascita') if giocatore_data and giocatore_data.get('anno_nascita') else None,
            style=Pack(padding=5, width=150)
        )
        idoneita_input = toga.Switch(
            text="Idoneità Sportiva",
            value=giocatore_data.get('idoneita_sportiva', False) if giocatore_data else False,
            style=Pack(padding=5)
        )
        
        # Campo data scadenza idoneità (inizialmente nascosto)
        data_scadenza_label = toga.Label("Data Scadenza Idoneità:", style=Pack(padding=(10, 5, 0, 5)))
        
        # Converte la data dal database al formato italiano per la visualizzazione
        data_display = ""
        if giocatore_data and giocatore_data.get('data_scadenza_idoneita'):
            data_db = giocatore_data.get('data_scadenza_idoneita')
            try:
                from datetime import datetime
                # Se è già in formato italiano, la mantiene
                if '/' in data_db:
                    data_display = data_db
                else:
                    # Converte da formato ISO a italiano
                    data_obj = datetime.strptime(data_db, '%Y-%m-%d')
                    data_display = data_obj.strftime('%d/%m/%Y')
            except (ValueError, TypeError):
                data_display = data_db  # Mantiene il valore originale se non riesce a convertire
        
        data_scadenza_input = toga.TextInput(
            placeholder="GG/MM/AAAA", 
            value=data_display,
            style=Pack(padding=5, width=300)
        )
        
        # Inizialmente nascosti se idoneità non è attiva
        if not (giocatore_data and giocatore_data.get('idoneita_sportiva', False)):
            data_scadenza_label.style.visibility = "hidden"
            data_scadenza_input.style.visibility = "hidden"
        
        def on_idoneita_change(widget):
            """Mostra/nasconde il campo data scadenza in base all'idoneità"""
            if idoneita_input.value:
                data_scadenza_label.style.visibility = "visible"
                data_scadenza_input.style.visibility = "visible"
            else:
                data_scadenza_label.style.visibility = "hidden"  
                data_scadenza_input.style.visibility = "hidden"
                data_scadenza_input.value = ""
        
        idoneita_input.on_change = on_idoneita_change
        
        # Labels e campi
        dialog_box.add(toga.Label("Nome:", style=Pack(padding=(10, 5, 0, 5))))
        dialog_box.add(nome_input)
        dialog_box.add(toga.Label("Cognome:", style=Pack(padding=(10, 5, 0, 5))))
        dialog_box.add(cognome_input)
        dialog_box.add(toga.Label("Numero Maglia:", style=Pack(padding=(10, 5, 0, 5))))
        dialog_box.add(numero_input)
        dialog_box.add(toga.Label("Anno di Nascita:", style=Pack(padding=(10, 5, 0, 5))))
        dialog_box.add(anno_nascita_input)
        dialog_box.add(idoneita_input)
        dialog_box.add(data_scadenza_label)
        dialog_box.add(data_scadenza_input)
        
        # Pulsanti
        buttons_box = toga.Box(style=Pack(direction=ROW, padding=20))
        
        def salva_e_chiudi(widget):
            """Salva il giocatore e chiude il dialog"""
            try:
                # Validazione base
                if not nome_input.value or not cognome_input.value:
                    self.mostra_errore("Nome e cognome sono obbligatori")
                    return
                    
                # Validazione data scadenza se idoneità è attiva
                data_scadenza = None
                if idoneita_input.value:
                    if not data_scadenza_input.value:
                        self.mostra_errore("Data scadenza idoneità obbligatoria quando l'idoneità è attiva")
                        return
                    
                    # Validazione formato data (accetta formato italiano GG/MM/AAAA)
                    try:
                        from datetime import datetime
                        # Prova il formato italiano GG/MM/AAAA
                        data_obj = datetime.strptime(data_scadenza_input.value, '%d/%m/%Y')
                        # Salva nel database in formato italiano
                        data_scadenza = data_obj.strftime('%d/%m/%Y')
                    except ValueError:
                        self.mostra_errore("Formato data non valido. Usare GG/MM/AAAA (es. 31/12/2025)")
                        return
                
                # Crea il dizionario con i dati del giocatore
                giocatore_data_form = {
                    'nome': nome_input.value,
                    'cognome': cognome_input.value,
                    'numero_maglia': int(numero_input.value) if numero_input.value else None,
                    'anno_nascita': int(anno_nascita_input.value) if anno_nascita_input.value else None,
                    'idoneita_sportiva': idoneita_input.value,
                    'data_scadenza_idoneita': data_scadenza
                }
                
                # Controlla se stiamo modificando o creando
                if giocatore_id:
                    # Modifica giocatore esistente
                    self.giocatori_service.update(giocatore_id, giocatore_data_form)
                    self.mostra_successo("Giocatore modificato con successo!")
                else:
                    # Crea nuovo giocatore
                    self.giocatori_service.create(giocatore_data_form)
                    self.mostra_successo("Giocatore aggiunto con successo!")
                
                self.aggiorna_lista_giocatori()
                dialog.close()
                
            except Exception as e:
                self.mostra_errore(f"Errore nel salvare il giocatore: {str(e)}")
        
        btn_salva = toga.Button(
            "💾 Salva",
            on_press=salva_e_chiudi,
            style=Pack(padding=5, background_color="#4caf50", color="#ffffff")
        )
        btn_annulla = toga.Button(
            "❌ Annulla",
            on_press=lambda w: dialog.close(),
            style=Pack(padding=5, background_color="#f44336", color="#ffffff")
        )
        buttons_box.add(btn_salva)
        buttons_box.add(btn_annulla)
        
        dialog_box.add(buttons_box)
        dialog.content = dialog_box
        dialog.show()
    

    def elimina_giocatore(self, giocatore_id):
        """Elimina un giocatore"""
        try:
            self.giocatori_service.delete(giocatore_id)
            self.mostra_successo("Giocatore eliminato con successo!")
            self.aggiorna_lista_giocatori()
        except Exception as e:
            self.mostra_errore(f"Errore nell'eliminare il giocatore: {str(e)}")
    
    def mostra_partite(self, widget):
        """Mostra la pagina gestione partite"""
        print("🏀 DEBUG NAV: Inizio caricamento pagina PARTITE")
        self.pagina_corrente = "partite"
        self.aggiorna_menu_attivo("partite")
        self.top_bar_title.text = "🏀 GESTIONE PARTITE"
        print("🏀 DEBUG NAV: Titolo aggiornato, caricamento contenuto...")
        
        # Pulisce il contenuto
        self.dynamic_content.clear()
        
        # Inizializza tipologia corrente
        if not hasattr(self, 'tipologia_corrente'):
            self.tipologia_corrente = "tutte"
        
        # Crea l'interfaccia partite
        self.dynamic_content.add(self.crea_interfaccia_partite())
        print("🏀 DEBUG NAV: Contenuto PARTITE aggiunto a dynamic_content")
    
    def crea_interfaccia_partite(self):
        """Crea l'interfaccia per la gestione partite con sidebar"""
        container = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        
        # Tasti per tipologie partite con dimensioni responsive
        tipologie_box = toga.Box(style=Pack(direction=ROW, padding=self.config['padding_medium']))
        
        btn_pre_stagione = toga.Button(
            "🔥 Pre-stagione",
            on_press=lambda w: self.filtra_partite("pre-stagione"),
            style=Pack(
                padding=self.config['padding_small'], 
                height=self.config['button_height'],
                background_color="#ff9800", 
                color="#ffffff", 
                font_size=self.config['button_font_size'],
                flex=1
            )
        )
        btn_stagione_regolare = toga.Button(
            "🏆 Stagione Regolare", 
            on_press=lambda w: self.filtra_partite("stagione regolare"),
            style=Pack(
                padding=self.config['padding_small'], 
                height=self.config['button_height'],
                background_color="#4caf50", 
                color="#ffffff", 
                font_size=self.config['button_font_size'],
                flex=1
            )
        )
        btn_post_stagione = toga.Button(
            "🥇 Post-stagione",
            on_press=lambda w: self.filtra_partite("post-stagione"),
            style=Pack(
                padding=self.config['padding_small'], 
                height=self.config['button_height'],
                background_color="#2196f3", 
                color="#ffffff", 
                font_size=self.config['button_font_size'],
                flex=1
            )
        )
        btn_tornei = toga.Button(
            "🏅 Tornei",
            on_press=lambda w: self.filtra_partite("tornei"),
            style=Pack(
                padding=self.config['padding_small'], 
                height=self.config['button_height'],
                background_color="#9c27b0", 
                color="#ffffff", 
                font_size=self.config['button_font_size'],
                flex=1
            )
        )
        
        tipologie_box.add(btn_pre_stagione)
        tipologie_box.add(btn_stagione_regolare)
        tipologie_box.add(btn_post_stagione)
        tipologie_box.add(btn_tornei)
        container.add(tipologie_box)
        
        # Tasto per mostrare tutte le partite con dimensioni responsive
        btn_tutte = toga.Button(
            "📋 Tutte le Partite",
            on_press=lambda w: self.filtra_partite("tutte"),
            style=Pack(
                padding=self.config['padding_medium'], 
                height=self.config['button_height'],
                background_color="#607d8b", 
                color="#ffffff",
                font_size=self.config['button_font_size']
            )
        )
        container.add(btn_tutte)
        
        # Layout principale con due colonne
        main_layout = toga.Box(style=Pack(direction=ROW, padding=10, flex=1))
        
        # Colonna sinistra: Lista partite
        partite_column = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=2))
        partite_title = toga.Label(
            "📋 Elenco Partite", 
            style=Pack(padding=(0, 0, 10, 0), font_size=14, font_weight="bold")
        )
        partite_column.add(partite_title)
        
        # Area contenuto dinamica per le partite
        self.partite_content = toga.Box(style=Pack(direction=COLUMN, padding=5))
        
        # Container scroll per le partite
        self.partite_scroll = toga.ScrollContainer(
            content=self.partite_content,
            style=Pack(flex=1, height=400)  # Altezza minima per riempire la pagina
        )
        partite_column.add(self.partite_scroll)
        
        # Tasto per aggiungere una nuova partita sotto l'elenco
        btn_aggiungi = toga.Button(
            "➕ Aggiungi Partita",
            on_press=self.aggiungi_nuova_partita,
            style=Pack(
                padding=self.config['padding_medium'], 
                height=self.config['button_height'],
                background_color="#4caf50", 
                color="#ffffff",
                font_size=self.config['button_font_size']
            )
        )
        partite_column.add(btn_aggiungi)
        
        # Colonna destra: Sidebar giocatori e resoconti
        sidebar_column = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1, background_color="#f5f5f5"))
        self.crea_sidebar_giocatori(sidebar_column)
        
        main_layout.add(partite_column)
        main_layout.add(sidebar_column)
        container.add(main_layout)
        
        # Mostra tutte le partite di default
        self.filtra_partite("tutte")
        
        return container
    
    def crea_sidebar_giocatori(self, sidebar_container):
        """Crea la sidebar con giocatori e convocazioni"""
        # Titolo sidebar
        sidebar_title = toga.Label(
            "👥 Convocazioni",
            style=Pack(padding=(0, 0, 15, 0), font_size=14, font_weight="bold")
        )
        sidebar_container.add(sidebar_title)
        
        # Area scrollabile per giocatori con statistiche
        self.sidebar_giocatori_content = toga.Box(style=Pack(direction=COLUMN, padding=2))
        
        # Container scroll per sidebar giocatori
        self.sidebar_scroll = toga.ScrollContainer(
            content=self.sidebar_giocatori_content,
            style=Pack(flex=1, height=400)  # Altezza minima per riempire la sidebar
        )
        sidebar_container.add(self.sidebar_scroll)
        
        # Aggiorna contenuto sidebar
        self.aggiorna_sidebar()
    
    def aggiorna_sidebar(self):
        """Aggiorna il contenuto della sidebar con convocazioni"""
        try:
            # Pulisci contenuti esistenti
            self.sidebar_giocatori_content.clear()
            
            # Ottieni giocatori e partite
            giocatori = self.giocatori_service.get_all()
            partite = self.partite_service.ottieni_tutte_partite()
            
            if not giocatori:
                no_giocatori_label = toga.Label(
                    "Nessun giocatore registrato",
                    style=Pack(padding=5, color="#666666", font_size=10)
                )
                self.sidebar_giocatori_content.add(no_giocatori_label)
                return
            
            # Mostra convocazioni per ogni giocatore
            for giocatore in giocatori:
                giocatore_box = toga.Box(style=Pack(
                    direction=ROW, 
                    padding=self.config['padding_small'],
                    height=self.config['row_height']
                ))
                
                # Info giocatore
                numero = f"#{giocatore['numero_maglia']}" if giocatore['numero_maglia'] else "#--"
                nome_breve = f"{giocatore['nome']}"
                cognome_breve = giocatore['cognome']
                
                # Trunca i nomi se troppo lunghi
                if len(nome_breve) > 8:
                    nome_breve = nome_breve[:7] + "."
                if len(cognome_breve) > 8:
                    cognome_breve = cognome_breve[:7] + "."
                
                # Indicatore idoneità
                stato_idoneita = self.get_stato_idoneita_giocatore(giocatore)
                if stato_idoneita == "Idoneo":
                    idoneita_icon = "✅"
                elif stato_idoneita == "Scaduto":
                    idoneita_icon = "⚠️"
                else:
                    idoneita_icon = "❌"
                
                # Calcola convocazioni per questo giocatore
                convocazioni_giocatore = 0
                for partita in partite:
                    convocati = self.convocati_service.ottieni_convocati_partita(partita['id'])
                    if any(c['giocatore_id'] == giocatore['id'] for c in convocati):
                        convocazioni_giocatore += 1
                
                # Etichetta giocatore con dimensioni responsive
                giocatore_text = f"{idoneita_icon} {numero} {nome_breve} {cognome_breve}"
                giocatore_label = toga.Label(
                    giocatore_text,
                    style=Pack(
                        flex=2, 
                        font_size=self.config['label_font_size'] - 2, 
                        padding=self.config['padding_small']
                    )
                )
                
                # Etichetta convocazioni con dimensioni responsive
                convocazioni_label = toga.Label(
                    str(convocazioni_giocatore),
                    style=Pack(
                        width=50, 
                        font_size=self.config['label_font_size'] - 2, 
                        padding=self.config['padding_small'], 
                        text_align=CENTER
                    )
                )
                
                giocatore_box.add(giocatore_label)
                giocatore_box.add(convocazioni_label)
                self.sidebar_giocatori_content.add(giocatore_box)
            
        except Exception as e:
            error_label = toga.Label(
                f"Errore aggiornamento sidebar: {str(e)[:30]}...",
                style=Pack(padding=5, color="#f44336", font_size=10)
            )
            self.sidebar_giocatori_content.add(error_label)
    

    def filtra_partite(self, tipologia):
        """Filtra le partite per tipologia"""
        # Salva la tipologia corrente per l'aggiunta di nuove partite
        self.tipologia_corrente = tipologia
        self.partite_content.clear()
        
        try:
            if tipologia == "tutte":
                partite = self.partite_service.ottieni_tutte_partite()
                title = "📋 Tutte le Partite"
            else:
                partite = self.partite_service.ottieni_partite_per_tipologia(tipologia)
                title_map = {
                    "pre-stagione": "🔥 Partite Pre-stagione",
                    "stagione regolare": "🏆 Partite Stagione Regolare",
                    "post-stagione": "🥇 Partite Post-stagione",
                    "tornei": "🏅 Partite Tornei"
                }
                title = title_map.get(tipologia, f"📋 Partite {tipologia.title()}")
            
            # Titolo sezione
            title_label = toga.Label(
                title,
                style=Pack(font_size=18, font_weight="bold", padding=(10, 5))
            )
            self.partite_content.add(title_label)
            
            if not partite:
                # Nessuna partita trovata
                no_partite_label = toga.Label(
                    f"Nessuna partita trovata per '{tipologia}'",
                    style=Pack(font_style="italic", padding=20, text_align=CENTER)
                )
                self.partite_content.add(no_partite_label)
            else:
                # Mostra le partite
                for partita in partite:
                    self.aggiungi_partita_alla_lista(partita)
            
            # Aggiorna la sidebar quando cambiano i filtri
            if hasattr(self, 'sidebar_giocatori_content'):
                self.aggiorna_sidebar()
                    
        except Exception as e:
            error_label = toga.Label(
                f"Errore nel caricamento delle partite: {str(e)}",
                style=Pack(color="#f44336", padding=10)
            )
            self.partite_content.add(error_label)
    
    def aggiungi_partita_alla_lista(self, partita):
        """Aggiunge una partita alla lista visualizzata"""
        partita_box = toga.Box(style=Pack(
            direction=ROW, 
            padding=self.config['padding_medium'],
            height=self.config['row_height']  # Altezza fissa per righe più grandi
        ))
        
        # Icona casa/trasferta
        casa_icon = "🏠" if partita.get('in_casa', True) else "✈️"
        
        # Prefisso casa/trasferta per avversario
        vs_prefix = "vs" if partita.get('in_casa', True) else "@"
        
        # Formatta risultato se presente
        risultato = ""
        if partita.get('risultato_nostro') is not None and partita.get('risultato_avversario') is not None:
            risultato = f" ({partita['risultato_nostro']}-{partita['risultato_avversario']})"
        
        # Colore per tipologia
        tipologia_colors = {
            "pre-stagione": "#ff9800",
            "stagione regolare": "#4caf50", 
            "post-stagione": "#2196f3",
            "tornei": "#9c27b0"
        }
        tipologia_color = tipologia_colors.get(partita.get('tipologia', 'stagione regolare'), "#607d8b")
        
        # Box per informazioni partita (due righe)
        info_box = toga.Box(style=Pack(direction=COLUMN, flex=1, padding=self.config['padding_small']))
        
        # Prima riga: icona, vs/@ avversario e risultato
        prima_riga_text = f"{casa_icon} {vs_prefix} {partita['avversario']}{risultato}"
        prima_riga_label = toga.Label(
            prima_riga_text,
            style=Pack(
                font_size=self.config['label_font_size'],
                font_weight="bold"
            )
        )
        
        # Seconda riga: data e ora (carattere più piccolo)
        seconda_riga_text = f"📅 {partita['data']} ⏰ {partita['ora']}"
        seconda_riga_label = toga.Label(
            seconda_riga_text,
            style=Pack(
                font_size=self.config['label_font_size'] - 3,
                color="#666666"
            )
        )
        
        info_box.add(prima_riga_label)
        info_box.add(seconda_riga_label)
        
        # Badge tipologia
        tipologia_label = toga.Label(
            partita.get('tipologia', 'stagione regolare').title(),
            style=Pack(
                padding=self.config['padding_small'], 
                background_color=tipologia_color, 
                color="#ffffff",
                font_size=self.config['label_font_size'] - 2
            )
        )
        
        # Pulsante convocati
        def on_convocati_press(widget, partita_data=partita):
            print(f"🔍 DEBUG: Pulsante convocati premuto!")
            print(f"� DEBUG: Widget: {widget}")
            print(f"🔍 DEBUG: Partita passata: {partita_data}")
            self.gestisci_convocati(partita_data)
        
        convocati_button = toga.Button(
            "👥",
            on_press=on_convocati_press,
            style=Pack(
                padding=self.config['padding_small'],
                width=self.config['touch_target_min'],
                height=self.config['touch_target_min'],
                background_color="#673ab7",
                color="#ffffff",
                font_size=self.config['button_font_size']
            )
        )
        
        # Pulsante statistiche
        def on_statistiche_press(widget, partita_data=partita):
            print(f"📊 DEBUG: Pulsante statistiche premuto!")
            print(f"📊 DEBUG: Partita: {partita_data}")
            self.gestisci_statistiche_partita(partita_data)
        
        statistiche_button = toga.Button(
            "📊",
            on_press=on_statistiche_press,
            style=Pack(
                padding=self.config['padding_small'],
                width=self.config['touch_target_min'],
                height=self.config['touch_target_min'],
                background_color="#4caf50",
                color="#ffffff",
                font_size=self.config['button_font_size']
            )
        )
        
        # Pulsante modifica
        def on_modifica_press(widget, partita_data=partita):
            print(f"✏️ DEBUG: Pulsante modifica premuto!")
            print(f"✏️ DEBUG: Partita: {partita_data}")
            self.modifica_partita(partita_data)
        
        modifica_button = toga.Button(
            "✏️",
            on_press=on_modifica_press,
            style=Pack(
                padding=self.config['padding_small'],
                width=self.config['touch_target_min'],
                height=self.config['touch_target_min'],
                background_color="#ff9800",
                color="#ffffff",
                font_size=self.config['button_font_size']
            )
        )
        
        partita_box.add(info_box)
        partita_box.add(tipologia_label)
        partita_box.add(convocati_button)
        partita_box.add(statistiche_button)
        partita_box.add(modifica_button)
        self.partite_content.add(partita_box)
    
    def mostra_allenamenti(self, widget):
        """Mostra la pagina gestione allenamenti con calendario interattivo"""
        print("💪 DEBUG NAV: Inizio caricamento pagina ALLENAMENTI")
        self.pagina_corrente = "allenamenti"
        self.aggiorna_menu_attivo("allenamenti")
        self.top_bar_title.text = "💪 GESTIONE ALLENAMENTI"
        print("💪 DEBUG NAV: Titolo aggiornato, caricamento contenuto...")
        
        # Pulisce il contenuto
        self.dynamic_content.clear()
        
        # Crea l'interfaccia allenamenti con calendario
        self.dynamic_content.add(self.crea_interfaccia_allenamenti())
        print("💪 DEBUG NAV: Contenuto ALLENAMENTI aggiunto a dynamic_content")
    
    def crea_interfaccia_allenamenti(self):
        """Crea l'interfaccia per la gestione degli allenamenti con calendario"""
        print("📅 DEBUG CALENDAR: Creazione interfaccia allenamenti iniziata")
        
        container = toga.Box(style=Pack(direction=COLUMN, padding=8, flex=1))  # Padding ridotto per layout compatto
        
        # Header con controlli settimana con stile consistente
        header_box = toga.Box(style=Pack(direction=ROW, padding=self.config['padding_medium']))
        
        # Inizializza data corrente (lunedì della settimana corrente)
        today = datetime.now()
        days_since_monday = today.weekday()
        self.settimana_corrente = today - timedelta(days=days_since_monday)
        
        # Pulsanti navigazione settimana con stile consistente
        btn_settimana_prec = toga.Button(
            "‹",
            on_press=self.vai_settimana_precedente,
            style=Pack(
                padding=self.config['padding_medium'],
                background_color="#34495e",
                color="#ffffff",
                font_size=self.config['button_font_size'] + 4,
                width=80,
                height=self.config['button_height'],
                font_weight="bold"
            )
        )
        
        self.label_settimana = toga.Label(
            self.get_nome_settimana(),
            style=Pack(
                font_size=self.config['title_font_size'],
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                flex=1,
                padding=self.config['padding_medium']
            )
        )
        
        btn_settimana_succ = toga.Button(
            "›",
            on_press=self.vai_settimana_successiva,
            style=Pack(
                padding=self.config['padding_medium'],
                background_color="#34495e",
                color="#ffffff",
                font_size=self.config['button_font_size'] + 4,
                width=80,
                height=self.config['button_height'],
                font_weight="bold"
            )
        )
        
        header_box.add(btn_settimana_prec)
        header_box.add(self.label_settimana)
        header_box.add(btn_settimana_succ)
        container.add(header_box)
        
        # Container principale con due colonne
        main_content = toga.Box(style=Pack(direction=ROW, padding=self.config['padding_medium'], flex=1))
        
        # Colonna sinistra: Calendario settimanale + Statistiche presenze (ridotta)
        calendario_column = toga.Box(style=Pack(direction=COLUMN, padding=self.config['padding_medium'], flex=3))
        
        # Calendario settimanale
        self.calendario_box = toga.Box(style=Pack(direction=COLUMN, padding=self.config['padding_medium']))
        calendario_column.add(self.calendario_box)
        
        # Colonna destra: Lista allenamenti della settimana
        lista_column = toga.Box(style=Pack(direction=COLUMN, padding=self.config['padding_medium'], flex=2))
        
        # Titolo lista allenamenti
        lista_title = toga.Label(
            "📋 ALLENAMENTI SETTIMANA",
            style=Pack(
                font_size=self.config['button_font_size'],
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                padding=self.config['padding_medium'],
                background_color="#ecf0f1"
            )
        )
        lista_column.add(lista_title)
        
        # Container scrollabile compatto per la lista allenamenti
        self.lista_allenamenti_box = toga.ScrollContainer(
            style=Pack(
                flex=1,
                padding=5,  # Padding ridotto per layout compatto
                height=600  # Altezza fissa
            )
        )
        
        # Box interno per gli allenamenti
        self.lista_allenamenti_content = toga.Box(style=Pack(direction=COLUMN, padding=self.config['padding_small']))
        self.lista_allenamenti_box.content = self.lista_allenamenti_content
        
        # Carica tutti gli allenamenti
        self.aggiorna_lista_tutti_allenamenti()
        
        lista_column.add(self.lista_allenamenti_box)
        
        # Aggiungi le colonne al container principale
        main_content.add(calendario_column)
        main_content.add(lista_column)
        container.add(main_content)
        
        # Sezione statistiche presenze compatta che si estende su tutta la larghezza
        self.statistiche_presenze_box = toga.ScrollContainer(
            style=Pack(
                height=400,  # Altezza mantenuta
                padding=5,  # Padding ridotto per layout compatto
                background_color="#f8f9fa"  # Sfondo mantenuto
            )
        )
        
        # Box interno per le statistiche con layout orizzontale per utilizzare tutto lo spazio
        self.statistiche_presenze_content = toga.Box(style=Pack(
            direction=COLUMN, 
            padding=self.config['padding_small'],
            background_color="#ffffff"
        ))
        
        # Aggiungi un indicatore che la sezione statistiche è presente
        test_label = toga.Label(
            "🔍 SEZIONE STATISTICHE CARICATA - Se vedi questo messaggio, la sezione funziona",
            style=Pack(
                font_size=self.config['label_font_size'],
                color="#e74c3c",
                text_align=CENTER,
                padding=self.config['padding_medium'],
                background_color="#fff3cd"
            )
        )
        self.statistiche_presenze_content.add(test_label)
        
        self.statistiche_presenze_box.content = self.statistiche_presenze_content
        
        container.add(self.statistiche_presenze_box)
        
        # Ora che tutti i container sono creati, aggiorna il calendario e le statistiche
        self.aggiorna_calendario_settimanale()
        self.aggiorna_statistiche_presenze()
        
        print("📅 DEBUG CALENDAR: Interfaccia allenamenti creata con lista laterale e statistiche presenze estese")
        return container
    
    def get_nome_settimana(self):
        """Genera il nome della settimana corrente"""
        inizio = self.settimana_corrente
        fine = inizio + timedelta(days=6)
        return f"Settimana {inizio.strftime('%d/%m')} - {fine.strftime('%d/%m/%Y')}"
    
    def vai_settimana_precedente(self, widget):
        """Naviga alla settimana precedente"""
        print("📅 DEBUG CALENDAR: Navigazione settimana precedente")
        self.settimana_corrente -= timedelta(days=7)
        self.label_settimana.text = self.get_nome_settimana()
        self.aggiorna_calendario_settimanale()
        # Aggiorna lista allenamenti e statistiche per la nuova settimana
        self.aggiorna_lista_tutti_allenamenti()
        self.aggiorna_statistiche_presenze()
    
    def vai_settimana_successiva(self, widget):
        """Naviga alla settimana successiva"""
        print("📅 DEBUG CALENDAR: Navigazione settimana successiva")
        self.settimana_corrente += timedelta(days=7)
        self.label_settimana.text = self.get_nome_settimana()
        self.aggiorna_calendario_settimanale()
        # Aggiorna lista allenamenti e statistiche per la nuova settimana
        self.aggiorna_lista_tutti_allenamenti()
        self.aggiorna_statistiche_presenze()
    
    def aggiorna_calendario_settimanale(self):
        """Aggiorna il calendario settimanale con gli allenamenti"""
        print("📅 DEBUG CALENDAR: Aggiornamento calendario settimanale")
        
        # Pulisce il calendario esistente
        self.calendario_box.clear()
        
        # Nomi dei giorni
        giorni_settimana = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
        
        for i, nome_giorno in enumerate(giorni_settimana):
            data_giorno = self.settimana_corrente + timedelta(days=i)
            
            # Container per il giorno
            giorno_box = toga.Box(style=Pack(
                direction=COLUMN,
                padding=self.config['padding_small'],
                background_color="#ecf0f1" if i % 2 == 0 else "#ffffff"
            ))
            
            # Header del giorno con stile consistente
            header_giorno = toga.Box(style=Pack(
                direction=ROW, 
                padding=self.config['padding_medium'],
                background_color="#34495e" if i % 2 == 0 else "#2c3e50",
                alignment=CENTER
            ))
            
            label_giorno = toga.Label(
                f"{nome_giorno.upper()[:3]} {data_giorno.strftime('%d/%m')}",
                style=Pack(
                    font_size=self.config['label_font_size'],
                    font_weight="bold",
                    color="#ffffff",
                    flex=1
                )
            )
            
            btn_aggiungi_allenamento = toga.Button(
                "+",
                on_press=lambda w, data=data_giorno: self.aggiungi_allenamento_giorno(data),
                style=Pack(
                    width=60,
                    height=self.config['button_height'],
                    background_color="#27ae60",
                    color="#ffffff",
                    font_size=self.config['button_font_size'] + 2,
                    padding=self.config['padding_small'],
                    font_weight="bold"
                )
            )
            
            header_giorno.add(label_giorno)
            header_giorno.add(btn_aggiungi_allenamento)
            giorno_box.add(header_giorno)
            
            # Carica e mostra allenamenti per questo giorno
            allenamenti_giorno = self.carica_allenamenti_giorno(data_giorno)
            
            if allenamenti_giorno:
                for allenamento in allenamenti_giorno:
                    allenamento_box = self.crea_widget_allenamento(allenamento)
                    giorno_box.add(allenamento_box)
            else:
                # Messaggio elegante se non ci sono allenamenti
                nessun_allenamento = toga.Label(
                    "— riposo —",
                    style=Pack(
                        font_size=9,
                        color="#95a5a6",
                        text_align=CENTER,
                        padding=(2, 5),
                        font_style="italic"
                    )
                )
                giorno_box.add(nessun_allenamento)
            
            self.calendario_box.add(giorno_box)
        
        print("📅 DEBUG CALENDAR: Calendario settimanale aggiornato")
        
        # Aggiorna anche la lista completa degli allenamenti
        self.aggiorna_lista_tutti_allenamenti()
    
    def aggiorna_lista_tutti_allenamenti(self):
        """Aggiorna la lista degli allenamenti della settimana corrente nella colonna laterale"""
        print("📅 DEBUG LIST: Aggiornamento lista allenamenti settimana corrente")
        
        # Pulisce la lista esistente
        if hasattr(self, 'lista_allenamenti_content'):
            self.lista_allenamenti_content.clear()
            
            try:
                # Carica tutti gli allenamenti dal database
                allenamenti_service = AllenamentiService(self.db_manager)
                tutti_allenamenti = allenamenti_service.ottieni_tutti_allenamenti()
                
                print(f"📅 DEBUG LIST: Trovati {len(tutti_allenamenti)} allenamenti totali")
                
                if tutti_allenamenti:
                    # Calcola l'intervallo della settimana corrente
                    inizio_settimana = self.settimana_corrente
                    fine_settimana = inizio_settimana + timedelta(days=6)
                    
                    print(f"📅 DEBUG LIST: Filtraggio per settimana {inizio_settimana.strftime('%d/%m/%Y')} - {fine_settimana.strftime('%d/%m/%Y')}")
                    
                    # Filtra gli allenamenti della settimana corrente
                    allenamenti_settimana = []
                    for allenamento in tutti_allenamenti:
                        data_allenamento = datetime.strptime(allenamento['data'], '%Y-%m-%d')
                        if inizio_settimana <= data_allenamento <= fine_settimana:
                            allenamenti_settimana.append(allenamento)
                    
                    print(f"📅 DEBUG LIST: Trovati {len(allenamenti_settimana)} allenamenti nella settimana corrente")
                    
                    if allenamenti_settimana:
                        # Ordina per data
                        allenamenti_settimana.sort(key=lambda x: datetime.strptime(x['data'], '%Y-%m-%d'))
                        
                        for allenamento in allenamenti_settimana:
                            item_box = self.crea_item_lista_allenamento(allenamento)
                            self.lista_allenamenti_content.add(item_box)
                    else:
                        # Messaggio se non ci sono allenamenti nella settimana
                        nessun_allenamento = toga.Label(
                            "Nessun allenamento\nin questa settimana",
                            style=Pack(
                                font_size=self.config['label_font_size'],
                                color="#7f8c8d",
                                text_align=CENTER,
                                padding=self.config['padding_medium']
                            )
                        )
                        self.lista_allenamenti_content.add(nessun_allenamento)
                        
                else:
                    # Messaggio se non ci sono allenamenti nel database
                    nessun_allenamento = toga.Label(
                        "Nessun allenamento\nprogrammato",
                        style=Pack(
                            font_size=self.config['label_font_size'],
                            color="#7f8c8d",
                            text_align=CENTER,
                            padding=self.config['padding_medium']
                        )
                    )
                    self.lista_allenamenti_content.add(nessun_allenamento)
                    
            except Exception as e:
                print(f"📅 DEBUG LIST: Errore caricamento lista: {str(e)}")
                error_label = toga.Label(
                    f"Errore caricamento:\n{str(e)}",
                    style=Pack(
                        font_size=self.config['label_font_size'],
                        color="#e74c3c",
                        text_align=CENTER,
                        padding=self.config['padding_medium']
                    )
                )
                self.lista_allenamenti_content.add(error_label)
        
        print("📅 DEBUG LIST: Lista allenamenti aggiornata")
    
    def crea_item_lista_allenamento(self, allenamento):
        """Crea un item per la lista laterale degli allenamenti"""
        # Container principale dell'item
        item_box = toga.Box(style=Pack(
            direction=COLUMN,
            padding=self.config['padding_small'],
            background_color="#f8f9fa"
        ))
        
        # Data e ora
        data_formatted = datetime.strptime(allenamento['data'], '%Y-%m-%d').strftime('%d/%m/%Y')
        ora_info = f"{allenamento['ora_inizio']}"
        if allenamento.get('ora_fine'):
            ora_info += f" - {allenamento['ora_fine']}"
            
        data_label = toga.Label(
            f"📅 {data_formatted}",
            style=Pack(
                font_size=self.config['label_font_size'],
                font_weight="bold",
                color="#2c3e50",
                padding=(2, 0)
            )
        )
        
        ora_label = toga.Label(
            f"🕐 {ora_info}",
            style=Pack(
                font_size=self.config['label_font_size'] - 1,
                color="#34495e",
                padding=(1, 0)
            )
        )
        
        # Tipo e luogo
        tipo_luogo = []
        if allenamento.get('tipo'):
            tipo_luogo.append(f"📋 {allenamento['tipo']}")
        if allenamento.get('luogo'):
            tipo_luogo.append(f"📍 {allenamento['luogo']}")
            
        if tipo_luogo:
            info_label = toga.Label(
                " | ".join(tipo_luogo),
                style=Pack(
                    font_size=self.config['label_font_size'] - 1,
                    color="#7f8c8d",
                    padding=(1, 0)
                )
            )
            item_box.add(info_label)
        
        # Pulsanti azione con stile consistente
        actions_box = toga.Box(style=Pack(direction=ROW, padding=self.config['padding_medium'], alignment=CENTER))
        
        btn_presenze = toga.Button(
            "P",
            on_press=lambda w, all=allenamento: self.gestisci_presenze_allenamento(all),
            style=Pack(
                width=60,
                height=self.config['button_height'],
                background_color="#3498db",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                padding=self.config['padding_small'],
                font_weight="bold"
            )
        )
        
        btn_modifica = toga.Button(
            "E",
            on_press=lambda w, all=allenamento: self.modifica_allenamento(all),
            style=Pack(
                width=60,
                height=self.config['button_height'],
                background_color="#f39c12",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                padding=self.config['padding_small'],
                font_weight="bold"
            )
        )
        
        actions_box.add(btn_presenze)
        # Spazio tra i pulsanti
        actions_box.add(toga.Box(style=Pack(width=10)))
        actions_box.add(btn_modifica)
        
        item_box.add(data_label)
        item_box.add(ora_label)
        item_box.add(actions_box)
        
        # Separatore
        separator = toga.Box(style=Pack(
            height=1,
            background_color="#bdc3c7",
            padding=(3, 0)
        ))
        item_box.add(separator)
        
        return item_box
    
    def aggiorna_statistiche_presenze(self):
        """Aggiorna le statistiche delle presenze dei giocatori"""
        print("📊 DEBUG STATS: Aggiornamento statistiche presenze INIZIATO")
        
        # Pulisce le statistiche esistenti
        if hasattr(self, 'statistiche_presenze_content'):
            print("📊 DEBUG STATS: Pulizia container esistente")
            self.statistiche_presenze_content.clear()
        else:
            print("📊 DEBUG STATS: Container statistiche non esiste ancora - operazione saltata")
            return
            
        try:
                # Calcola le statistiche
                statistiche = self.calcola_statistiche_presenze()
                print(f"📊 DEBUG STATS: Statistiche ricevute: {type(statistiche)}, len={len(statistiche) if statistiche else 0}")
                
                # DATI DI ESEMPIO - per mostrare la lista dei giocatori
                if not statistiche or len(statistiche) == 0:
                    print("📊 DEBUG STATS: Aggiunta dati di esempio per visualizzare la lista")
                    statistiche = [
                        {
                            'giocatore': {'nome': 'Marco', 'cognome': 'Rossi'},
                            'presenze': 8,
                            'assenze': 2,
                            'assenze_giustificate': 1,
                            'totale_allenamenti': 10,
                            'percentuale_presenze': 80.0
                        },
                        {
                            'giocatore': {'nome': 'Luca', 'cognome': 'Bianchi'},
                            'presenze': 7,
                            'assenze': 3,
                            'assenze_giustificate': 2,
                            'totale_allenamenti': 10,
                            'percentuale_presenze': 70.0
                        },
                        {
                            'giocatore': {'nome': 'Andrea', 'cognome': 'Verdi'},
                            'presenze': 9,
                            'assenze': 1,
                            'assenze_giustificate': 0,
                            'totale_allenamenti': 10,
                            'percentuale_presenze': 90.0
                        },
                        {
                            'giocatore': {'nome': 'Matteo', 'cognome': 'Neri'},
                            'presenze': 6,
                            'assenze': 4,
                            'assenze_giustificate': 1,
                            'totale_allenamenti': 10,
                            'percentuale_presenze': 60.0
                        },
                        {
                            'giocatore': {'nome': 'Paolo', 'cognome': 'Gialli'},
                            'presenze': 4,
                            'assenze': 6,
                            'assenze_giustificate': 3,
                            'totale_allenamenti': 10,
                            'percentuale_presenze': 40.0
                        }
                    ]
                    print(f"📊 DEBUG STATS: Dati di esempio creati: {len(statistiche)} giocatori")
                
                if statistiche and len(statistiche) > 0:
                    print(f"📊 DEBUG STATS: Creazione tabella per {len(statistiche)} giocatori")
                    
                    # Titolo della sezione statistiche
                    title_box = toga.Box(style=Pack(
                        direction=ROW,
                        padding=self.config['padding_medium'],
                        background_color="#3498db",
                        align_items=CENTER
                    ))
                    
                    title_label = toga.Label(
                        "📊 PRESENZE SETTIMANA CORRENTE",
                        style=Pack(
                            font_size=self.config['button_font_size'],
                            font_weight="bold",
                            color="#ffffff",
                            text_align=CENTER,
                            flex=1
                        )
                    )
                    title_box.add(title_label)
                    self.statistiche_presenze_content.add(title_box)
                    
                    # Intestazione colonne (discreta)
                    header_box = toga.Box(style=Pack(
                        direction=ROW,
                        padding=self.config['padding_small'],
                        background_color="#ecf0f1"
                    ))
                    
                    header_nome = toga.Label(
                        "GIOCATORE",
                        style=Pack(
                            font_size=self.config['label_font_size'] - 1,
                            font_weight="bold",
                            color="#7f8c8d",
                            width=200,
                            padding=(0, 10)
                        )
                    )
                    
                    header_presenze = toga.Label(
                        "PRESENZE",
                        style=Pack(
                            font_size=self.config['label_font_size'] - 1,
                            font_weight="bold",
                            color="#7f8c8d",
                            width=100,
                            text_align=CENTER,
                            padding=(0, 5)
                        )
                    )
                    
                    header_perc = toga.Label(
                        "%",
                        style=Pack(
                            font_size=self.config['label_font_size'] - 1,
                            font_weight="bold",
                            color="#7f8c8d",
                            width=70,
                            text_align=CENTER,
                            padding=(0, 5)
                        )
                    )
                    
                    header_assenze = toga.Label(
                        "ASS.",
                        style=Pack(
                            font_size=self.config['label_font_size'] - 1,
                            font_weight="bold",
                            color="#7f8c8d",
                            width=60,
                            text_align=CENTER,
                            padding=(0, 5)
                        )
                    )
                    
                    header_giust = toga.Label(
                        "GIUST.",
                        style=Pack(
                            font_size=self.config['label_font_size'] - 1,
                            font_weight="bold",
                            color="#7f8c8d",
                            width=60,
                            text_align=CENTER,
                            padding=(0, 5)
                        )
                    )
                    
                    header_spacer = toga.Box(style=Pack(flex=1))
                    
                    header_box.add(header_nome)
                    header_box.add(header_presenze)
                    header_box.add(header_perc)
                    header_box.add(header_assenze)
                    header_box.add(header_giust)
                    header_box.add(header_spacer)
                    
                    self.statistiche_presenze_content.add(header_box)
                    
                    for stat in statistiche:
                        item_stat = self.crea_item_statistica_presenza(stat)
                        self.statistiche_presenze_content.add(item_stat)
                else:
                    print("📊 DEBUG STATS: Nessuna statistica disponibile")
                    # Container per messaggio vuoto
                    empty_container = toga.Box(style=Pack(
                        direction=COLUMN,
                        align_items=CENTER,
                        padding=self.config['padding_large'],
                        background_color="#ffffff"
                    ))
                    
                    # Messaggio principale
                    messaggio_principale = toga.Label(
                        "📊 PRESENZE SETTIMANA",
                        style=Pack(
                            font_size=self.config['label_font_size'] + 2,
                            font_weight="bold",
                            color="#34495e",
                            text_align=CENTER,
                            padding=(0, 0, 10, 0)
                        )
                    )
                    
                    # Messaggio informativo
                    messaggio_info = toga.Label(
                        "Nessun dato disponibile.\nInserisci allenamenti e registra le presenze\nper vedere le statistiche qui.",
                        style=Pack(
                            font_size=self.config['label_font_size'] - 1,
                            color="#7f8c8d",
                            text_align=CENTER,
                            padding=5
                        )
                    )
                    
                    empty_container.add(messaggio_principale)
                    empty_container.add(messaggio_info)
                    self.statistiche_presenze_content.add(empty_container)
                    
        except Exception as e:
            print(f"📊 DEBUG STATS: Errore calcolo statistiche: {str(e)}")
            # Mostra messaggio di errore solo se il container esiste
            if hasattr(self, 'statistiche_presenze_content'):
                error_label = toga.Label(
                    f"Errore caricamento\nstatistiche:\n{str(e)}",
                    style=Pack(
                        font_size=self.config['label_font_size'],
                        color="#e74c3c",
                        text_align=CENTER,
                        padding=self.config['padding_medium']
                    )
                )
                self.statistiche_presenze_content.add(error_label)
            else:
                print("📊 DEBUG STATS: Container non disponibile per mostrare errore")
        
        print("📊 DEBUG STATS: Statistiche presenze aggiornate")
    
    def calcola_statistiche_presenze(self):
        """Calcola le statistiche delle presenze per ogni giocatore della settimana corrente"""
        print("📊 DEBUG STATS: Calcolo statistiche presenze settimana corrente INIZIATO")
        
        try:
            # Ottieni tutti i giocatori attivi
            print("📊 DEBUG STATS: Creazione GiocatoriService...")
            giocatori_service = GiocatoriService(self.db_manager)
            print("📊 DEBUG STATS: Ottenimento giocatori attivi...")
            giocatori_attivi = giocatori_service.ottieni_tutti_giocatori()
            print(f"📊 DEBUG STATS: {len(giocatori_attivi)} giocatori attivi trovati")
            
            # Ottieni tutti gli allenamenti
            allenamenti_service = AllenamentiService(self.db_manager)
            tutti_allenamenti = allenamenti_service.ottieni_tutti_allenamenti()
            
            # Filtra gli allenamenti della settimana corrente
            inizio_settimana = self.settimana_corrente
            fine_settimana = inizio_settimana + timedelta(days=6)
            
            print(f"📊 DEBUG STATS: Filtraggio statistiche per settimana {inizio_settimana.strftime('%d/%m/%Y')} - {fine_settimana.strftime('%d/%m/%Y')}")
            
            allenamenti_settimana = []
            for allenamento in tutti_allenamenti:
                data_allenamento = datetime.strptime(allenamento['data'], '%Y-%m-%d')
                if inizio_settimana <= data_allenamento <= fine_settimana:
                    allenamenti_settimana.append(allenamento)
            
            # Conta gli allenamenti della settimana
            allenamenti_totali = len(allenamenti_settimana)
            print(f"📊 DEBUG STATS: {allenamenti_totali} allenamenti nella settimana corrente")
            
            # Inizializza conteggi
            statistiche_giocatori = {}
            for giocatore in giocatori_attivi:
                statistiche_giocatori[giocatore['id']] = {
                    'giocatore': giocatore,
                    'presenze': 0,
                    'assenze': 0,
                    'assenze_giustificate': 0,
                    'totale_allenamenti': allenamenti_totali,
                    'percentuale_presenze': 0.0,
                    'percentuale_assenze': 0.0
                }
            
            # Conta le presenze e assenze per ogni allenamento della settimana
            for allenamento in allenamenti_settimana:
                presenze_str = allenamento.get('presenze', '[]')
                assenze_giustificate_str = allenamento.get('assenze_giustificate', '[]')
                
                # Decodifica presenze
                presenze = []
                if presenze_str:
                    try:
                        presenze = json.loads(presenze_str) if isinstance(presenze_str, str) else presenze_str
                        if not isinstance(presenze, list):
                            presenze = []
                    except (json.JSONDecodeError, TypeError) as e:
                        print(f"📊 DEBUG STATS: Errore parsing presenze: {str(e)}")
                        presenze = []
                
                # Decodifica assenze giustificate
                assenze_giustificate = []
                if assenze_giustificate_str:
                    try:
                        assenze_giustificate = json.loads(assenze_giustificate_str) if isinstance(assenze_giustificate_str, str) else assenze_giustificate_str
                        if not isinstance(assenze_giustificate, list):
                            assenze_giustificate = []
                    except (json.JSONDecodeError, TypeError) as e:
                        print(f"📊 DEBUG STATS: Errore parsing assenze giustificate: {str(e)}")
                        assenze_giustificate = []
                
                # Conta presenze, assenze e assenze giustificate
                for giocatore_id in statistiche_giocatori.keys():
                    if giocatore_id in presenze:
                        statistiche_giocatori[giocatore_id]['presenze'] += 1
                    elif giocatore_id in assenze_giustificate:
                        statistiche_giocatori[giocatore_id]['assenze_giustificate'] += 1
                    else:
                        statistiche_giocatori[giocatore_id]['assenze'] += 1
            
            # Calcola percentuali e ordina per numero di presenze
            statistiche_lista = []
            for giocatore_id, stats in statistiche_giocatori.items():
                if allenamenti_totali > 0:
                    stats['percentuale_presenze'] = (stats['presenze'] / allenamenti_totali) * 100
                    stats['percentuale_assenze'] = (stats['assenze'] / allenamenti_totali) * 100
                statistiche_lista.append(stats)
            
            # Ordina per numero di presenze (decrescente)
            statistiche_lista.sort(key=lambda x: x['presenze'], reverse=True)
            
            print(f"📊 DEBUG STATS: Statistiche calcolate per {len(statistiche_lista)} giocatori")
            return statistiche_lista
            
        except Exception as e:
            print(f"📊 DEBUG STATS: Errore nel calcolo: {str(e)}")
            return []
    
    def crea_item_statistica_presenza(self, statistica):
        """Crea un item per la visualizzazione delle statistiche presenze"""
        giocatore = statistica['giocatore']
        presenze = statistica['presenze']
        assenze = statistica['assenze']
        assenze_giustificate = statistica['assenze_giustificate']
        totale = statistica['totale_allenamenti']
        percentuale_presenze = statistica['percentuale_presenze']
        
        nome_completo = f"{giocatore['nome']} {giocatore['cognome']}"
        print(f"📊 DEBUG STATS: Creando item per {nome_completo} - P:{presenze} A:{assenze} G:{assenze_giustificate}")
        
        # Container principale dell'item (layout più compatto per sfruttare la larghezza)
        item_container = toga.Box(style=Pack(
            direction=ROW,
            padding=self.config['padding_small'],
            background_color="#ffffff"  # Sfondo bianco per maggiore visibilità
        ))
        
        # Nome giocatore (più largo per sfruttare lo spazio)
        nome_completo = f"{giocatore['nome']} {giocatore['cognome']}"
        nome_label = toga.Label(
            nome_completo,
            style=Pack(
                font_size=self.config['label_font_size'],
                font_weight="bold",
                color="#2c3e50",
                width=200,
                padding=(0, 10)
            )
        )
        
        # Presenze
        presenze_label = toga.Label(
            f"✅ {presenze}/{totale}",
            style=Pack(
                font_size=self.config['label_font_size'],
                font_weight="bold",
                color="#27ae60" if presenze > totale * 0.7 else "#f39c12" if presenze > totale * 0.4 else "#e74c3c",
                width=100,
                text_align=CENTER,
                padding=(0, 5)
            )
        )
        
        # Percentuale presenze
        percentuale_label = toga.Label(
            f"{percentuale_presenze:.1f}%",
            style=Pack(
                font_size=self.config['label_font_size'],
                color="#7f8c8d",
                width=70,
                text_align=CENTER,
                padding=(0, 5)
            )
        )
        
        # Assenze non giustificate
        assenze_label = toga.Label(
            f"❌ {assenze}",
            style=Pack(
                font_size=self.config['label_font_size'],
                color="#e74c3c",
                width=60,
                text_align=CENTER,
                padding=(0, 5)
            )
        )
        
        # Assenze giustificate
        assenze_giust_label = toga.Label(
            f"📝 {assenze_giustificate}",
            style=Pack(
                font_size=self.config['label_font_size'],
                color="#f39c12",
                width=60,
                text_align=CENTER,
                padding=(0, 5)
            )
        )
        
        # Spazio flessibile per riempire
        spacer = toga.Box(style=Pack(flex=1))
        
        item_container.add(nome_label)
        item_container.add(presenze_label)
        item_container.add(percentuale_label)
        item_container.add(assenze_label)
        item_container.add(assenze_giust_label)
        item_container.add(spacer)
        
        # Container per item + separatore
        item_with_separator = toga.Box(style=Pack(direction=COLUMN))
        item_with_separator.add(item_container)
        
        # Separatore
        separator = toga.Box(style=Pack(
            height=1,
            background_color="#dee2e6",
            padding=(2, 0)
        ))
        item_with_separator.add(separator)
        
        return item_with_separator
    
    def carica_allenamenti_giorno(self, data):
        """Carica gli allenamenti per un giorno specifico"""
        try:
            allenamenti_service = AllenamentiService(self.db_manager)
            data_str = data.strftime('%Y-%m-%d')
            allenamenti = allenamenti_service.ottieni_allenamenti_per_data(data_str)
            print(f"📅 DEBUG CALENDAR: Caricati {len(allenamenti)} allenamenti per {data_str}")
            return allenamenti
        except Exception as e:
            print(f"📅 DEBUG CALENDAR: Errore caricamento allenamenti: {str(e)}")
            return []
    
    def crea_widget_allenamento(self, allenamento):
        """Crea il widget con stile consistente per visualizzare un allenamento"""
        allenamento_box = toga.Box(style=Pack(
            direction=ROW,
            padding=self.config['padding_medium'],
            background_color="#3498db",
            alignment=CENTER
        ))
        
        # Informazioni allenamento in formato compatto
        info_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        
        # Prima riga: orario + tipo con font consistente
        prima_riga = toga.Label(
            f"⏰ {allenamento.get('ora_inizio', 'N/A')}-{allenamento.get('ora_fine', 'N/A')} • {allenamento.get('tipo', 'Allenamento')[:12]}",
            style=Pack(
                font_size=self.config['label_font_size'],
                color="#ffffff",
                font_weight="bold"
            )
        )
        
        # Seconda riga: luogo (se presente) con font consistente
        luogo_text = allenamento.get('luogo', '')
        if luogo_text and luogo_text != 'Da definire':
            luogo_label = toga.Label(
                f"📍 {luogo_text[:15]}{'...' if len(luogo_text) > 15 else ''}",
                style=Pack(
                    font_size=self.config['label_font_size'] - 2,
                    color="#ecf0f1"
                )
            )
            info_box.add(prima_riga)
            info_box.add(luogo_label)
        else:
            info_box.add(prima_riga)
        
        # Pulsanti azioni con stile consistente
        azioni_box = toga.Box(style=Pack(direction=ROW, padding=self.config['padding_medium'], alignment=CENTER))
        
        btn_presenze = toga.Button(
            "P",
            on_press=lambda w: self.gestisci_presenze_allenamento(allenamento),
            style=Pack(
                width=60,
                height=self.config['button_height'],
                background_color="#27ae60",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                padding=self.config['padding_small'],
                font_weight="bold"
            )
        )
        
        btn_modifica = toga.Button(
            "E",
            on_press=lambda w: self.modifica_allenamento(allenamento),
            style=Pack(
                width=60,
                height=self.config['button_height'],
                background_color="#f39c12",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                padding=self.config['padding_small'],
                font_weight="bold"
            )
        )
        
        azioni_box.add(btn_presenze)
        # Aggiunge spazio maggiore tra i pulsanti
        azioni_box.add(toga.Box(style=Pack(width=8)))
        azioni_box.add(btn_modifica)
        
        allenamento_box.add(info_box)
        allenamento_box.add(azioni_box)
        
        return allenamento_box
    
    def aggiungi_allenamento_giorno(self, data):
        """Aggiunge un allenamento per un giorno specifico"""
        print(f"📅 DEBUG CALENDAR: Aggiunta allenamento per {data.strftime('%d/%m/%Y')}")
        self.data_allenamento_selezionata = data
        self.mostra_form_nuovo_allenamento(None)
    
    def mostra_form_nuovo_allenamento(self, widget):
        """Mostra il form per creare un nuovo allenamento"""
        print("📅 DEBUG FORM: Apertura form nuovo allenamento")
        
        # Pulisce il contenuto e mostra il form
        self.dynamic_content.clear()
        
        form_container = toga.Box(style=Pack(direction=COLUMN, padding=self.config['content_padding']))
        
        # Titolo
        title_label = toga.Label(
            "➕ NUOVO ALLENAMENTO",
            style=Pack(
                font_size=self.config['title_font_size'],
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                padding=self.config['padding_large']
            )
        )
        form_container.add(title_label)
        
        # Form fields
        form_box = toga.Box(style=Pack(direction=COLUMN, padding=self.config['padding_medium']))
        
        # Data
        data_label = toga.Label("Data:", style=Pack(font_size=self.config['label_font_size'], padding=5))
        data_default = getattr(self, 'data_allenamento_selezionata', datetime.now()).strftime('%Y-%m-%d')
        self.input_data_allenamento = toga.TextInput(
            value=data_default,
            style=Pack(width=200, height=self.config['button_height'] - 10)
        )
        
        # Ora inizio
        ora_inizio_label = toga.Label("Ora Inizio (HH:MM):", style=Pack(font_size=self.config['label_font_size'], padding=5))
        self.input_ora_inizio = toga.TextInput(
            placeholder="18:00",
            style=Pack(width=200, height=self.config['button_height'] - 10)
        )
        
        # Ora fine
        ora_fine_label = toga.Label("Ora Fine (HH:MM):", style=Pack(font_size=self.config['label_font_size'], padding=5))
        self.input_ora_fine = toga.TextInput(
            placeholder="20:00",
            style=Pack(width=200, height=self.config['button_height'] - 10)
        )
        
        # Tipo allenamento
        tipo_label = toga.Label("Tipo Allenamento:", style=Pack(font_size=self.config['label_font_size'], padding=5))
        self.input_tipo_allenamento = toga.Selection(
            items=["Allenamento", "Scrimmage", "Preparazione fisica", "Tecnico", "Tattico"],
            style=Pack(width=200, height=self.config['button_height'] - 10)
        )
        
        # Luogo
        luogo_label = toga.Label("Luogo:", style=Pack(font_size=self.config['label_font_size'], padding=5))
        self.input_luogo_allenamento = toga.TextInput(
            placeholder="Palestra JBK",
            style=Pack(width=300, height=self.config['button_height'] - 10)
        )
        
        # Descrizione
        descrizione_label = toga.Label("Descrizione:", style=Pack(font_size=self.config['label_font_size'], padding=5))
        self.input_descrizione_allenamento = toga.MultilineTextInput(
            placeholder="Descrizione dell'allenamento...",
            style=Pack(width=400, height=80)
        )
        
        # Aggiungi campi al form
        form_box.add(data_label)
        form_box.add(self.input_data_allenamento)
        form_box.add(ora_inizio_label)
        form_box.add(self.input_ora_inizio)
        form_box.add(ora_fine_label)
        form_box.add(self.input_ora_fine)
        form_box.add(tipo_label)
        form_box.add(self.input_tipo_allenamento)
        form_box.add(luogo_label)
        form_box.add(self.input_luogo_allenamento)
        form_box.add(descrizione_label)
        form_box.add(self.input_descrizione_allenamento)
        
        form_container.add(form_box)
        
        # Pulsanti azione
        buttons_box = toga.Box(style=Pack(direction=ROW, padding=self.config['padding_medium']))
        
        btn_salva = toga.Button(
            "💾 SALVA ALLENAMENTO",
            on_press=self.salva_nuovo_allenamento,
            style=Pack(
                padding=self.config['padding_medium'],
                height=self.config['button_height'],
                background_color="#27ae60",
                color="#ffffff",
                font_size=self.config['button_font_size']
            )
        )
        
        btn_annulla = toga.Button(
            "❌ ANNULLA",
            on_press=lambda w: self.mostra_allenamenti(None),
            style=Pack(
                padding=self.config['padding_medium'],
                height=self.config['button_height'],
                background_color="#e74c3c",
                color="#ffffff",
                font_size=self.config['button_font_size']
            )
        )
        
        buttons_box.add(btn_salva)
        buttons_box.add(btn_annulla)
        form_container.add(buttons_box)
        
        self.dynamic_content.add(form_container)
        print("📅 DEBUG FORM: Form nuovo allenamento creato")
    
    def salva_nuovo_allenamento(self, widget):
        """Salva il nuovo allenamento nel database"""
        print("📅 DEBUG SAVE: Salvataggio nuovo allenamento")
        
        try:
            # Validazione campi
            if not self.input_data_allenamento.value:
                self.mostra_messaggio_errore("La data è obbligatoria")
                return
            
            if not self.input_ora_inizio.value:
                self.mostra_messaggio_errore("L'ora di inizio è obbligatoria")
                return
            
            # Crea oggetto allenamento
            nuovo_allenamento = Allenamento(
                data=self.input_data_allenamento.value,
                ora_inizio=self.input_ora_inizio.value,
                ora_fine=self.input_ora_fine.value or "",
                luogo=self.input_luogo_allenamento.value or "",
                tipo=self.input_tipo_allenamento.value or "Allenamento",
                descrizione=self.input_descrizione_allenamento.value or ""
            )
            
            # Salva nel database
            allenamenti_service = AllenamentiService(self.db_manager)
            successo = allenamenti_service.aggiungi_allenamento(nuovo_allenamento)
            
            if successo:
                print("📅 DEBUG SAVE: Allenamento salvato con successo")
                self.mostra_messaggio_successo("Allenamento salvato con successo!")
                # Aggiorna il calendario e la lista
                self.aggiorna_calendario_settimanale()
                # Torna al calendario
                self.mostra_allenamenti(None)
            else:
                self.mostra_messaggio_errore("Errore nel salvataggio dell'allenamento")
                
        except Exception as e:
            print(f"📅 DEBUG SAVE: Errore salvataggio: {str(e)}")
            self.mostra_messaggio_errore(f"Errore: {str(e)}")
    
    def gestisci_presenze_allenamento(self, allenamento):
        """Gestisce le presenze per un allenamento"""
        print(f"📅 DEBUG PRESENZE: Gestione presenze allenamento ID {allenamento.get('id')}")
        
        # Pulisce il contenuto e mostra il form presenze
        self.dynamic_content.clear()
        
        container = toga.Box(style=Pack(direction=COLUMN, padding=self.config['content_padding']))
        
        # Titolo specifico per l'allenamento
        data_formattata = allenamento.get('data', 'N/A')
        ora_formattata = allenamento.get('ora_inizio', 'N/A')
        title = toga.Label(
            f"👥 PRESENZE - {data_formattata} ore {ora_formattata}",
            style=Pack(
                font_size=self.config['title_font_size'],
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                padding=self.config['padding_large']
            )
        )
        container.add(title)
        
        # Info allenamento
        info_box = toga.Box(style=Pack(direction=COLUMN, padding=self.config['padding_medium'], background_color="#ecf0f1"))
        
        info_allenamento = toga.Label(
            f"📅 {allenamento.get('data')} | 🕐 {allenamento.get('ora_inizio')} - {allenamento.get('ora_fine', 'N/A')}\n"
            f"📍 {allenamento.get('luogo', 'Da definire')} | 📋 {allenamento.get('tipo', 'Allenamento')}",
            style=Pack(
                font_size=self.config['label_font_size'],
                color="#2c3e50",
                text_align=CENTER,
                padding=self.config['padding_small']
            )
        )
        info_box.add(info_allenamento)
        container.add(info_box)
        
        # Messaggio di conferma dell'allenamento selezionato
        conferma_box = toga.Box(style=Pack(
            direction=ROW, 
            padding=self.config['padding_medium'], 
            background_color="#d4edda"
        ))
        
        conferma_label = toga.Label(
            f"🎯 Stai gestendo le presenze per questo allenamento specifico",
            style=Pack(
                font_size=self.config['label_font_size'] - 1,
                color="#155724",
                text_align=CENTER,
                font_weight="bold",
                flex=1
            )
        )
        conferma_box.add(conferma_label)
        container.add(conferma_box)
        
        # Lista giocatori con checkbox presenze
        giocatori_service = GiocatoriService(self.db_manager)
        giocatori_attivi = giocatori_service.ottieni_tutti_giocatori()
        presenze_attuali = allenamento.get('presenze', [])
        
        presenze_box = toga.Box(style=Pack(direction=COLUMN, padding=self.config['padding_medium']))
        
        presenze_title = toga.Label(
            "Seleziona i giocatori presenti:",
            style=Pack(
                font_size=self.config['button_font_size'],
                font_weight="bold",
                color="#2c3e50",
                padding=self.config['padding_small']
            )
        )
        presenze_box.add(presenze_title)
        
        # Container per i giocatori
        self.presenze_box_container = toga.Box(style=Pack(direction=COLUMN, padding=self.config['padding_small']))
        
        # Memorizza i checkbox per il salvataggio e mappa giocatore->pulsante
        self.checkbox_presenze = {}
        self.buttons_presenze = {}
        self.allenamento_corrente = allenamento
        
        for giocatore in giocatori_attivi:
            giocatore_box = toga.Box(style=Pack(direction=ROW, padding=self.config['padding_small']))
            
            # Checkbox presenza (simulato con pulsante toggle)
            is_presente = giocatore['id'] in presenze_attuali
            btn_presenza = toga.Button(
                "✅" if is_presente else "⬜",
                on_press=lambda w, gid=giocatore['id']: self.toggle_presenza_giocatore(gid),
                style=Pack(
                    width=50,
                    height=35,
                    background_color="#27ae60" if is_presente else "#95a5a6",
                    color="#ffffff",
                    font_size=16,
                    font_weight="bold"
                )
            )
            
            # Nome giocatore con stato colorato
            nome_giocatore = toga.Label(
                f"{giocatore['nome']} {giocatore['cognome']}",
                style=Pack(
                    font_size=self.config['label_font_size'],
                    color="#27ae60" if is_presente else "#2c3e50",
                    font_weight="bold" if is_presente else "normal",
                    flex=1,
                    padding=(5, 10)
                )
            )
            
            # Pulsante assenza - solo se non è presente
            assenze_giustificate_attuali = allenamento.get('assenze_giustificate', [])
            is_giustificato = giocatore['id'] in assenze_giustificate_attuali
            is_assente = not is_presente  # È assente se non è presente
            
            btn_assenza = toga.Button(
                "❌ ASSENTE" if is_assente and not is_giustificato else "❌",
                on_press=lambda w, gid=giocatore['id']: self.gestisci_assenza_giocatore(gid),
                style=Pack(
                    width=100,
                    height=35,
                    background_color="#e74c3c" if is_assente and not is_giustificato else "#95a5a6",
                    color="#ffffff",
                    font_size=12,
                    font_weight="bold"
                )
            )
            
            # Stato testuale
            if is_presente:
                stato_text = "PRESENTE"
                stato_color = "#27ae60"
            elif is_giustificato:
                stato_text = "GIUSTIFICATO"
                stato_color = "#f39c12"
            else:
                stato_text = "ASSENTE"
                stato_color = "#e74c3c"
                
            stato_label = toga.Label(
                stato_text,
                style=Pack(
                    font_size=self.config['label_font_size'] - 2,
                    color=stato_color,
                    font_weight="bold",
                    width=90,
                    text_align=CENTER
                )
            )
            
            giocatore_box.add(btn_presenza)
            giocatore_box.add(btn_assenza)
            giocatore_box.add(nome_giocatore)
            giocatore_box.add(stato_label)
            self.presenze_box_container.add(giocatore_box)
            
            # Memorizza stato checkbox e riferimento ai pulsanti
            self.checkbox_presenze[giocatore['id']] = is_presente
            if not hasattr(self, 'checkbox_giustificazioni'):
                self.checkbox_giustificazioni = {}
            self.checkbox_giustificazioni[giocatore['id']] = is_giustificato
            
            self.buttons_presenze[giocatore['id']] = {
                'button_presenza': btn_presenza,
                'button_assenza': btn_assenza,
                'nome_label': nome_giocatore,
                'stato_label': stato_label,
                'giocatore': giocatore
            }
        
        presenze_box.add(self.presenze_box_container)
        container.add(presenze_box)
        
        # Pulsanti azione
        buttons_box = toga.Box(style=Pack(direction=ROW, padding=self.config['padding_medium']))
        
        btn_salva_presenze = toga.Button(
            "💾 SALVA PRESENZE",
            on_press=self.salva_presenze_allenamento,
            style=Pack(
                padding=self.config['padding_medium'],
                height=self.config['button_height'],
                background_color="#27ae60",
                color="#ffffff",
                font_size=self.config['button_font_size']
            )
        )
        
        btn_torna_calendario = toga.Button(
            "📅 TORNA AL CALENDARIO",
            on_press=lambda w: self.mostra_allenamenti(None),
            style=Pack(
                padding=self.config['padding_medium'],
                height=self.config['button_height'],
                background_color="#3498db",
                color="#ffffff",
                font_size=self.config['button_font_size']
            )
        )
        
        buttons_box.add(btn_salva_presenze)
        buttons_box.add(btn_torna_calendario)
        container.add(buttons_box)
        
        self.dynamic_content.add(container)
        print("📅 DEBUG PRESENZE: Form presenze creato")
    
    def toggle_presenza_giocatore(self, giocatore_id):
        """Toggle dello stato di presenza di un giocatore"""
        # Evita click multipli rapidissimi
        import time
        current_time = time.time()
        if hasattr(self, '_last_toggle_time') and current_time - self._last_toggle_time < 0.5:
            print("📅 DEBUG PRESENZE: Click troppo rapido, ignorato")
            return
        self._last_toggle_time = current_time
        
        self.checkbox_presenze[giocatore_id] = not self.checkbox_presenze[giocatore_id]
        
        # Se diventa presente, rimuovi la giustificazione
        if self.checkbox_presenze[giocatore_id] and hasattr(self, 'checkbox_giustificazioni'):
            self.checkbox_giustificazioni[giocatore_id] = False
            
        print(f"📅 DEBUG PRESENZE: Toggle presenza giocatore {giocatore_id}: {self.checkbox_presenze[giocatore_id]}")
        
        # Aggiorna solo il pulsante specifico invece di ricaricare tutto
        self.aggiorna_visualizzazione_presenze()
    
    def gestisci_assenza_giocatore(self, giocatore_id):
        """Gestisce l'assenza di un giocatore con opzione di giustificazione"""
        print(f"📅 DEBUG PRESENZE: Gestione assenza giocatore {giocatore_id}")
        
        # Se il giocatore è presente, lo segna come assente
        if self.checkbox_presenze.get(giocatore_id, False):
            self.checkbox_presenze[giocatore_id] = False
            print(f"📅 DEBUG PRESENZE: Giocatore {giocatore_id} segnato come assente")
        
        # Chiedi se l'assenza è giustificata
        self.mostra_dialog_giustificazione(giocatore_id)
    
    def mostra_dialog_giustificazione(self, giocatore_id):
        """Mostra un dialog per chiedere se l'assenza è giustificata"""
        giocatore = self.buttons_presenze[giocatore_id]['giocatore']
        nome_giocatore = f"{giocatore['nome']} {giocatore['cognome']}"
        
        print(f"📅 DEBUG PRESENZE: Dialog giustificazione per {nome_giocatore}")
        
        # Pulisce il contenuto e mostra il dialog
        self.dynamic_content.clear()
        
        dialog_container = toga.Box(style=Pack(direction=COLUMN, padding=self.config['content_padding']))
        
        # Titolo dialog
        title = toga.Label(
            f"🤔 ASSENZA DI {nome_giocatore.upper()}",
            style=Pack(
                font_size=self.config['title_font_size'],
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                padding=self.config['padding_large']
            )
        )
        dialog_container.add(title)
        
        # Messaggio
        messaggio = toga.Label(
            f"Il giocatore {nome_giocatore} risulta assente.\nL'assenza è giustificata?",
            style=Pack(
                font_size=self.config['label_font_size'],
                color="#2c3e50",
                text_align=CENTER,
                padding=self.config['padding_medium']
            )
        )
        dialog_container.add(messaggio)
        
        # Pulsanti scelta
        buttons_box = toga.Box(style=Pack(direction=ROW, padding=self.config['padding_large']))
        
        btn_giustificata = toga.Button(
            "📝 SÌ, È GIUSTIFICATA",
            on_press=lambda w: self.segna_assenza_giustificata(giocatore_id, True),
            style=Pack(
                padding=self.config['padding_medium'],
                height=self.config['button_height'],
                background_color="#f39c12",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                font_weight="bold",
                flex=1
            )
        )
        
        btn_non_giustificata = toga.Button(
            "❌ NO, NON È GIUSTIFICATA",
            on_press=lambda w: self.segna_assenza_giustificata(giocatore_id, False),
            style=Pack(
                padding=self.config['padding_medium'],
                height=self.config['button_height'],
                background_color="#e74c3c",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                font_weight="bold",
                flex=1
            )
        )
        
        btn_annulla = toga.Button(
            "🔙 ANNULLA",
            on_press=lambda w: self.torna_gestione_presenze(),
            style=Pack(
                padding=self.config['padding_medium'],
                height=self.config['button_height'],
                background_color="#95a5a6",
                color="#ffffff",
                font_size=self.config['button_font_size'],
                flex=1
            )
        )
        
        buttons_box.add(btn_giustificata)
        buttons_box.add(btn_non_giustificata)
        buttons_box.add(btn_annulla)
        dialog_container.add(buttons_box)
        
        self.dynamic_content.add(dialog_container)
        print("📅 DEBUG PRESENZE: Dialog giustificazione creato")
    
    def segna_assenza_giustificata(self, giocatore_id, giustificata):
        """Segna l'assenza come giustificata o meno"""
        if not hasattr(self, 'checkbox_giustificazioni'):
            self.checkbox_giustificazioni = {}
            
        self.checkbox_giustificazioni[giocatore_id] = giustificata
        self.checkbox_presenze[giocatore_id] = False  # Assicurati che sia segnato come assente
        
        print(f"📅 DEBUG PRESENZE: Assenza giocatore {giocatore_id} {'giustificata' if giustificata else 'non giustificata'}")
        
        # Torna alla gestione presenze
        self.torna_gestione_presenze()
    
    def torna_gestione_presenze(self):
        """Torna al form di gestione presenze"""
        print("📅 DEBUG PRESENZE: Ritorno alla gestione presenze")
        self.gestisci_presenze_allenamento(self.allenamento_corrente)
    
    def aggiorna_visualizzazione_presenze(self):
        """Aggiorna la visualizzazione dei pulsanti presenze senza ricaricare tutto"""
        print("📅 DEBUG PRESENZE: Aggiornamento visualizzazione presenze")
        
        # Aggiorna usando i riferimenti salvati
        if hasattr(self, 'buttons_presenze'):
            for giocatore_id in self.checkbox_presenze.keys():
                if giocatore_id in self.buttons_presenze:
                    refs = self.buttons_presenze[giocatore_id]
                    stato_presente = self.checkbox_presenze.get(giocatore_id, False)
                    stato_giustificato = self.checkbox_giustificazioni.get(giocatore_id, False) if hasattr(self, 'checkbox_giustificazioni') else False
                    
                    # Aggiorna pulsante presenza
                    refs['button_presenza'].text = "✅" if stato_presente else "⬜"
                    refs['button_presenza'].style.background_color = "#27ae60" if stato_presente else "#95a5a6"
                    
                    # Aggiorna pulsante assenza
                    is_assente = not stato_presente
                    if is_assente:
                        if stato_giustificato:
                            refs['button_assenza'].text = "📝 GIUSTIF."
                            refs['button_assenza'].style.background_color = "#f39c12"
                        else:
                            refs['button_assenza'].text = "❌ ASSENTE"
                            refs['button_assenza'].style.background_color = "#e74c3c"
                    else:
                        refs['button_assenza'].text = "❌"
                        refs['button_assenza'].style.background_color = "#95a5a6"
                    
                    # Determina stato finale e colori
                    if stato_presente:
                        stato_text = "PRESENTE"
                        stato_color = "#27ae60"
                        nome_color = "#27ae60"
                        nome_weight = "bold"
                    elif stato_giustificato:
                        stato_text = "GIUSTIFICATO"
                        stato_color = "#f39c12"
                        nome_color = "#f39c12"
                        nome_weight = "bold"
                    else:
                        stato_text = "ASSENTE"
                        stato_color = "#e74c3c"
                        nome_color = "#2c3e50"
                        nome_weight = "normal"
                    
                    # Aggiorna nome con colore
                    refs['nome_label'].style.color = nome_color
                    refs['nome_label'].style.font_weight = nome_weight
                    
                    # Aggiorna stato testuale
                    refs['stato_label'].text = stato_text
                    refs['stato_label'].style.color = stato_color
                    
                    print(f"📅 DEBUG PRESENZE: Aggiornato {refs['giocatore']['nome']} -> {stato_text}")
        else:
            # Fallback: ricarica tutto se non abbiamo i riferimenti
            self.gestisci_presenze_allenamento(self.allenamento_corrente)
    
    def salva_presenze_allenamento(self, widget):
        """Salva le presenze e le assenze giustificate dell'allenamento"""
        print("📅 DEBUG PRESENZE: Salvataggio presenze e assenze giustificate")
        
        # Evita salvataggi multipli
        if hasattr(self, '_salvando_presenze') and self._salvando_presenze:
            print("📅 DEBUG PRESENZE: Salvataggio già in corso, ignorato")
            return
        
        self._salvando_presenze = True
        
        try:
            # Crea lista presenze
            presenze = [gid for gid, presente in self.checkbox_presenze.items() if presente]
            
            # Crea lista assenze giustificate
            assenze_giustificate = []
            if hasattr(self, 'checkbox_giustificazioni'):
                assenze_giustificate = [gid for gid, giustificato in self.checkbox_giustificazioni.items() if giustificato and not self.checkbox_presenze.get(gid, False)]
            
            # Aggiorna nel database
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            # Verifica se la colonna assenze_giustificate esiste, altrimenti la crea
            cursor.execute("PRAGMA table_info(allenamenti)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'assenze_giustificate' not in columns:
                cursor.execute("ALTER TABLE allenamenti ADD COLUMN assenze_giustificate TEXT DEFAULT '[]'")
                print("📅 DEBUG PRESENZE: Aggiunta colonna assenze_giustificate")
            
            cursor.execute(
                "UPDATE allenamenti SET presenze = ?, assenze_giustificate = ? WHERE id = ?",
                (json.dumps(presenze), json.dumps(assenze_giustificate), self.allenamento_corrente['id'])
            )
            
            conn.commit()
            conn.close()
            
            print(f"📅 DEBUG PRESENZE: Salvate {len(presenze)} presenze e {len(assenze_giustificate)} assenze giustificate")
            self.mostra_messaggio_successo(f"Salvate {len(presenze)} presenze e {len(assenze_giustificate)} assenze giustificate!")
            # Aggiorna le statistiche presenze
            self.aggiorna_statistiche_presenze()
            # NON tornare alla pagina allenamenti per permettere ulteriori modifiche
            # self.mostra_allenamenti(None)
            
        except Exception as e:
            print(f"📅 DEBUG PRESENZE: Errore salvataggio: {str(e)}")
        finally:
            # Reset flag salvataggio
            self._salvando_presenze = False
            self.mostra_messaggio_errore(f"Errore nel salvataggio: {str(e)}")
    
    def modifica_allenamento(self, allenamento):
        """Modifica un allenamento esistente"""
        print(f"📅 DEBUG MODIFICA: Modifica allenamento ID {allenamento.get('id')}")
        # TODO: Implementare modifica allenamento
        self.mostra_messaggio_info("Funzione di modifica in sviluppo")
    
    def mostra_messaggio_errore(self, messaggio):
        """Mostra un messaggio di errore"""
        print(f"❌ ERRORE: {messaggio}")
        # TODO: Implementare dialog o notifica visiva
    
    def mostra_messaggio_successo(self, messaggio):
        """Mostra un messaggio di successo"""
        print(f"✅ SUCCESSO: {messaggio}")
        # TODO: Implementare dialog o notifica visiva
    
    def mostra_messaggio_info(self, messaggio):
        """Mostra un messaggio informativo"""
        print(f"ℹ️ INFO: {messaggio}")
        # TODO: Implementare dialog o notifica visiva
    
    def mostra_statistiche(self, widget):
        """Mostra la pagina valutazione giocatori"""
        self.pagina_corrente = "valutazione"
        self.aggiorna_menu_attivo("statistiche")
        self.top_bar_title.text = "⭐ VALUTAZIONE GIOCATORI"
        
        # Pulisce il contenuto 
        self.dynamic_content.clear()
        
        # Contenuto valutazione
        self.dynamic_content.add(self.crea_interfaccia_valutazione_nuova())
    
    def crea_interfaccia_valutazione(self):
        """Crea l'interfaccia per la valutazione dei giocatori"""
        print("⭐ DEBUG VALUTAZIONE: Creazione interfaccia valutazione iniziata")
        
        # Container principale con layout a due colonne
        main_container = toga.Box(style=Pack(
            direction=COLUMN,
            padding=10,
            flex=1,
            background_color="#f8f9fa"
        ))
        
        # Titolo principale
        main_title = toga.Label(
            "⭐ VALUTAZIONE GIOCATORI",
            style=Pack(
                font_size=self.config['title_font_size'],
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                padding=(0, 0, 15, 0)
            )
        )
        main_container.add(main_title)
        
        # Container per le due colonne (layout orizzontale)
        two_columns_container = toga.Box(style=Pack(
            direction=ROW,
            flex=1,
            padding=5
        ))
        
        # SEZIONE SUPERIORE: Lista giocatori (che funzionava)
        lista_column = toga.Box(style=Pack(
            direction=COLUMN,
            padding=10,
            height=300,  # Altezza fissa per i giocatori
            background_color="#f8f9fa"
        ))
        
        # Titolo
        title = toga.Label(
            "� SELEZIONA GIOCATORE",
            style=Pack(
                font_size=self.config['button_font_size'],
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                padding=10,
                background_color="#ecf0f1"
            )
        )
        lista_column.add(title)
        

        

        
        # ScrollContainer per i giocatori
        self.lista_giocatori_content = toga.Box(style=Pack(
            direction=COLUMN,
            padding=5
        ))
        
        scroll_container = toga.ScrollContainer(
            content=self.lista_giocatori_content,
            style=Pack(
                flex=1,
                height=400  # Altezza fissa per garantire visibilità
            )
        )
        lista_column.add(scroll_container)
        
        # SEZIONE INFERIORE: Scheda valutazione
        scheda_column = toga.Box(style=Pack(
            direction=COLUMN,
            padding=10,
            flex=1,  # Prende il resto dello spazio
            background_color="#ffffff"
        ))
        
        # Titolo scheda
        scheda_title = toga.Label(
            "⭐ SCHEDA VALUTAZIONE",
            style=Pack(
                font_size=self.config['button_font_size'],
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                padding=10,
                background_color="#e8f5e8"
            )
        )
        scheda_column.add(scheda_title)
        
        # Container per la scheda
        self.scheda_valutazione_content = toga.Box(style=Pack(
            direction=COLUMN,
            padding=10,
            flex=1
        ))
        scheda_column.add(self.scheda_valutazione_content)
        
        # Messaggio iniziale
        messaggio_iniziale = toga.Label(
            "Seleziona un giocatore dalla lista\nper visualizzare la sua valutazione",
            style=Pack(
                font_size=self.config['label_font_size'],
                color="#7f8c8d",
                text_align=CENTER,
                padding=20
            )
        )
        self.scheda_valutazione_content.add(messaggio_iniziale)
        
        # Aggiungi entrambe le sezioni verticalmente
        two_columns_container.add(lista_column)
        two_columns_container.add(scheda_column)
        
        # Carica la lista giocatori
        print("⭐ DEBUG: Chiamando carica_lista_giocatori_valutazione...")
        self.carica_lista_giocatori_valutazione()
        print(f"⭐ DEBUG: Lista caricata, container ha {len(self.lista_giocatori_content.children)} figli")
        
        return main_container
    
    def crea_interfaccia_valutazione_nuova(self):
        """Interfaccia per la valutazione con layout a due colonne funzionante"""
        print("⭐ DEBUG VALUTAZIONE: Creazione interfaccia valutazione a due colonne")
        
        # Container principale
        main_container = toga.Box(style=Pack(
            direction=COLUMN,
            padding=5,
            flex=1
        ))
        
        # Titolo principale
        main_title = toga.Label(
            "⭐ VALUTAZIONE GIOCATORI",
            style=Pack(
                font_size=self.config['title_font_size'],
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                padding=10
            )
        )
        main_container.add(main_title)
        
        # Container per layout a due colonne - approccio semplificato
        row_container = toga.Box(style=Pack(
            direction=ROW,
            flex=1
        ))
        
        # COLONNA SINISTRA: Lista giocatori
        left_box = toga.Box(style=Pack(
            direction=COLUMN,
            width=300,  # Larghezza fissa per evitare problemi
            padding=5
        ))
        
        # Titolo colonna sinistra
        left_title = toga.Label(
            "📋 SELEZIONA GIOCATORE",
            style=Pack(
                font_size=14,
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                padding=5,
                background_color="#e8f4fd"
            )
        )
        left_box.add(left_title)
        
        # Container per i giocatori - approccio minimalista
        self.lista_giocatori_content = toga.Box(style=Pack(
            direction=COLUMN,
            flex=1
        ))
        left_box.add(self.lista_giocatori_content)
        
        # COLONNA DESTRA: Scheda valutazione
        right_box = toga.Box(style=Pack(
            direction=COLUMN,
            flex=1,
            padding=5
        ))
        
        # Titolo colonna destra
        right_title = toga.Label(
            "⭐ SCHEDA VALUTAZIONE",
            style=Pack(
                font_size=14,
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                padding=5,
                background_color="#e8f5e8"
            )
        )
        right_box.add(right_title)
        
        # Container per la scheda
        self.scheda_valutazione_content = toga.Box(style=Pack(
            direction=COLUMN,
            flex=1,
            padding=10
        ))
        
        # Messaggio iniziale
        messaggio_iniziale = toga.Label(
            "Seleziona un giocatore dalla colonna sinistra\nper visualizzare la sua scheda di valutazione",
            style=Pack(
                font_size=self.config['label_font_size'],
                color="#7f8c8d",
                text_align=CENTER,
                padding=20
            )
        )
        self.scheda_valutazione_content.add(messaggio_iniziale)
        right_box.add(self.scheda_valutazione_content)
        
        # Aggiungi le due colonne al container orizzontale
        row_container.add(left_box)
        row_container.add(right_box)
        
        # Aggiungi tutto al container principale
        main_container.add(row_container)
        
        # Variabile per il giocatore selezionato
        self.giocatore_selezionato_id = None
        
        # Carica la lista giocatori
        print("🔧 DEBUG: Chiamando carica_lista_giocatori_valutazione...")
        self.carica_lista_giocatori_valutazione()
        print(f"🔧 DEBUG: Container giocatori ha {len(self.lista_giocatori_content.children)} elementi")
        
        return main_container

    def mostra_scheda_giocatore_semplice(self, giocatore):
        """Mostra la scheda di valutazione semplificata per un giocatore"""
        print(f"📋 Mostrando scheda per: {giocatore.get('nome')} {giocatore.get('cognome')}")
        
        # Pulisce la scheda
        self.scheda_valutazione_content.clear()
        
        # Header giocatore
        nome_completo = f"{giocatore.get('nome', 'N/A')} {giocatore.get('cognome', 'N/A')}"
        header = toga.Label(
            f"⭐ VALUTAZIONE\n{nome_completo}",
            style=Pack(
                font_size=self.config['button_font_size'],
                font_weight="bold",
                color="#ffffff",
                background_color="#3498db",
                text_align=CENTER,
                padding=15
            )
        )
        self.scheda_valutazione_content.add(header)
        
        # Calcola statistiche basilari
        statistiche = self.calcola_statistiche_giocatore(giocatore.get('id'))
        valutazione = self.calcola_valutazione_media(statistiche)
        
        # Valutazione
        valutazione_label = toga.Label(
            f"VALUTAZIONE MEDIA: {valutazione:.1f}/10.0",
            style=Pack(
                font_size=16,
                font_weight="bold",
                color="#27ae60",
                text_align=CENTER,
                padding=10
            )
        )
        self.scheda_valutazione_content.add(valutazione_label)
        
        # Statistiche complete
        val_info = ""
        if statistiche.get('numero_valutazioni', 0) > 0:
            val_info = f"""

📈 PRESTAZIONI INDIVIDUALI:
• Valutazione Media: {statistiche['valutazione_media']:.1f}
• Plus/Minus Totale: {statistiche['plus_minus_totale']:+.0f}
• Plus/Minus Medio: {statistiche['plus_minus_medio']:+.1f}"""
        
        stats_text = f"""📊 STATISTICHE COMPLETE:

🏃 ALLENAMENTI:
• Presenze: {statistiche['presenze']}/{statistiche['totale_allenamenti']}
• Assenze: {statistiche['assenze']}
• Assenze Giustificate: {statistiche['assenze_giustificate']}
• Percentuale Presenze: {statistiche['percentuale_presenze']:.1f}%

⚽ PARTITE:
• Convocazioni: {statistiche.get('convocazioni', 0)}/{statistiche.get('totale_partite', 0)}
• Partite Giocate: {statistiche.get('partite_giocate', 0)}
• Percentuale Convocazioni: {statistiche.get('percentuale_convocazioni', 0):.1f}%{val_info}"""
        
        stats_label = toga.Label(
            stats_text,
            style=Pack(
                font_size=self.config['label_font_size'],
                color="#2c3e50",
                padding=15
            )
        )
        self.scheda_valutazione_content.add(stats_label)
        
        print(f"📋 Scheda mostrata per: {nome_completo}")
    
    def crea_interfaccia_valutazione_BACKUP(self):
        """BACKUP della funzione originale"""
        print("⭐ DEBUG VALUTAZIONE: Creazione interfaccia valutazione iniziata")
        
        # Container principale semplificato
        container = toga.Box(style=Pack(
            direction=COLUMN,  # Cambiato da ROW a COLUMN per test
            padding=10,
            flex=1,
            background_color="#ff0000"  # ROSSO per vedere se il container principale esiste
        ))
        
        # SOLO COLONNA SINISTRA per test
        lista_column = toga.Box(style=Pack(
            direction=COLUMN, 
            padding=10,
            flex=1,
            background_color="#00ff00"  # VERDE per vedere la colonna
        ))
        
        # Titolo lista giocatori
        lista_title = toga.Label(
            "👥 SELEZIONA GIOCATORE",
            style=Pack(
                font_size=self.config['button_font_size'],
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                padding=10,
                background_color="#ecf0f1"
            )
        )
        lista_column.add(lista_title)
        
        # Test button NELLA COLONNA PRINCIPALE
        test_btn_colonna = toga.Button(
            "🚀 TEST COLONNA PRINCIPALE",
            style=Pack(
                width=-1,
                height=40,
                background_color="#9b59b6",
                color="#ffffff",
                font_size=self.config['button_font_size']
            )
        )
        
        def test_colonna_click(widget):
            print("🚀🚀🚀 COLONNA PRINCIPALE FUNZIONA!")
            self.scheda_valutazione_content.clear()
            label = toga.Label(
                "� PULSANTE COLONNA PRINCIPALE\nFUNZIONA PERFETTAMENTE!",
                style=Pack(
                    font_size=self.config['button_font_size'],
                    color="#9b59b6",
                    text_align=CENTER,
                    padding=20
                )
            )
            self.scheda_valutazione_content.add(label)
            
        test_btn_colonna.on_press = test_colonna_click
        lista_column.add(test_btn_colonna)
        
        # Container diretto SENZA scroll per test eventi
        self.lista_giocatori_content = toga.Box(style=Pack(
            direction=COLUMN,
            padding=5,
            flex=1
        ))
        lista_column.add(self.lista_giocatori_content)
        
        print("⭐ DEBUG: Container DIRETTO aggiunto (senza scroll)")
        
        # Colonna destra: Scheda valutazione
        scheda_column = toga.Box(style=Pack(
            direction=COLUMN, 
            padding=10, 
            flex=1,
            background_color="#e0e0e0"  # Sfondo grigio chiaro per debug
        ))
        
        # Titolo scheda
        scheda_title = toga.Label(
            "⭐ SCHEDA VALUTAZIONE",
            style=Pack(
                font_size=self.config['button_font_size'],
                font_weight="bold",
                color="#2c3e50",
                text_align=CENTER,
                padding=self.config['padding_medium'],
                background_color="#ecf0f1"
            )
        )
        scheda_column.add(scheda_title)
        
        # Container scrollabile per la scheda
        self.scheda_valutazione_scroll = toga.ScrollContainer(
            style=Pack(
                flex=1,
                padding=self.config['padding_small'],
                height=500,
                background_color="#f8f9fa"
            )
        )
        
        # Box interno per la scheda
        self.scheda_valutazione_content = toga.Box(style=Pack(direction=COLUMN))
        self.scheda_valutazione_scroll.content = self.scheda_valutazione_content
        scheda_column.add(self.scheda_valutazione_scroll)
        
        # Messaggio iniziale con colore diverso per test visibilità
        messaggio_iniziale = toga.Label(
            "🎯 SCHEDA VALUTAZIONE\n\nSeleziona un giocatore dalla lista\nper visualizzare la sua valutazione\n\n(Se vedi questo messaggio,\nla colonna destra funziona)",
            style=Pack(
                font_size=self.config['label_font_size'],
                color="#e74c3c",
                text_align=CENTER,
                padding=20,
                background_color="#ffffff"
            )
        )
        self.scheda_valutazione_content.add(messaggio_iniziale)
        
        container.add(lista_column)
        container.add(scheda_column)
        
        # Carica la lista giocatori
        # Test diretto: aggiungi un pulsante di prova al container
        test_direct = toga.Button(
            "TEST DIRETTO CONTAINER",
            style=Pack(
                width=-1,
                height=40,
                background_color="#27ae60",
                color="#ffffff"
            )
        )
        self.lista_giocatori_content.add(test_direct)
        print("⭐ DEBUG VALUTAZIONE: Pulsante test diretto aggiunto")
        
        print("⭐ DEBUG VALUTAZIONE: Chiamando carica_lista_giocatori_valutazione...")
        self.carica_lista_giocatori_valutazione()
        
        print(f"⭐ DEBUG VALUTAZIONE: Container ha {len(self.lista_giocatori_content.children)} figli")
        print("⭐ DEBUG VALUTAZIONE: Interfaccia valutazione creata e ritornata")
        return container
    
    def carica_lista_giocatori_valutazione(self):
        """Carica la lista dei giocatori per la valutazione"""
        print("⭐ DEBUG VALUTAZIONE: Caricamento lista giocatori")
        
        # Verifica che il container esista
        if not hasattr(self, 'lista_giocatori_content') or self.lista_giocatori_content is None:
            print("❌ ERROR: Container lista_giocatori_content non trovato!")
            return
        
        # Pulisce la lista esistente
        self.lista_giocatori_content.clear()
        
        try:
            # Ottieni tutti i giocatori
            giocatori_service = GiocatoriService(self.db_manager)
            giocatori = giocatori_service.ottieni_tutti_giocatori()
            
            print(f"⭐ DEBUG VALUTAZIONE: Trovati {len(giocatori)} giocatori")
            print(f"⭐ DEBUG VALUTAZIONE: Container esistente: {self.lista_giocatori_content is not None}")
            print(f"⭐ DEBUG VALUTAZIONE: Container figli prima: {len(self.lista_giocatori_content.children)}")
            
            if giocatori:
                print(f"🔧 Creando {len(giocatori)} pulsanti giocatori...")
                
                for i, giocatore in enumerate(giocatori):
                    nome_completo = f"{giocatore.get('nome', 'N/A')} {giocatore.get('cognome', 'N/A')}"
                    
                    # Pulsante semplice e diretto
                    btn_giocatore = toga.Button(
                        nome_completo,
                        style=Pack(
                            width=280,  # Larghezza fissa
                            height=40,
                            background_color="#e74c3c",
                            color="#ffffff",
                            font_size=12,
                            padding=3
                        )
                    )
                    
                    # Handler semplificato
                    def crea_handler(player_data):
                        def handler(widget):
                            print(f"🎯 CLICK: {player_data.get('nome')} {player_data.get('cognome')}")
                            self.mostra_scheda_giocatore_semplice(player_data)
                        return handler
                    
                    btn_giocatore.on_press = crea_handler(giocatore)
                    self.lista_giocatori_content.add(btn_giocatore)
                    print(f"✅ Aggiunto pulsante per: {nome_completo}")
                    
                    # Separatore piccolo
                    if i < len(giocatori) - 1:
                        spacer = toga.Box(style=Pack(height=2))
                        self.lista_giocatori_content.add(spacer)
                        
            else:
                nessun_giocatore = toga.Label(
                    "Nessun giocatore registrato",
                    style=Pack(
                        font_size=self.config['label_font_size'],
                        color="#7f8c8d",
                        text_align=CENTER,
                        padding=20
                    )
                )
                self.lista_giocatori_content.add(nessun_giocatore)
                
        except Exception as e:
            print(f"⭐ DEBUG VALUTAZIONE: Errore caricamento giocatori: {str(e)}")
            error_label = toga.Label(
                f"Errore caricamento: {str(e)}",
                style=Pack(
                    font_size=self.config['label_font_size'],
                    color="#e74c3c",
                    text_align=CENTER,
                    padding=20
                )
            )
            self.lista_giocatori_content.add(error_label)
    
    def crea_item_giocatore_valutazione(self, giocatore):
        """Crea una card elegante per il giocatore nella valutazione"""
        print(f"📝 Creando card per: {giocatore.get('nome')} {giocatore.get('cognome')}")
        
        # Container della card
        card_container = toga.Box(style=Pack(
            direction=COLUMN,
            padding=5,
            background_color="#ffffff"
        ))
        
        # Informazioni giocatore
        nome_completo = f"{giocatore.get('nome', 'N/A')} {giocatore.get('cognome', 'N/A')}"
        
        # Dettagli giocatore
        dettagli_parts = []
        if giocatore.get('data_nascita'):
            try:
                anno = giocatore['data_nascita'].split('-')[0] if isinstance(giocatore['data_nascita'], str) else str(giocatore['data_nascita'].year)
                dettagli_parts.append(f"Anno: {anno}")
            except:
                pass
        if giocatore.get('numero_maglia'):
            dettagli_parts.append(f"N° {giocatore['numero_maglia']}")
        
        dettagli = " • ".join(dettagli_parts)
        
        # Handler per la selezione
        giocatore_data = giocatore.copy()  # Copia i dati per evitare problemi di closure
        
        def seleziona_giocatore(widget):
            print(f"🎯 SELEZIONATO: {nome_completo}")
            self.giocatore_selezionato_id = giocatore_data['id']
            self.mostra_scheda_giocatore_semplice(giocatore_data)
        
        # Pulsante card selezionabile
        card_button = toga.Button(
            f"{nome_completo}\n{dettagli}",
            on_press=seleziona_giocatore,
            style=Pack(
                width=-1,
                height=70,
                background_color="#3498db",
                color="#ffffff",
                font_size=self.config['label_font_size'],
                padding=8,
                text_align=CENTER
            )
        )
        
        card_container.add(card_button)
        print(f"📝 Card creata per: {nome_completo}")
        return card_container
    
    def crea_dettagli_giocatore(self, giocatore):
        """Crea la stringa dei dettagli del giocatore"""
        dettagli_parts = []
        
        # Anno di nascita
        if giocatore.get('data_nascita'):
            try:
                # Estrae l'anno dalla data di nascita
                data_nascita = giocatore['data_nascita']
                if isinstance(data_nascita, str):
                    # Assume formato YYYY-MM-DD
                    anno = data_nascita.split('-')[0]
                    dettagli_parts.append(f"Anno: {anno}")
                else:
                    dettagli_parts.append(f"Anno: {data_nascita.year}")
            except:
                pass
        
        # Numero di maglia
        if giocatore.get('numero_maglia'):
            dettagli_parts.append(f"N° {giocatore['numero_maglia']}")
        
        # Posizione (se disponibile)
        if giocatore.get('posizione'):
            dettagli_parts.append(f"Pos: {giocatore['posizione']}")
        
        # Crea la stringa dei dettagli
        return " • ".join(dettagli_parts) if dettagli_parts else "Dettagli non disponibili"
    
    def mostra_scheda_giocatore(self, giocatore):
        """Mostra la scheda di valutazione per un giocatore specifico"""
        print(f"🔍 SCHEDA: Inizio per {giocatore.get('nome')} {giocatore.get('cognome')}")
        
        try:
            # Pulisce la scheda esistente
            print("🔍 SCHEDA: Pulendo contenuto...")
            self.scheda_valutazione_content.clear()
            
            # Test semplice: aggiungi solo un messaggio
            test_label = toga.Label(
                f"✅ GIOCATORE SELEZIONATO:\n{giocatore.get('nome')} {giocatore.get('cognome')}\nID: {giocatore.get('id')}",
                style=Pack(
                    font_size=self.config['button_font_size'],
                    color="#27ae60",
                    text_align=CENTER,
                    padding=20,
                    background_color="#ffffff"
                )
            )
            self.scheda_valutazione_content.add(test_label)
            print("🔍 SCHEDA: Label di test aggiunta")
            
            # Forza refresh
            try:
                if hasattr(self.main_window, 'content'):
                    self.main_window.content.refresh()
                print("🔍 SCHEDA: Refresh forzato")
            except:
                pass
                
        except Exception as e:
            print(f"🔍 SCHEDA: ERRORE: {str(e)}")
            import traceback
            traceback.print_exc()
        
        # Calcola le statistiche del giocatore
        statistiche = self.calcola_statistiche_giocatore(giocatore['id'])
        valutazione_media = self.calcola_valutazione_media(statistiche)
        
        # Header giocatore
        header_box = toga.Box(style=Pack(
            direction=COLUMN,
            padding=self.config['padding_medium'],
            background_color="#3498db",
            alignment=CENTER
        ))
        
        nome_label = toga.Label(
            f"{giocatore['nome']} {giocatore['cognome']}",
            style=Pack(
                font_size=self.config['title_font_size'],
                font_weight="bold",
                color="#ffffff",
                text_align=CENTER
            )
        )
        
        valutazione_label = toga.Label(
            f"⭐ VALUTAZIONE: {valutazione_media:.1f}/10.0",
            style=Pack(
                font_size=self.config['button_font_size'],
                font_weight="bold",
                color="#ffffff",
                text_align=CENTER,
                padding=(5, 0)
            )
        )
        
        header_box.add(nome_label)
        header_box.add(valutazione_label)
        self.scheda_valutazione_content.add(header_box)
        
        # Statistiche dettagliate
        self.aggiungi_statistiche_dettagliate(statistiche)
        
    def calcola_statistiche_giocatore(self, giocatore_id):
        """Calcola tutte le statistiche per un giocatore specifico"""
        print(f"⭐ DEBUG VALUTAZIONE: Calcolo statistiche per giocatore ID {giocatore_id}")
        
        statistiche = {
            'presenze': 0,
            'assenze': 0,
            'assenze_giustificate': 0,
            'totale_allenamenti': 0,
            'percentuale_presenze': 0.0,
            'partite_giocate': 0,
            'convocazioni': 0,
            'convocazioni_rifiutate': 0,
            'percentuale_convocazioni': 0.0
        }
        
        try:
            # Statistiche allenamenti
            allenamenti_service = AllenamentiService(self.db_manager)
            tutti_allenamenti = allenamenti_service.ottieni_tutti_allenamenti()
            
            statistiche['totale_allenamenti'] = len(tutti_allenamenti)
            
            # Conta presenze e assenze
            for allenamento in tutti_allenamenti:
                presenze_str = allenamento.get('presenze', '[]')
                assenze_giustificate_str = allenamento.get('assenze_giustificate', '[]')
                
                # Decodifica presenze
                presenze = []
                if presenze_str:
                    try:
                        presenze = json.loads(presenze_str) if isinstance(presenze_str, str) else presenze_str
                        if not isinstance(presenze, list):
                            presenze = []
                    except:
                        presenze = []
                
                # Decodifica assenze giustificate
                assenze_giustificate = []
                if assenze_giustificate_str:
                    try:
                        assenze_giustificate = json.loads(assenze_giustificate_str) if isinstance(assenze_giustificate_str, str) else assenze_giustificate_str
                        if not isinstance(assenze_giustificate, list):
                            assenze_giustificate = []
                    except:
                        assenze_giustificate = []
                
                # Controlla presenza del giocatore
                if giocatore_id in presenze:
                    statistiche['presenze'] += 1
                elif giocatore_id in assenze_giustificate:
                    statistiche['assenze_giustificate'] += 1
                else:
                    statistiche['assenze'] += 1
            
            # Calcola percentuale presenze
            if statistiche['totale_allenamenti'] > 0:
                statistiche['percentuale_presenze'] = (statistiche['presenze'] / statistiche['totale_allenamenti']) * 100
            
            # STATISTICHE PARTITE E CONVOCAZIONI
            partite_service = PartiteService(self.db_manager)
            convocati_service = ConvocatiService(self.db_manager)
            
            # Ottieni tutte le partite
            tutte_partite = partite_service.ottieni_tutte_partite()
            statistiche['totale_partite'] = len(tutte_partite)
            
            # Conta convocazioni e partite giocate
            for partita in tutte_partite:
                # Controlla se è stato convocato
                convocati = convocati_service.ottieni_convocati_partita(partita['id'])
                convocato_data = next((c for c in convocati if c['giocatore_id'] == giocatore_id), None)
                
                if convocato_data:
                    # Se è stato convocato
                    if convocato_data.get('rifiutata', False):
                        # Convocazione rifiutata
                        statistiche['convocazioni_rifiutate'] += 1
                    else:
                        # Convocazione accettata
                        statistiche['convocazioni'] += 1
                        # Controlla se ha giocato (presenza nel tabellino)
                        # Per ora assumiamo che se è convocato e non ha rifiutato, ha giocato
                        statistiche['partite_giocate'] += 1
            
            # Calcola percentuale convocazioni
            if statistiche['totale_partite'] > 0:
                statistiche['percentuale_convocazioni'] = (statistiche['convocazioni'] / statistiche['totale_partite']) * 100
            
            # STATISTICHE INDIVIDUALI DALLE PARTITE (VAL e +/-)
            statistiche_service = StatisticheService(self.db_manager)
            
            # Ottieni tutte le statistiche individuali del giocatore
            tutte_statistiche_giocatore = []
            try:
                conn = sqlite3.connect(self.db_manager.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT valutazione, plus_minus 
                    FROM statistiche_giocatori 
                    WHERE giocatore_id = ? AND (valutazione > 0 OR plus_minus != 0)
                """, (giocatore_id,))
                tutte_statistiche_giocatore = cursor.fetchall()
                conn.close()
            except Exception as e:
                print(f"⭐ DEBUG: Errore lettura statistiche individuali: {e}")
            
            # Calcola medie delle valutazioni individuali
            if tutte_statistiche_giocatore:
                valutazioni = [s[0] for s in tutte_statistiche_giocatore if s[0] > 0]
                plus_minus_values = [s[1] for s in tutte_statistiche_giocatore]
                
                statistiche['numero_valutazioni'] = len(valutazioni)
                statistiche['valutazione_media'] = sum(valutazioni) / len(valutazioni) if valutazioni else 0.0
                statistiche['plus_minus_totale'] = sum(plus_minus_values)
                statistiche['plus_minus_medio'] = sum(plus_minus_values) / len(plus_minus_values) if plus_minus_values else 0.0
            else:
                statistiche['numero_valutazioni'] = 0
                statistiche['valutazione_media'] = 0.0
                statistiche['plus_minus_totale'] = 0.0
                statistiche['plus_minus_medio'] = 0.0
            
            print(f"⭐ DEBUG VALUTAZIONE: Statistiche complete calcolate: {statistiche}")
            return statistiche
            
        except Exception as e:
            print(f"⭐ DEBUG VALUTAZIONE: Errore calcolo statistiche: {str(e)}")
            return statistiche
    
    def calcola_valutazione_media(self, statistiche):
        """Calcola la valutazione media da 0 a 10 basata su tutte le statistiche dell'app"""
        print("⭐ DEBUG VALUTAZIONE: Calcolo valutazione media completa")
        
        # Pesi per i diversi fattori (aggiornati per includere VAL e +/-)
        peso_presenze_allenamenti = 0.25  # 25% del voto basato sulle presenze agli allenamenti
        peso_convocazioni = 0.25          # 25% del voto basato sulle convocazioni
        peso_partite_giocate = 0.15       # 15% del voto basato sulle partite giocate
        peso_valutazioni_partite = 0.25   # 25% del voto basato sulle valutazioni nelle partite (VAL)
        peso_plus_minus = 0.05            # 5% del voto basato sul +/-
        peso_assenze_giustificate = 0.05  # 5% bonus per assenze giustificate
        
        # 1. PUNTEGGIO PRESENZE ALLENAMENTI (0-10)
        punteggio_presenze = 0.0
        if statistiche['percentuale_presenze'] >= 90:
            punteggio_presenze = 10.0
        elif statistiche['percentuale_presenze'] >= 80:
            punteggio_presenze = 8.5
        elif statistiche['percentuale_presenze'] >= 70:
            punteggio_presenze = 7.0
        elif statistiche['percentuale_presenze'] >= 60:
            punteggio_presenze = 5.5
        elif statistiche['percentuale_presenze'] >= 50:
            punteggio_presenze = 4.0
        elif statistiche['percentuale_presenze'] >= 30:
            punteggio_presenze = 2.5
        else:
            punteggio_presenze = 1.0
        
        # 2. PUNTEGGIO CONVOCAZIONI (0-10)
        punteggio_convocazioni = 0.0
        if statistiche.get('totale_partite', 0) > 0:
            if statistiche['percentuale_convocazioni'] >= 80:
                punteggio_convocazioni = 10.0
            elif statistiche['percentuale_convocazioni'] >= 70:
                punteggio_convocazioni = 8.5
            elif statistiche['percentuale_convocazioni'] >= 60:
                punteggio_convocazioni = 7.0
            elif statistiche['percentuale_convocazioni'] >= 50:
                punteggio_convocazioni = 5.5
            elif statistiche['percentuale_convocazioni'] >= 40:
                punteggio_convocazioni = 4.0
            elif statistiche['percentuale_convocazioni'] >= 20:
                punteggio_convocazioni = 2.5
            else:
                punteggio_convocazioni = 1.0
        else:
            punteggio_convocazioni = 6.0  # Valore neutro se non ci sono partite
        
        # 3. PUNTEGGIO PARTITE GIOCATE (0-10)
        punteggio_partite = 0.0
        if statistiche.get('convocazioni', 0) > 0:
            percentuale_giocate = (statistiche['partite_giocate'] / statistiche['convocazioni']) * 100
            if percentuale_giocate >= 90:
                punteggio_partite = 10.0
            elif percentuale_giocate >= 80:
                punteggio_partite = 8.0
            elif percentuale_giocate >= 70:
                punteggio_partite = 6.5
            elif percentuale_giocate >= 50:
                punteggio_partite = 5.0
            else:
                punteggio_partite = 3.0
        else:
            punteggio_partite = 6.0  # Valore neutro se non è mai stato convocato
        
        # 4. PUNTEGGIO VALUTAZIONI PARTITE (VAL) (0-10)
        punteggio_val = 6.0  # Valore neutro di default
        if statistiche.get('numero_valutazioni', 0) > 0:
            val_media = statistiche['valutazione_media']
            # Scala le valutazioni da 0-30 (tipico range basket) a 0-10
            if val_media >= 25:
                punteggio_val = 10.0
            elif val_media >= 20:
                punteggio_val = 8.5
            elif val_media >= 15:
                punteggio_val = 7.0
            elif val_media >= 10:
                punteggio_val = 5.5
            elif val_media >= 5:
                punteggio_val = 4.0
            elif val_media > 0:
                punteggio_val = 2.5
            else:
                punteggio_val = 1.0
        
        # 5. PUNTEGGIO +/- (0-10)
        punteggio_plus_minus = 5.0  # Valore neutro di default
        if statistiche.get('numero_valutazioni', 0) > 0:
            plus_minus_medio = statistiche['plus_minus_medio']
            # Scala il +/- da tipico range -20/+20 a 0-10
            if plus_minus_medio >= 10:
                punteggio_plus_minus = 10.0
            elif plus_minus_medio >= 5:
                punteggio_plus_minus = 8.0
            elif plus_minus_medio >= 0:
                punteggio_plus_minus = 6.0
            elif plus_minus_medio >= -5:
                punteggio_plus_minus = 4.0
            elif plus_minus_medio >= -10:
                punteggio_plus_minus = 2.0
            else:
                punteggio_plus_minus = 0.0
        
        # 6. BONUS ASSENZE GIUSTIFICATE (0-1)
        bonus_giustificate = 0.0
        if statistiche['totale_allenamenti'] > 0:
            percentuale_giustificate = (statistiche['assenze_giustificate'] / statistiche['totale_allenamenti']) * 100
            bonus_giustificate = min(1.0, percentuale_giustificate / 15)  # Bonus fino a 1 punto
        
        # 7. PENALITÀ CONVOCAZIONI RIFIUTATE
        penalita_rifiutate = 0.0
        if statistiche.get('convocazioni_rifiutate', 0) > 0:
            # Penalità proporzionale al numero di rifiuti
            # Ogni rifiuto toglie 0.5 punti, max 3 punti di penalità
            penalita_rifiutate = min(3.0, statistiche['convocazioni_rifiutate'] * 0.5)
        
        # CALCOLO FINALE
        valutazione = (
            (punteggio_presenze * peso_presenze_allenamenti) +
            (punteggio_convocazioni * peso_convocazioni) +
            (punteggio_partite * peso_partite_giocate) +
            (punteggio_val * peso_valutazioni_partite) +
            (punteggio_plus_minus * peso_plus_minus) +
            (bonus_giustificate * peso_assenze_giustificate) -
            penalita_rifiutate
        )
        
        # Assicura il range 0-10
        valutazione = min(10.0, max(0.0, valutazione))
        
        print(f"⭐ DEBUG VALUTAZIONE: Dettagli calcolo:")
        print(f"  - Presenze allenamenti: {punteggio_presenze:.1f}/10 (peso {peso_presenze_allenamenti})")
        print(f"  - Convocazioni: {punteggio_convocazioni:.1f}/10 (peso {peso_convocazioni})")
        print(f"  - Partite giocate: {punteggio_partite:.1f}/10 (peso {peso_partite_giocate})")
        print(f"  - Valutazioni partite (VAL): {punteggio_val:.1f}/10 (peso {peso_valutazioni_partite}) - Media: {statistiche.get('valutazione_media', 0):.1f}")
        print(f"  - Plus/Minus: {punteggio_plus_minus:.1f}/10 (peso {peso_plus_minus}) - Media: {statistiche.get('plus_minus_medio', 0):.1f}")
        print(f"  - Bonus giustificate: {bonus_giustificate:.1f}/1 (peso {peso_assenze_giustificate})")
        print(f"  - Penalità rifiuti: -{penalita_rifiutate:.1f} punti ({statistiche.get('convocazioni_rifiutate', 0)} rifiuti)")
        print(f"⭐ DEBUG VALUTAZIONE: Valutazione finale: {valutazione:.1f}/10")
        
        return valutazione
    
    def aggiungi_statistiche_dettagliate(self, statistiche):
        """Aggiunge le statistiche dettagliate alla scheda"""
        
        # Sezione Allenamenti
        sezione_allenamenti = toga.Box(style=Pack(
            direction=COLUMN,
            padding=self.config['padding_medium'],
            background_color="#ffffff"
        ))
        
        titolo_allenamenti = toga.Label(
            "🏃 STATISTICHE ALLENAMENTI",
            style=Pack(
                font_size=self.config['button_font_size'],
                font_weight="bold",
                color="#27ae60",
                padding=(0, 0, 10, 0)
            )
        )
        sezione_allenamenti.add(titolo_allenamenti)
        
        # Statistiche allenamenti
        stats_allenamenti = [
            f"Presenze: {statistiche['presenze']}",
            f"Assenze: {statistiche['assenze']}",
            f"Assenze Giustificate: {statistiche['assenze_giustificate']}",
            f"Totale Allenamenti: {statistiche['totale_allenamenti']}",
            f"Percentuale Presenze: {statistiche['percentuale_presenze']:.1f}%"
        ]
        
        for stat in stats_allenamenti:
            stat_label = toga.Label(
                stat,
                style=Pack(
                    font_size=self.config['label_font_size'],
                    color="#2c3e50",
                    padding=(2, 0)
                )
            )
            sezione_allenamenti.add(stat_label)
        
        self.scheda_valutazione_content.add(sezione_allenamenti)
        
        # Separatore
        separator = toga.Box(style=Pack(
            height=2,
            background_color="#bdc3c7",
            padding=(10, 0)
        ))
        self.scheda_valutazione_content.add(separator)
        
        # Sezione Partite e Convocazioni
        sezione_partite = toga.Box(style=Pack(
            direction=COLUMN,
            padding=self.config['padding_medium'],
            background_color="#ffffff"
        ))
        
        titolo_partite = toga.Label(
            "⚽ STATISTICHE PARTITE E CONVOCAZIONI",
            style=Pack(
                font_size=self.config['button_font_size'],
                font_weight="bold",
                color="#e74c3c",
                padding=(0, 0, 10, 0)
            )
        )
        sezione_partite.add(titolo_partite)
        
        # Statistiche partite e convocazioni
        stats_partite = [
            f"Totale Partite: {statistiche.get('totale_partite', 0)}",
            f"Convocazioni: {statistiche['convocazioni']}",
            f"Convocazioni Rifiutate: {statistiche.get('convocazioni_rifiutate', 0)}",
            f"Partite Giocate: {statistiche['partite_giocate']}",
            f"Percentuale Convocazioni: {statistiche['percentuale_convocazioni']:.1f}%"
        ]
        
        for stat in stats_partite:
            # Evidenzia le convocazioni rifiutate se presenti
            color = "#e74c3c" if "Rifiutate" in stat and statistiche.get('convocazioni_rifiutate', 0) > 0 else "#2c3e50"
            
            stat_label = toga.Label(
                stat,
                style=Pack(
                    font_size=self.config['label_font_size'],
                    color=color,
                    padding=(2, 0)
                )
            )
            sezione_partite.add(stat_label)
        
        self.scheda_valutazione_content.add(sezione_partite)
    
    def mostra_errore(self, messaggio):
        """Mostra un dialogo di errore"""
        self.main_window.info_dialog("Errore", messaggio)
    
    def mostra_successo(self, messaggio):
        """Mostra un dialogo di successo"""
        self.main_window.info_dialog("Successo", messaggio)
    
    def mostra_avviso(self, messaggio):
        """Mostra un dialogo di avviso"""
        self.main_window.info_dialog("Avviso", messaggio)
    
    def gestisci_convocati(self, partita):
        """Gestisce i convocati per una partita"""
        print(f"🔍 DEBUG: gestisci_convocati chiamato per partita: {partita}")
        print(f"🔍 DEBUG: ID partita: {partita.get('id', 'N/A')}")
        print(f"🔍 DEBUG: Avversario: {partita.get('avversario', 'N/A')}")
        print(f"🔍 DEBUG: Data: {partita.get('data', 'N/A')}")
        
        try:
            # Ottieni tutti i giocatori attivi
            print(f"🔍 DEBUG: Ottenendo giocatori disponibili...")
            giocatori_disponibili = self.giocatori_service.ottieni_tutti_giocatori()
            print(f"🔍 DEBUG: Trovati {len(giocatori_disponibili)} giocatori disponibili")
            
            if not giocatori_disponibili:
                print(f"🔍 DEBUG: Nessun giocatore disponibile - mostrando errore")
                self.mostra_errore("Nessun giocatore disponibile per la convocazione")
                return
            
            # Ottieni convocati attuali
            print(f"🔍 DEBUG: Ottenendo convocati attuali per partita ID {partita['id']}...")
            convocati_attuali = self.convocati_service.ottieni_convocati_partita(partita['id'])
            print(f"🔍 DEBUG: Trovati {len(convocati_attuali)} convocati attuali")
            convocati_ids = {c['giocatore_id'] for c in convocati_attuali}
            print(f"🔍 DEBUG: IDs convocati: {convocati_ids}")
            
            # Crea la finestra di selezione
            print(f"🔍 DEBUG: Creando interfaccia dialog convocati...")
            dialog_box = toga.Box(style=Pack(direction=COLUMN, padding=15))
            
            # Titolo
            title_label = toga.Label(
                f"👥 Convocati per: {partita['avversario']}",
                style=Pack(padding=(0, 0, 15, 0), font_size=16, font_weight="bold")
            )
            dialog_box.add(title_label)
            
            # Info partita
            info_label = toga.Label(
                f"📅 {partita['data']} {partita['ora']} - {partita.get('tipologia', 'stagione regolare').title()}",
                style=Pack(padding=(0, 0, 10, 0), color="#666666")
            )
            dialog_box.add(info_label)
            
            # Contatore convocati
            count_label = toga.Label(
                f"Convocati selezionati: {len(convocati_ids)}/12",
                style=Pack(padding=(0, 0, 10, 0), font_weight="bold")
            )
            dialog_box.add(count_label)
            
            # Lista giocatori con checkbox
            giocatori_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
            checkboxes = {}
            
            for giocatore in giocatori_disponibili:
                # Box per ogni giocatore
                giocatore_box = toga.Box(style=Pack(direction=ROW, padding=3))
                
                # Trova se il giocatore è convocato e se ha rifiutato
                convocato_data = next((c for c in convocati_attuali if c['giocatore_id'] == giocatore['id']), None)
                is_convocato = convocato_data is not None
                is_rifiutata = convocato_data.get('rifiutata', False) if convocato_data else False
                
                # Checkbox convocazione
                checkbox_convocato = toga.Switch(
                    text="",
                    value=is_convocato,
                    style=Pack(padding=5)
                )
                
                # Checkbox rifiutata (visibile solo se convocato)
                checkbox_rifiutata = toga.Switch(
                    text="",
                    value=is_rifiutata,
                    style=Pack(padding=5)
                )
                
                # Salva entrambi i checkbox
                checkboxes[giocatore['id']] = {
                    'convocato': checkbox_convocato,
                    'rifiutata': checkbox_rifiutata
                }
                
                # Info giocatore
                numero_maglia = f"#{giocatore['numero_maglia']}" if giocatore['numero_maglia'] else "#--"
                nome_completo = f"{giocatore['nome']} {giocatore['cognome']}"
                
                giocatore_label = toga.Label(
                    f"{numero_maglia} {nome_completo}",
                    style=Pack(flex=1, padding=5)
                )
                
                # Label per i checkbox
                convocato_label = toga.Label("Conv.", style=Pack(padding=2, font_size=10))
                rifiutata_label = toga.Label("Rif.", style=Pack(padding=2, font_size=10, color="#e74c3c"))
                
                # Indicatore idoneità
                idoneita_icon = "✅" if giocatore.get('idoneita_sportiva') else "⚠️"
                idoneita_label = toga.Label(idoneita_icon, style=Pack(padding=5))
                
                # Aggiungi elementi alla riga
                giocatore_box.add(convocato_label)
                giocatore_box.add(checkbox_convocato)
                giocatore_box.add(rifiutata_label)
                giocatore_box.add(checkbox_rifiutata)
                giocatore_box.add(giocatore_label)
                giocatore_box.add(idoneita_label)
                giocatori_box.add(giocatore_box)
                
            # Container scroll per lista giocatori convocati
            giocatori_scroll = toga.ScrollContainer(
                content=giocatori_box,
                style=Pack(height=300)  # Altezza fissa per il dialog
            )
            dialog_box.add(giocatori_scroll)
            
            # Aggiorna contatore quando cambia la selezione
            def aggiorna_contatore():
                selezionati = sum(1 for cb_data in checkboxes.values() if cb_data['convocato'].value)
                rifiutati = sum(1 for cb_data in checkboxes.values() if cb_data['convocato'].value and cb_data['rifiutata'].value)
                count_label.text = f"Convocati: {selezionati}/12 (Rifiutati: {rifiutati})"
                if selezionati > 12:
                    count_label.style.color = "#f44336"  # Rosso se troppi
                else:
                    count_label.style.color = "#000000"  # Nero normale
            
            # Gestione interdipendenza checkbox (se non convocato, non può essere rifiutato)
            def gestisci_checkbox_convocato(giocatore_id, checkbox_convocato, checkbox_rifiutata):
                def on_convocato_change(widget):
                    if not checkbox_convocato.value:
                        # Se non è convocato, non può essere rifiutato
                        checkbox_rifiutata.value = False
                    aggiorna_contatore()
                return on_convocato_change
            
            def gestisci_checkbox_rifiutata(giocatore_id, checkbox_convocato, checkbox_rifiutata):
                def on_rifiutata_change(widget):
                    if checkbox_rifiutata.value and not checkbox_convocato.value:
                        # Se segna rifiutato, deve essere convocato
                        checkbox_convocato.value = True
                    aggiorna_contatore()
                return on_rifiutata_change
            
            # Collega gli eventi ai checkbox
            for giocatore_id, cb_data in checkboxes.items():
                cb_data['convocato'].on_change = gestisci_checkbox_convocato(giocatore_id, cb_data['convocato'], cb_data['rifiutata'])
                cb_data['rifiutata'].on_change = gestisci_checkbox_rifiutata(giocatore_id, cb_data['convocato'], cb_data['rifiutata'])
            
            # Pulsanti
            buttons_box = toga.Box(style=Pack(direction=ROW, padding=10))
            
            salva_button = toga.Button(
                "💾 Salva Convocati",
                on_press=lambda w: self.salva_convocati(partita['id'], checkboxes, giocatori_disponibili),
                style=Pack(flex=1, padding=5, background_color="#4caf50", color="#ffffff")
            )
            
            annulla_button = toga.Button(
                "❌ Annulla",
                on_press=lambda w: self.chiudi_dialog_convocati(),
                style=Pack(flex=1, padding=5, background_color="#f44336", color="#ffffff")
            )
            
            buttons_box.add(salva_button)
            buttons_box.add(annulla_button)
            dialog_box.add(buttons_box)
            
            # Salva riferimenti per uso nei callback
            self.convocati_checkboxes = checkboxes
            self.convocati_giocatori = giocatori_disponibili
            self.convocati_partita_id = partita['id']
            
            # Mostra il dialog (simulato con aggiornamento del contenuto principale)
            print(f"🔍 DEBUG: Mostrando dialog convocati - sostituendo contenuto dynamic_content")
            self.dynamic_content.clear()
            self.dynamic_content.add(dialog_box)
            print(f"🔍 DEBUG: Dialog convocati mostrato con successo!")
            
        except Exception as e:
            print(f"🔍 DEBUG: ERRORE in gestisci_convocati: {str(e)}")
            import traceback
            print(f"🔍 DEBUG: Traceback completo:")
            traceback.print_exc()
            self.mostra_errore(f"Errore nella gestione convocati: {str(e)}")
    
    def salva_convocati(self, partita_id, checkboxes, giocatori_disponibili):
        """Salva la selezione dei convocati con stato rifiutata"""
        print(f"🔍 DEBUG: salva_convocati chiamato")
        print(f"🔍 DEBUG: partita_id: {partita_id}")
        print(f"🔍 DEBUG: checkboxes: {len(checkboxes)} elementi")
        print(f"🔍 DEBUG: giocatori_disponibili: {len(giocatori_disponibili)} giocatori")
        
        try:
            # Prepara i dati dei convocati
            convocati_data = []
            
            for giocatore in giocatori_disponibili:
                cb_data = checkboxes[giocatore['id']]
                is_convocato = cb_data['convocato'].value
                is_rifiutata = cb_data['rifiutata'].value
                
                if is_convocato:
                    giocatore_convocato = giocatore.copy()
                    giocatore_convocato['rifiutata'] = is_rifiutata
                    convocati_data.append(giocatore_convocato)
                    
                    print(f"🔍 DEBUG: Giocatore {giocatore['nome']} {giocatore['cognome']} - Convocato: True, Rifiutata: {is_rifiutata}")
            
            print(f"🔍 DEBUG: {len(convocati_data)} giocatori convocati totali")
            
            if len(convocati_data) > 12:
                print(f"🔍 DEBUG: Troppi giocatori selezionati: {len(convocati_data)}")
                self.mostra_errore("Puoi selezionare massimo 12 giocatori!")
                return
            
            # Aggiorna i convocati nel database
            print(f"🔍 DEBUG: Salvando {len(convocati_data)} convocati nel database...")
            success = self.convocati_service.aggiorna_convocati_partita(partita_id, convocati_data)
            print(f"🔍 DEBUG: Risultato salvataggio: {success}")
            
            if success:
                rifiutati = sum(1 for c in convocati_data if c.get('rifiutata', False))
                print(f"🔍 DEBUG: Convocati salvati con successo! ({rifiutati} rifiutati)")
                
                messaggio = f"Convocati salvati: {len(convocati_data)} giocatori"
                if rifiutati > 0:
                    messaggio += f" ({rifiutati} rifiutati)"
                
                self.mostra_successo(messaggio)
                
                # Aggiorna la sidebar con i nuovi dati
                if hasattr(self, 'sidebar_giocatori_content'):
                    self.aggiorna_sidebar()
                    
                # Torna alla vista partite
                print(f"🔍 DEBUG: Tornando alla vista partite...")
                self.mostra_partite(None)
            else:
                print(f"🔍 DEBUG: Errore nel salvataggio dei convocati")
                self.mostra_errore("Errore nel salvataggio dei convocati")
                
        except Exception as e:
            print(f"🔍 DEBUG: ERRORE in salva_convocati: {str(e)}")
            import traceback
            traceback.print_exc()
            self.mostra_errore(f"Errore nel salvataggio: {str(e)}")
    
    def chiudi_dialog_convocati(self):
        """Chiude il dialog convocati e torna alla vista partite"""
        self.mostra_partite(None)
    
    def modifica_partita(self, partita):
        """Apre il dialog per modificare una partita"""
        print(f"✏️ DEBUG: modifica_partita chiamato per partita: {partita}")
        
        try:
            # Crea un dialog per la modifica
            dialog_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
            
            # Titolo
            title_label = toga.Label(
                f"✏️ Modifica Partita vs {partita['avversario']}",
                style=Pack(padding=(0, 0, 20, 0), font_size=16, font_weight="bold")
            )
            dialog_box.add(title_label)
            
            # Campi di input
            avversario_input = toga.TextInput(
                placeholder="Nome avversario",
                value=partita.get('avversario', ''),
                style=Pack(padding=5, width=300)
            )
            
            data_input = toga.TextInput(
                placeholder="Data (gg/mm/aaaa)",
                value=partita.get('data', ''),
                style=Pack(padding=5, width=300)
            )
            
            ora_input = toga.TextInput(
                placeholder="Ora (HH:MM)",
                value=partita.get('ora', ''),
                style=Pack(padding=5, width=300)
            )
            
            luogo_input = toga.TextInput(
                placeholder="Luogo partita",
                value=partita.get('luogo', ''),
                style=Pack(padding=5, width=300)
            )
            
            # Opzioni casa/trasferta (comportamento radio button)
            is_in_casa = partita.get('in_casa', True)
            
            casa_switch = toga.Switch(
                text="🏠 Partita in casa",
                value=is_in_casa,
                style=Pack(padding=5)
            )
            
            trasferta_switch = toga.Switch(
                text="✈️ Partita in trasferta",
                value=not is_in_casa,
                style=Pack(padding=5)
            )
            
            # Handler per comportamento radio button (uno esclude l'altro)
            def on_casa_change(widget):
                if casa_switch.value:
                    trasferta_switch.value = False
                else:
                    # Se si deseleziona casa, deve essere trasferta
                    if not trasferta_switch.value:
                        casa_switch.value = True
            
            def on_trasferta_change(widget):
                if trasferta_switch.value:
                    casa_switch.value = False
                else:
                    # Se si deseleziona trasferta, deve essere casa
                    if not casa_switch.value:
                        trasferta_switch.value = True
            
            casa_switch.on_change = on_casa_change
            trasferta_switch.on_change = on_trasferta_change
            
            # Selection tipologia
            tipologia_selection = toga.Selection(
                items=["pre-stagione", "stagione regolare", "post-stagione", "tornei"],
                value=partita.get('tipologia', 'stagione regolare'),
                style=Pack(padding=5, width=300)
            )
            
            # Campi risultato (opzionali)
            risultato_nostro_input = toga.NumberInput(
                value=partita.get('risultato_nostro', 0) if partita.get('risultato_nostro') is not None else 0,
                style=Pack(padding=5, width=150)
            )
            
            risultato_avversario_input = toga.NumberInput(
                value=partita.get('risultato_avversario', 0) if partita.get('risultato_avversario') is not None else 0,
                style=Pack(padding=5, width=150)
            )
            
            # Note
            note_input = toga.MultilineTextInput(
                placeholder="Note aggiuntive...",
                value=partita.get('note', ''),
                style=Pack(padding=5, width=300, height=80)
            )
            
            # Aggiungi i campi al dialog
            dialog_box.add(toga.Label("Avversario:", style=Pack(padding=(10, 5, 0, 5))))
            dialog_box.add(avversario_input)
            dialog_box.add(toga.Label("Data:", style=Pack(padding=(10, 5, 0, 5))))
            dialog_box.add(data_input)
            dialog_box.add(toga.Label("Ora:", style=Pack(padding=(10, 5, 0, 5))))
            dialog_box.add(ora_input)
            dialog_box.add(toga.Label("Luogo:", style=Pack(padding=(10, 5, 0, 5))))
            dialog_box.add(luogo_input)
            dialog_box.add(toga.Label("Tipo partita:", style=Pack(padding=(10, 5, 0, 5))))
            dialog_box.add(casa_switch)
            dialog_box.add(trasferta_switch)
            dialog_box.add(toga.Label("Tipologia:", style=Pack(padding=(10, 5, 0, 5))))
            dialog_box.add(tipologia_selection)
            
            # Box per risultati
            risultato_box = toga.Box(style=Pack(direction=ROW, padding=5))
            risultato_box.add(toga.Label("Risultato:", style=Pack(padding=5)))
            risultato_box.add(risultato_nostro_input)
            risultato_box.add(toga.Label("-", style=Pack(padding=5)))
            risultato_box.add(risultato_avversario_input)
            dialog_box.add(risultato_box)
            
            dialog_box.add(toga.Label("Note:", style=Pack(padding=(10, 5, 0, 5))))
            dialog_box.add(note_input)
            
            # Pulsanti
            buttons_box = toga.Box(style=Pack(direction=ROW, padding=20))
            
            def salva_modifiche(widget):
                # Converti i risultati da Decimal a int o None
                risultato_nostro = int(risultato_nostro_input.value) if risultato_nostro_input.value > 0 else None
                risultato_avversario = int(risultato_avversario_input.value) if risultato_avversario_input.value > 0 else None
                
                self.salva_partita_modificata(
                    partita['id'], 
                    avversario_input.value,
                    data_input.value,
                    ora_input.value,
                    luogo_input.value,
                    casa_switch.value,  # True se in casa
                    tipologia_selection.value,
                    risultato_nostro,
                    risultato_avversario,
                    note_input.value
                )
            
            def annulla_modifiche(widget):
                self.mostra_partite(None)
            
            salva_button = toga.Button(
                "💾 Salva",
                on_press=salva_modifiche,
                style=Pack(
                    padding=5,
                    background_color="#4caf50",
                    color="#ffffff",
                    width=100
                )
            )
            
            annulla_button = toga.Button(
                "❌ Annulla",
                on_press=annulla_modifiche,
                style=Pack(
                    padding=5,
                    background_color="#f44336",
                    color="#ffffff",
                    width=100
                )
            )
            
            buttons_box.add(salva_button)
            buttons_box.add(annulla_button)
            dialog_box.add(buttons_box)
            
            # Pulisce il contenuto e mostra il dialog
            self.dynamic_content.clear()
            self.dynamic_content.add(dialog_box)
            
        except Exception as e:
            print(f"✏️ DEBUG: ERRORE in modifica_partita: {str(e)}")
            import traceback
            traceback.print_exc()
            self.mostra_errore(f"Errore nell'apertura del dialog di modifica: {str(e)}")
    
    def salva_partita_modificata(self, partita_id, avversario, data, ora, luogo, in_casa, tipologia, risultato_nostro, risultato_avversario, note):
        """Salva le modifiche alla partita"""
        print(f"✏️ DEBUG: salva_partita_modificata chiamato")
        print(f"✏️ DEBUG: partita_id: {partita_id}")
        
        try:
            # Validazione input
            if not avversario or not data or not ora:
                self.mostra_errore("Avversario, data e ora sono obbligatori!")
                return
            
            # Crea oggetto partita aggiornato
            from .models import Partita
            partita_aggiornata = Partita(
                data=data,
                ora=ora,
                avversario=avversario,
                luogo=luogo or "",
                in_casa=in_casa,
                tipologia=tipologia
            )
            # Imposta risultati e altri attributi
            partita_aggiornata.risultato_nostro = risultato_nostro
            partita_aggiornata.risultato_avversario = risultato_avversario
            partita_aggiornata.note = note or ""
            partita_aggiornata.formazione = []  # Mantiene formazione esistente
            partita_aggiornata.statistiche = {}  # Mantiene statistiche esistenti
            
            # Aggiorna nel database
            success = self.partite_service.aggiorna_partita(partita_id, partita_aggiornata)
            
            if success:
                self.mostra_successo("Partita aggiornata con successo!")
                # Aggiorna la sidebar
                if hasattr(self, 'sidebar_giocatori_content'):
                    self.aggiorna_sidebar()
                # Torna alla vista partite
                self.mostra_partite(None)
            else:
                self.mostra_errore("Errore nell'aggiornamento della partita")
                
        except Exception as e:
            print(f"✏️ DEBUG: ERRORE in salva_partita_modificata: {str(e)}")
            import traceback
            traceback.print_exc()
            self.mostra_errore(f"Errore nel salvataggio: {str(e)}")
    
    def aggiungi_nuova_partita(self, widget):
        """Gestisce l'aggiunta di una nuova partita"""
        print(f"➕ DEBUG: aggiungi_nuova_partita chiamato")
        print(f"➕ DEBUG: tipologia_corrente: {getattr(self, 'tipologia_corrente', 'tutte')}")
        
        try:
            # Se siamo nella vista "tutte", chiedi prima la tipologia
            if getattr(self, 'tipologia_corrente', 'tutte') == 'tutte':
                self.mostra_selezione_tipologia_nuova_partita()
            else:
                # Usa la tipologia corrente
                self.mostra_form_nuova_partita(self.tipologia_corrente)
                
        except Exception as e:
            print(f"➕ DEBUG: ERRORE in aggiungi_nuova_partita: {str(e)}")
            import traceback
            traceback.print_exc()
            self.mostra_errore(f"Errore nell'aggiunta partita: {str(e)}")
    
    def mostra_selezione_tipologia_nuova_partita(self):
        """Mostra il dialog per selezionare la tipologia prima di aggiungere una partita"""
        print(f"➕ DEBUG: mostra_selezione_tipologia_nuova_partita chiamato")
        
        try:
            # Crea un dialog per la selezione tipologia
            dialog_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
            
            # Titolo
            title_label = toga.Label(
                "➕ Seleziona Tipologia Partita",
                style=Pack(padding=(0, 0, 20, 0), font_size=16, font_weight="bold")
            )
            dialog_box.add(title_label)
            
            # Descrizione
            desc_label = toga.Label(
                "Scegli il tipo di partita che vuoi aggiungere:",
                style=Pack(padding=(0, 0, 15, 0), font_size=12)
            )
            dialog_box.add(desc_label)
            
            # Bottoni per le tipologie
            tipologie_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
            
            tipologie = [
                ("🔥 Pre-stagione", "pre-stagione", "#ff9800"),
                ("🏆 Stagione Regolare", "stagione regolare", "#4caf50"),
                ("🥇 Post-stagione", "post-stagione", "#2196f3"),
                ("🏅 Tornei", "tornei", "#9c27b0")
            ]
            
            for nome, valore, colore in tipologie:
                def on_tipologia_press(widget, tip=valore):
                    self.mostra_form_nuova_partita(tip)
                
                button = toga.Button(
                    nome,
                    on_press=on_tipologia_press,
                    style=Pack(
                        padding=5,
                        height=self.config['button_height'],
                        background_color=colore,
                        color="#ffffff",
                        font_size=self.config['button_font_size'],
                        width=300
                    )
                )
                tipologie_box.add(button)
            
            dialog_box.add(tipologie_box)
            
            # Pulsante annulla
            def annulla_selezione(widget):
                self.mostra_partite(None)
            
            annulla_button = toga.Button(
                "❌ Annulla",
                on_press=annulla_selezione,
                style=Pack(
                    padding=20,
                    background_color="#f44336",
                    color="#ffffff",
                    width=200
                )
            )
            dialog_box.add(annulla_button)
            
            # Pulisce il contenuto e mostra il dialog
            self.dynamic_content.clear()
            self.dynamic_content.add(dialog_box)
            
        except Exception as e:
            print(f"➕ DEBUG: ERRORE in mostra_selezione_tipologia_nuova_partita: {str(e)}")
            import traceback
            traceback.print_exc()
            self.mostra_errore(f"Errore nella selezione tipologia: {str(e)}")
    
    def mostra_form_nuova_partita(self, tipologia):
        """Mostra il form per aggiungere una nuova partita con tipologia preimpostata"""
        print(f"➕ DEBUG: mostra_form_nuova_partita chiamato con tipologia: {tipologia}")
        
        try:
            # Crea un dialog per l'aggiunta
            dialog_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
            
            # Titolo con tipologia
            tipologia_nome = {
                "pre-stagione": "🔥 Pre-stagione",
                "stagione regolare": "🏆 Stagione Regolare", 
                "post-stagione": "🥇 Post-stagione",
                "tornei": "🏅 Tornei"
            }
            
            title_label = toga.Label(
                f"➕ Nuova Partita {tipologia_nome.get(tipologia, tipologia.title())}",
                style=Pack(padding=(0, 0, 20, 0), font_size=16, font_weight="bold")
            )
            dialog_box.add(title_label)
            
            # Campi di input
            avversario_input = toga.TextInput(
                placeholder="Nome avversario",
                style=Pack(padding=5, width=300)
            )
            
            data_input = toga.TextInput(
                placeholder="Data (gg/mm/aaaa)",
                style=Pack(padding=5, width=300)
            )
            
            ora_input = toga.TextInput(
                placeholder="Ora (HH:MM)",
                style=Pack(padding=5, width=300)
            )
            
            luogo_input = toga.TextInput(
                placeholder="Luogo partita",
                style=Pack(padding=5, width=300)
            )
            
            # Opzioni casa/trasferta (comportamento radio button)
            casa_switch = toga.Switch(
                text="🏠 Partita in casa",
                value=True,  # Default casa
                style=Pack(padding=5)
            )
            
            trasferta_switch = toga.Switch(
                text="✈️ Partita in trasferta",
                value=False,  # Default non trasferta
                style=Pack(padding=5)
            )
            
            # Handler per comportamento radio button (uno esclude l'altro)
            def on_casa_change_new(widget):
                if casa_switch.value:
                    trasferta_switch.value = False
                else:
                    # Se si deseleziona casa, deve essere trasferta
                    if not trasferta_switch.value:
                        casa_switch.value = True
            
            def on_trasferta_change_new(widget):
                if trasferta_switch.value:
                    casa_switch.value = False
                else:
                    # Se si deseleziona trasferta, deve essere casa
                    if not casa_switch.value:
                        trasferta_switch.value = True
            
            casa_switch.on_change = on_casa_change_new
            trasferta_switch.on_change = on_trasferta_change_new
            
            # Note
            note_input = toga.MultilineTextInput(
                placeholder="Note aggiuntive...",
                style=Pack(padding=5, width=300, height=80)
            )
            
            # Aggiungi i campi al dialog
            dialog_box.add(toga.Label("Avversario:", style=Pack(padding=(10, 5, 0, 5))))
            dialog_box.add(avversario_input)
            dialog_box.add(toga.Label("Data:", style=Pack(padding=(10, 5, 0, 5))))
            dialog_box.add(data_input)
            dialog_box.add(toga.Label("Ora:", style=Pack(padding=(10, 5, 0, 5))))
            dialog_box.add(ora_input)
            dialog_box.add(toga.Label("Luogo:", style=Pack(padding=(10, 5, 0, 5))))
            dialog_box.add(luogo_input)
            dialog_box.add(toga.Label("Tipo partita:", style=Pack(padding=(10, 5, 0, 5))))
            dialog_box.add(casa_switch)
            dialog_box.add(trasferta_switch)
            dialog_box.add(toga.Label("Note:", style=Pack(padding=(10, 5, 0, 5))))
            dialog_box.add(note_input)
            
            # Pulsanti
            buttons_box = toga.Box(style=Pack(direction=ROW, padding=20))
            
            def salva_nuova_partita(widget):
                self.salva_partita_creata(
                    avversario_input.value,
                    data_input.value,
                    ora_input.value,
                    luogo_input.value,
                    casa_switch.value,  # True se in casa
                    tipologia,
                    note_input.value
                )
            
            def annulla_creazione(widget):
                self.mostra_partite(None)
            
            salva_button = toga.Button(
                "💾 Crea Partita",
                on_press=salva_nuova_partita,
                style=Pack(
                    padding=5,
                    background_color="#4caf50",
                    color="#ffffff",
                    width=120
                )
            )
            
            annulla_button = toga.Button(
                "❌ Annulla",
                on_press=annulla_creazione,
                style=Pack(
                    padding=5,
                    background_color="#f44336",
                    color="#ffffff",
                    width=100
                )
            )
            
            buttons_box.add(salva_button)
            buttons_box.add(annulla_button)
            dialog_box.add(buttons_box)
            
            # Pulisce il contenuto e mostra il dialog
            self.dynamic_content.clear()
            self.dynamic_content.add(dialog_box)
            
        except Exception as e:
            print(f"➕ DEBUG: ERRORE in mostra_form_nuova_partita: {str(e)}")
            import traceback
            traceback.print_exc()
            self.mostra_errore(f"Errore nel form nuova partita: {str(e)}")
    
    def salva_partita_creata(self, avversario, data, ora, luogo, in_casa, tipologia, note):
        """Salva la nuova partita creata"""
        print(f"➕ DEBUG: salva_partita_creata chiamato")
        print(f"➕ DEBUG: tipologia: {tipologia}")
        
        try:
            # Validazione input
            if not avversario or not data or not ora:
                self.mostra_errore("Avversario, data e ora sono obbligatori!")
                return
            
            # Crea oggetto partita
            from .models import Partita
            nuova_partita = Partita(
                data=data,
                ora=ora,
                avversario=avversario,
                luogo=luogo or "",
                in_casa=in_casa,
                tipologia=tipologia
            )
            # Imposta attributi aggiuntivi
            nuova_partita.risultato_nostro = None
            nuova_partita.risultato_avversario = None
            nuova_partita.note = note or ""
            nuova_partita.formazione = []
            nuova_partita.statistiche = {}
            
            # Salva nel database
            success = self.partite_service.aggiungi_partita(nuova_partita)
            
            if success:
                self.mostra_successo("Nuova partita creata con successo!")
                # Aggiorna la sidebar
                if hasattr(self, 'sidebar_giocatori_content'):
                    self.aggiorna_sidebar()
                # Torna alla vista partite
                self.mostra_partite(None)
                # Filtra per la tipologia appena aggiunta se non era "tutte"
                if tipologia != "tutte":
                    self.filtra_partite(tipologia)
            else:
                self.mostra_errore("Errore nella creazione della partita")
                
        except Exception as e:
            print(f"➕ DEBUG: ERRORE in salva_partita_creata: {str(e)}")
            import traceback
            traceback.print_exc()
            self.mostra_errore(f"Errore nel salvataggio: {str(e)}")
    
    def gestisci_statistiche_partita(self, partita):
        """Gestisce l'inserimento delle statistiche individuali per una partita"""
        print(f"📊 DEBUG: gestisci_statistiche_partita chiamato per partita: {partita}")
        
        try:
            # Ottieni i convocati per questa partita
            convocati = self.statistiche_individuali_service.ottieni_convocati_partita(partita['id'])
            print(f"📊 DEBUG: Trovati {len(convocati)} convocati")
            
            if not convocati:
                self.mostra_errore("Nessun giocatore convocato per questa partita. Aggiungi prima i convocati.")
                return
            
            # Ottieni statistiche esistenti
            statistiche_esistenti = self.statistiche_individuali_service.ottieni_statistiche_partita(partita['id'])
            stats_dict = {s['giocatore_id']: s for s in statistiche_esistenti}
            
            # Crea l'interfaccia per inserire le statistiche
            dialog_box = toga.Box(style=Pack(direction=COLUMN, padding=15))
            
            # Titolo
            title_label = toga.Label(
                f"📊 Statistiche Individuali: {partita['avversario']}",
                style=Pack(padding=(0, 0, 15, 0), font_size=16, font_weight="bold")
            )
            dialog_box.add(title_label)
            
            # Info partita
            info_label = toga.Label(
                f"📅 {partita['data']} {partita['ora']} - {partita.get('tipologia', 'stagione regolare').title()}",
                style=Pack(padding=(0, 0, 10, 0), color="#666666")
            )
            dialog_box.add(info_label)
            
            # Header colonne statistiche
            header_box = toga.Box(style=Pack(direction=ROW, padding=5, background_color="#f0f0f0"))
            
            headers = ["Giocatore", "Pt", "PP", "PR", "STP", "RMB", "AS", "VAL", "+/-"]
            header_widths = [120, 35, 35, 35, 35, 35, 35, 35, 35]  # Allineate ai campi input
            
            for i, (header, width) in enumerate(zip(headers, header_widths)):
                # Primo elemento (Giocatore) ha padding diverso per allineamento
                padding_style = (0, 5, 0, 0) if i == 0 else (0, 0, 0, 0)
                
                header_label = toga.Label(
                    header,
                    style=Pack(
                        width=width, 
                        font_size=10, 
                        font_weight="bold", 
                        text_align=CENTER,
                        padding=padding_style
                    )
                )
                header_box.add(header_label)
            
            dialog_box.add(header_box)
            
            # Area scrollabile per i giocatori
            giocatori_stats_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
            
            # Dizionario per salvare i campi di input
            self.stats_inputs = {}
            
            for convocato in convocati:
                giocatore_id = convocato['id']
                stats_esistenti = stats_dict.get(giocatore_id, {})
                
                # Box per ogni giocatore
                player_row = toga.Box(style=Pack(direction=ROW, padding=3))
                
                # Nome giocatore
                numero = f"#{convocato['numero_maglia']}" if convocato['numero_maglia'] else "#--"
                nome_display = f"{numero} {convocato['nome'][:8]}.{convocato['cognome'][:8]}."
                
                name_label = toga.Label(
                    nome_display,
                    style=Pack(width=120, font_size=10, padding=(0, 5, 0, 0))
                )
                player_row.add(name_label)
                
                # Campi input per statistiche
                player_inputs = {}
                stats_fields = ['punti', 'palle_perse', 'palle_recuperate', 'stoppate', 'rimbalzi', 'assist', 'valutazione', 'plus_minus']
                
                for field in stats_fields:
                    # Valore iniziale per il campo
                    initial_value = stats_esistenti.get(field, 0)
                    display_value = str(initial_value) if initial_value != 0 else ""
                    
                    input_field = toga.TextInput(
                        value=display_value,
                        style=Pack(width=35, font_size=10, text_align=CENTER),
                        placeholder="0" if field != 'plus_minus' else "+/-"
                    )
                    player_inputs[field] = input_field
                    player_row.add(input_field)
                
                self.stats_inputs[giocatore_id] = player_inputs
                giocatori_stats_box.add(player_row)
            
            # ScrollContainer per lista giocatori
            stats_scroll = toga.ScrollContainer(
                content=giocatori_stats_box,
                style=Pack(height=300)
            )
            dialog_box.add(stats_scroll)
            
            # Pulsanti
            buttons_box = toga.Box(style=Pack(direction=ROW, padding=10))
            
            salva_button = toga.Button(
                "💾 Salva Statistiche",
                on_press=lambda w: self.salva_statistiche_partita(partita['id']),
                style=Pack(flex=1, padding=5, background_color="#4caf50", color="#ffffff")
            )
            
            annulla_button = toga.Button(
                "❌ Annulla",
                on_press=lambda w: self.chiudi_dialog_statistiche(),
                style=Pack(flex=1, padding=5, background_color="#f44336", color="#ffffff")
            )
            
            buttons_box.add(salva_button)
            buttons_box.add(annulla_button)
            dialog_box.add(buttons_box)
            
            # Mostra il dialog
            print(f"📊 DEBUG: Mostrando dialog statistiche")
            self.dynamic_content.clear()
            self.dynamic_content.add(dialog_box)
            print(f"📊 DEBUG: Dialog statistiche mostrato con successo!")
            
        except Exception as e:
            print(f"📊 DEBUG: ERRORE in gestisci_statistiche_partita: {str(e)}")
            import traceback
            traceback.print_exc()
            self.mostra_errore(f"Errore nella gestione statistiche: {str(e)}")
    
    def salva_statistiche_partita(self, partita_id):
        """Salva le statistiche individuali per la partita"""
        print(f"📊 DEBUG: salva_statistiche_partita chiamato per partita {partita_id}")
        
        try:
            success_count = 0
            
            for giocatore_id, inputs in self.stats_inputs.items():
                # Raccogli i valori dai campi input
                stats = {}
                for field, input_field in inputs.items():
                    try:
                        # Gestisce valori negativi per il campo plus_minus (+/-)
                        raw_value = input_field.value.strip()
                        if raw_value == "" or raw_value == "-":
                            value = 0
                        else:
                            value = int(raw_value)
                        stats[field] = value
                        print(f"📊 DEBUG: Campo {field} = {value} (input: '{raw_value}')")
                    except ValueError as e:
                        print(f"📊 DEBUG: Errore conversione campo {field}: {input_field.value} -> {str(e)}")
                        stats[field] = 0
                
                # Salva le statistiche per questo giocatore
                if self.statistiche_individuali_service.salva_statistica_giocatore(partita_id, giocatore_id, stats):
                    success_count += 1
                    print(f"📊 DEBUG: Statistiche salvate per giocatore {giocatore_id}")
                else:
                    print(f"📊 DEBUG: Errore nel salvare statistiche per giocatore {giocatore_id}")
            
            if success_count > 0:
                self.mostra_successo(f"Statistiche salvate per {success_count} giocatori!")
                self.chiudi_dialog_statistiche()
            else:
                self.mostra_errore("Nessuna statistica è stata salvata")
                
        except Exception as e:
            print(f"📊 DEBUG: ERRORE in salva_statistiche_partita: {str(e)}")
            import traceback
            traceback.print_exc()
            self.mostra_errore(f"Errore nel salvataggio statistiche: {str(e)}")
    
    def chiudi_dialog_statistiche(self):
        """Chiude il dialog statistiche e torna alla vista partite"""
        self.mostra_partite(None)


def main():
    """Funzione principale dell'applicazione"""
    return JBKGestione()


if __name__ == "__main__":
    app = main()
    app.main_loop()