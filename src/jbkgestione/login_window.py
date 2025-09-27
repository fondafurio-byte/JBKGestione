"""
Schermata di Login per JBK Gestione
Interface di autenticazione con Supabase
"""

import toga
from toga.style.pack import COLUMN, ROW, Pack
from toga.constants import CENTER, LEFT
from jbkgestione.supabase_auth import auth_service

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
        # Usa il config dell'app per i colori
        self.config = app.config if hasattr(app, 'config') else {}
        
    def create_login_window(self):
        """Crea la finestra di login"""
        
        # Colori dal config o fallback
        text_color = self.config.get('text_color', '#2c3e50')
        secondary_text_color = self.config.get('text_color', '#34495e')
        
        # Container principale con centraggio completo
        main_container = toga.Box(style=Pack(
            direction=COLUMN,
            align_items=CENTER,
            padding=50,
            flex=1  # Occupa tutto lo spazio disponibile per centrare meglio
        ))
        
        # Logo/Titolo dell'app
        title_label = toga.Label(
            "🏀 JBK GESTIONE",
            style=Pack(
                font_size=28,
                font_weight="bold",
                color=text_color,  # Usa colore dal config
                margin_bottom=10,
                text_align=CENTER
            )
        )
        main_container.add(title_label)
        
        # Sottotitolo
        subtitle_label = toga.Label(
            "Sistema di Gestione Squadra Basket",
            style=Pack(
                font_size=14,
                color=secondary_text_color,  # Usa colore dal config
                margin_bottom=30,
                text_align=CENTER
            )
        )
        main_container.add(subtitle_label)
        
        # Container per il form di login centrato
        login_container = toga.Box(style=Pack(
            direction=COLUMN,
            padding=30,
            align_items=CENTER,
            width=400,  # Larghezza fissa per centrare meglio
        ))
        
        # Titolo form login
        login_title = toga.Label(
            "Accedi al Sistema",
            style=Pack(
                font_size=18,
                font_weight="bold",
                color=text_color,  # Usa colore dal config
                margin_bottom=20,
                text_align=CENTER
            )
        )
        login_container.add(login_title)
        
        # Campo Username
        username_label = toga.Label(
            "Nome Utente:",
            style=Pack(
                font_size=12,
                color=secondary_text_color,  # Usa colore dal config
                margin_bottom=5,
                text_align=CENTER  # Centrare le etichette
            )
        )
        login_container.add(username_label)
        
        self.username_input = toga.TextInput(
            placeholder="Inserisci il tuo nome utente",
            style=Pack(
                width=300,
                margin_bottom=15,
                font_size=14,
                text_align=CENTER  # Centrare il testo di input
            )
        )
        login_container.add(self.username_input)
        
        # Campo Password
        password_label = toga.Label(
            "Password:",
            style=Pack(
                font_size=12,
                color=secondary_text_color,  # Usa colore dal config
                margin_bottom=5,
                text_align=CENTER  # Centrare le etichette
            )
        )
        login_container.add(password_label)
        
        self.password_input = toga.PasswordInput(
            placeholder="Inserisci la tua password",
            style=Pack(
                width=300,
                margin_bottom=20,
                font_size=14,
                text_align=CENTER  # Centrare il testo di input
            )
        )
        login_container.add(self.password_input)
        
        # Container per i pulsanti
        button_container = toga.Box(style=Pack(
            direction=ROW,
            margin_bottom=20
        ))
        
        # Pulsante Login
        self.login_button = toga.Button(
            "🔐 ACCEDI",
            on_press=self.handle_login,
            style=Pack(
                width=140,
                padding=10,
                background_color="#d32f2f",
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
        
        # Label per messaggi di stato
        self.status_label = toga.Label(
            "",
            style=Pack(
                font_size=12,
                margin_top=10,
                text_align=CENTER,
                color=text_color  # Usa colore dal config
            )
        )
        login_container.add(self.status_label)
        
        # Label per ruolo utente
        self.user_role_label = toga.Label(
            "",
            style=Pack(
                font_size=11,
                margin_top=5,
                text_align=CENTER,
                color=secondary_text_color,  # Usa colore dal config
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
        """Gestisce la selezione del tipo di registrazione (Coach/Atleta)"""
        import toga
        from toga.style.pack import COLUMN, ROW, Pack
        from toga.constants import CENTER

        def on_select_coach(btn):
            select_role_dialog.close()
            register_window = RegisterWindow(self.app, self.main_window)
            register_window.show_register_coach_dialog()

        def on_select_atleta(btn):
            select_role_dialog.close()
            register_window = RegisterWindow(self.app, self.main_window)
            register_window.show_register_atleta_dialog()

        box = toga.Box(style=Pack(direction=COLUMN, padding=20, align_items=CENTER, width=300))
        label = toga.Label("Registrati come:", style=Pack(font_size=16, margin_bottom=20, text_align=CENTER))
        btn_coach = toga.Button("Coach", on_press=on_select_coach, style=Pack(width=200, padding=10, margin_bottom=10))
        btn_atleta = toga.Button("Atleta", on_press=on_select_atleta, style=Pack(width=200, padding=10))
        box.add(label)
        box.add(btn_coach)
        box.add(btn_atleta)
        select_role_dialog = toga.Window(title="Seleziona ruolo", size=(320, 200))
        select_role_dialog.content = box
        select_role_dialog.show()
    
    def show_status(self, message: str, color: str = "#2c3e50"):
        """Mostra un messaggio di stato"""
        self.status_label.text = message
        # Usa colori scuri per leggibilità su sfondo chiaro
        self.status_label.style.color = color
    
    async def delayed_app_start(self, widget):
        """Avvia l'app principale dopo un breve delay"""
        print("⏰ Inizio delay prima dell'avvio...")
        import asyncio
        await asyncio.sleep(1.5)  # Aspetta 1.5 secondi

        print("🚀 Chiamata start_main_app...")
        try:
            # Invece di chiudere la finestra, cambia il contenuto per passare all'app principale
            # Questo mantiene la stessa finestra invece di crearne una nuova
            self.app.start_main_app()
            print("✅ start_main_app completato")
        except Exception as e:
            print(f"❌ Errore in start_main_app: {e}")
            self.show_status(f"❌ Errore avvio app: {str(e)}")
            self.login_button.enabled = True

class RegisterWindow:
    def show_register_coach_dialog(self):
        """Form di registrazione per Coach"""
        import toga
        from toga.style.pack import COLUMN, ROW, Pack
        from toga.constants import CENTER
        text_color = self.app.config.get('text_color', '#2c3e50')
        secondary_text_color = self.app.config.get('text_color', '#34495e')
        dialog_container = toga.Box(style=Pack(direction=COLUMN, padding=0, align_items=CENTER, width=500, height=600))
        title_label = toga.Label("👤 REGISTRAZIONE COACH", style=Pack(font_size=20, font_weight="bold", color=text_color, margin_bottom=10, text_align=CENTER))
        dialog_container.add(title_label)
        subtitle_label = toga.Label("Crea un nuovo account Coach", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=25, text_align=CENTER))
        dialog_container.add(subtitle_label)
        scrollable_form = toga.ScrollContainer(horizontal=False, style=Pack(width=480, height=400, padding=0, margin_bottom=0, background_color="transparent"))
        form_container = toga.Box(style=Pack(direction=COLUMN, padding=20, align_items=CENTER, width=460))
        # Username
        username_label = toga.Label("Nome utente:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(username_label)
        self.username_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.username_input)
        # Email
        email_label = toga.Label("Email:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(email_label)
        self.email_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.email_input)
        # Nome
        first_name_label = toga.Label("Nome:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(first_name_label)
        self.first_name_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.first_name_input)
        # Cognome
        last_name_label = toga.Label("Cognome:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(last_name_label)
        self.last_name_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.last_name_input)
        # Password
        password_label = toga.Label("Password:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(password_label)
        self.password_input = toga.PasswordInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.password_input)
        # Conferma Password
        confirm_password_label = toga.Label("Conferma Password:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(confirm_password_label)
        self.confirm_password_input = toga.PasswordInput(style=Pack(width=350, margin_bottom=15, font_size=14, text_align=CENTER))
        form_container.add(self.confirm_password_input)
        # Categorie (multi)
        categorie = ["U13", "U14", "U15", "U17", "U19", "Promozione", "Minibasket"]
        category_label = toga.Label("Categorie:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(category_label)
        self.category_checkboxes = []
        category_box = toga.Box(style=Pack(direction=COLUMN, margin_bottom=10, align_items="start"))
        def on_category_switch_changed(widget):
            # Conta quante sono selezionate
            selected = [cb for cb in self.category_checkboxes if cb.value]
            if len(selected) > 3:
                # Trova la più vecchia selezionata (la prima nell'ordine)
                for cb in self.category_checkboxes:
                    if cb.value:
                        cb.value = False
                        break
        for cat in categorie:
            cb = toga.Switch(cat, value=False, style=Pack(align_items="start", margin_bottom=2))
            cb.on_change = on_category_switch_changed
            category_box.add(cb)
            self.category_checkboxes.append(cb)
        form_container.add(category_box)
        # Status label
        self.status_label = toga.Label("", style=Pack(font_size=12, margin_top=10, text_align=CENTER, color=text_color))
        form_container.add(self.status_label)
        scrollable_form.content = form_container
        dialog_container.add(scrollable_form)
        btn_registra = toga.Button("Registrati", on_press=self.handle_user_registration, style=Pack(width=200, padding=10, background_color="#27ae60", color="#fff", font_size=13, font_weight="bold", margin_top=15, margin_bottom=20))
        dialog_container.add(btn_registra)
        self.register_dialog = toga.Window(title="Registrazione Coach", size=(500, 600))
        self.register_dialog.content = dialog_container
        self.register_dialog.show()

    def show_register_atleta_dialog(self):
        """Form di registrazione per Atleta"""
        import toga
        from toga.style.pack import COLUMN, ROW, Pack
        from toga.constants import CENTER
        text_color = self.app.config.get('text_color', '#2c3e50')
        secondary_text_color = self.app.config.get('text_color', '#34495e')
        dialog_container = toga.Box(style=Pack(direction=COLUMN, padding=0, align_items=CENTER, width=500, height=700))
        title_label = toga.Label("👤 REGISTRAZIONE ATLETA", style=Pack(font_size=20, font_weight="bold", color=text_color, margin_bottom=10, text_align=CENTER))
        dialog_container.add(title_label)
        subtitle_label = toga.Label("Crea un nuovo account Atleta", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=25, text_align=CENTER))
        dialog_container.add(subtitle_label)
        scrollable_form = toga.ScrollContainer(horizontal=False, style=Pack(width=480, height=540, padding=0, margin_bottom=0, background_color="transparent"))
        form_container = toga.Box(style=Pack(direction=COLUMN, padding=20, align_items=CENTER, width=460))
        # Username
        username_label = toga.Label("Nome utente:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(username_label)
        self.username_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.username_input)
        # Email
        email_label = toga.Label("Email:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(email_label)
        self.email_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.email_input)
        # Nome
        first_name_label = toga.Label("Nome:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(first_name_label)
        self.first_name_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.first_name_input)
        # Cognome
        last_name_label = toga.Label("Cognome:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(last_name_label)
        self.last_name_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.last_name_input)
        # Data di nascita
        dob_label = toga.Label("Data di nascita (YYYY-MM-DD):", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(dob_label)
        self.dob_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.dob_input)
        # Numero maglia
        num_label = toga.Label("Numero maglia:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(num_label)
        self.num_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.num_input)
        # Password
        password_label = toga.Label("Password:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(password_label)
        self.password_input = toga.PasswordInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.password_input)
        # Conferma Password
        confirm_password_label = toga.Label("Conferma Password:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(confirm_password_label)
        self.confirm_password_input = toga.PasswordInput(style=Pack(width=350, margin_bottom=15, font_size=14, text_align=CENTER))
        form_container.add(self.confirm_password_input)
        # Categoria (singola)
        categorie = ["U13", "U14", "U15", "U17", "U19", "Promozione", "Minibasket"]
        category_label = toga.Label("Categoria:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(category_label)
        self.category_select = toga.Selection(items=categorie, style=Pack(width=200, font_size=14, text_align=CENTER, margin_bottom=10))
        form_container.add(self.category_select)
        # Status label
        self.status_label = toga.Label("", style=Pack(font_size=12, margin_top=10, text_align=CENTER, color=text_color))
        form_container.add(self.status_label)
        scrollable_form.content = form_container
        dialog_container.add(scrollable_form)
        btn_registra = toga.Button("Registrati", on_press=self.handle_user_registration, style=Pack(width=200, padding=10, background_color="#27ae60", color="#fff", font_size=13, font_weight="bold", margin_top=15, margin_bottom=20))
        dialog_container.add(btn_registra)
        self.register_dialog = toga.Window(title="Registrazione Atleta", size=(500, 700))
        self.register_dialog.content = dialog_container
        self.register_dialog.show()
    """Finestra di registrazione per utenti non admin"""
    def __init__(self, app, parent_window):
        self.app = app
        self.parent_window = parent_window
        self.register_dialog = None
        self.username_input = None
        self.email_input = None
        self.first_name_input = None
        self.last_name_input = None
        self.password_input = None
        self.confirm_password_input = None
        self.role_select = None
        self.category_select = None
        self.status_label = None
        # Campi extra atleta
        self.dob_label = None
        self.dob_input = None
        self.num_label = None
        self.num_input = None

    def show_register_dialog(self):
        """Mostra il dialog di registrazione come finestra modale, adattivo e scrollabile"""
        import toga
        text_color = self.app.config.get('text_color', '#2c3e50')
        secondary_text_color = self.app.config.get('text_color', '#34495e')
        dialog_container = toga.Box(style=Pack(direction=COLUMN, padding=0, align_items=CENTER, width=500, height=700))
        title_label = toga.Label("👤 REGISTRAZIONE UTENTE", style=Pack(font_size=20, font_weight="bold", color=text_color, margin_bottom=10, text_align=CENTER))
        dialog_container.add(title_label)
        subtitle_label = toga.Label("Crea un nuovo account utente", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=25, text_align=CENTER))
        dialog_container.add(subtitle_label)

        # Contenitore scrollabile per il form
        scrollable_form = toga.ScrollContainer(horizontal=False, style=Pack(width=480, height=540, padding=0, margin_bottom=0))
        form_container = toga.Box(style=Pack(direction=COLUMN, padding=20, align_items=CENTER, width=460))

        # Username
        username_label = toga.Label("Nome utente:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(username_label)
        self.username_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.username_input)

        # Email
        email_label = toga.Label("Email:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(email_label)
        self.email_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.email_input)

        # --- Campi extra atleta (creati come attributi della classe) ---
        self.dob_label = toga.Label("Data di nascita (YYYY-MM-DD):", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        self.dob_input = toga.TextInput(style=Pack(margin_bottom=10, font_size=14, text_align=CENTER, flex=1))
        self.num_label = toga.Label("Numero maglia:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        self.num_input = toga.TextInput(style=Pack(margin_bottom=10, font_size=14, text_align=CENTER, flex=1))

        # Box verticale per i campi atleta (inserito dinamicamente)
        self.atleta_fields_box = toga.Box(style=Pack(direction=COLUMN, align_items=CENTER, margin_bottom=10, flex=1))

        # Nome
        first_name_label = toga.Label("Nome:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(first_name_label)
        self.first_name_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.first_name_input)

        # Cognome
        last_name_label = toga.Label("Cognome:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(last_name_label)
        self.last_name_input = toga.TextInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.last_name_input)

        # Password
        password_label = toga.Label("Password:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(password_label)
        self.password_input = toga.PasswordInput(style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        form_container.add(self.password_input)

        # Conferma Password
        confirm_password_label = toga.Label("Conferma Password:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(confirm_password_label)
        self.confirm_password_input = toga.PasswordInput(style=Pack(width=350, margin_bottom=15, font_size=14, text_align=CENTER))
        form_container.add(self.confirm_password_input)


        # Ruolo con Selection (dropdown)
        role_label = toga.Label("Ruolo:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        form_container.add(role_label)
        self.role_select = toga.Selection(items=["Seleziona ruolo...", "Coach", "Atleta"], style=Pack(width=350, margin_bottom=10, font_size=14, text_align=CENTER))
        def on_role_select(widget):
            # debug rimossa
            ruolo = self.role_select.value
            form_container = self.role_select.parent
            # debug rimossa
            # debug rimossa
            if hasattr(self, 'status_label') and self.status_label:
                pass
            # Confronto esplicito con i valori esatti
            if ruolo == "Coach" or ruolo == "Atleta":
                # debug rimossa
                pass
                self.update_category_selector(ruolo)
            else:
                # debug rimossa
                pass
                if self.atleta_fields_box in form_container.children:
                    # debug rimossa
                    form_container.remove(self.atleta_fields_box)
                self.category_box.children.clear()
                self.extra_atleta_box.children.clear()
            # debug rimossa
            # refresh rimosso per evitare crash Toga
        self.role_select.on_select = on_role_select
        # Prova anche on_change se disponibile (alcune versioni di Toga lo usano per i dropdown)
        if hasattr(self.role_select, 'on_change'):
            self.role_select.on_change = on_role_select
        form_container.add(self.role_select)
        form_container.add(self.role_select)

        # Box verticale per i campi atleta (inserito dinamicamente tra role_select e categorie)
        self.atleta_fields_box = toga.Box(style=Pack(direction=COLUMN, align_items=CENTER, margin_bottom=10))


        # Categorie + campi atleta in un box orizzontale (devono essere creati PRIMA di qualsiasi chiamata a update_category_selector)
        self.categorie = ["U13", "U14", "U15", "U17", "U19", "Promozione", "Minibasket"]
        self.category_checkboxes = []
        self.category_select = None
        self.category_box = toga.Box(style=Pack(direction=COLUMN, margin_bottom=0, align_items="start", padding_left=0, padding_right=0))
        self.extra_atleta_box = toga.Box(style=Pack(direction=ROW, align_items=CENTER, margin_left=10))
        self.category_row = toga.Box(style=Pack(direction=ROW, align_items=CENTER, margin_bottom=15))
        self.category_label = toga.Label("Categoria:", style=Pack(font_size=12, color=secondary_text_color, margin_bottom=5, text_align=CENTER))
        self.category_row.add(self.category_box)
        self.category_row.add(self.extra_atleta_box)
        # La label rimane sopra
        form_container.add(self.category_label)
        form_container.add(self.category_row)
        # atleta_fields_box sarà aggiunto dinamicamente in fondo se necessario

    # Chiamata iniziale: nessun ruolo selezionato, i campi compariranno solo dopo la scelta

        # Status label
        self.status_label = toga.Label("", style=Pack(font_size=12, margin_top=10, text_align=CENTER, color=text_color))
        form_container.add(self.status_label)

        scrollable_form.content = form_container
        dialog_container.add(scrollable_form)

        # Pulsante REGISTRA in fondo al dialog, fuori dallo scroll
        btn_registra = toga.Button("Registrati", on_press=self.handle_user_registration, style=Pack(width=200, padding=10, background_color="#27ae60", color="#fff", font_size=13, font_weight="bold", margin_top=15, margin_bottom=20))
        dialog_container.add(btn_registra)

        self.register_dialog = toga.Window(title="Registrazione", size=(500, 700))
        self.register_dialog.content = dialog_container
        
        # Forza la sincronizzazione dei campi ogni volta che il dialog viene mostrato
        if self.role_select.value:
        # debug rimossa
            self.update_category_selector(self.role_select.value)
        self.register_dialog.show()

    def update_category_selector(self, ruolo):
    # debug rimossa
        # Trova il contenitore principale (form_container)
        form_container = None
        if hasattr(self.role_select, 'parent') and self.role_select.parent:
            form_container = self.role_select.parent
        # Rimuovi atleta_fields_box se già presente
        parent = self.atleta_fields_box._impl.container if hasattr(self.atleta_fields_box, '_impl') and hasattr(self.atleta_fields_box._impl, 'container') else None
        if form_container and self.atleta_fields_box in form_container.children:
            form_container.remove(self.atleta_fields_box)
        elif parent:
            try:
                parent.remove(self.atleta_fields_box)
            except Exception:
                pass
    # debug rimossa
        pass
        ruolo_norm = str(ruolo).strip().lower()
        # Svuota il box categorie e il box extra atleta
        self.category_box.children.clear()
        self.extra_atleta_box.children.clear()
        self.category_checkboxes = []
        if ruolo_norm == "coach":
            # debug rimossa
            pass
            # Ricrea i box
            self.category_box = toga.Box(style=Pack(direction=COLUMN, margin_bottom=0, align_items="start", padding_left=0, padding_right=0))
            self.extra_atleta_box = toga.Box(style=Pack(direction=ROW, align_items=CENTER, margin_left=10))
            self.category_row = toga.Box(style=Pack(direction=ROW, align_items=CENTER, margin_bottom=15))
            self.category_row.add(self.category_box)
            self.category_row.add(self.extra_atleta_box)
            self.category_checkboxes = []
            for cat in self.categorie:
                cb = toga.Switch(cat, value=False, style=Pack(align_items="start", margin_bottom=2, padding_left=0))
                self.category_box.add(cb)
                # debug rimossa
                pass
                self.category_checkboxes.append(cb)
            self.category_select = None
            # debug rimossa
            pass
            # Rimuovi la vecchia category_row (se esiste) e inserisci la nuova nella stessa posizione
            if form_container:
                idx = None
                for i, child in enumerate(list(form_container.children)):
                    if child is not self.category_row and isinstance(child, toga.Box) and getattr(child, 'style', None) and getattr(child.style, 'margin_bottom', None) == 15:
                        idx = i
                        form_container.remove(child)
                        break
                if idx is not None:
                    form_container.children.insert(idx, self.category_row)
                    # debug rimossa
                else:
                    form_container.add(self.category_row)
                    # debug rimossa
            # refresh rimossi per evitare crash Toga
        elif ruolo_norm == "atleta":
            # debug rimossa
            pass
            # Ricrea i box
            self.category_box = toga.Box(style=Pack(direction=COLUMN, margin_bottom=0, align_items="start", padding_left=0, padding_right=0))
            self.extra_atleta_box = toga.Box(style=Pack(direction=ROW, align_items=CENTER, margin_left=10))
            self.category_row = toga.Box(style=Pack(direction=ROW, align_items=CENTER, margin_bottom=15))
            self.category_row.add(self.category_box)
            self.category_row.add(self.extra_atleta_box)
            self.category_select = toga.Selection(items=self.categorie, style=Pack(width=150, font_size=14, text_align=CENTER, margin_right=10))
            self.category_box.add(self.category_select)
            # debug rimossa
            pass
            self.category_checkboxes = []
            # Prepara i campi atleta
            self.atleta_fields_box.children.clear()
            self.atleta_fields_box.add(self.dob_label)
            # debug rimossa
            self.atleta_fields_box.add(self.dob_input)
            # debug rimossa
            self.atleta_fields_box.add(self.num_label)
            # debug rimossa
            self.atleta_fields_box.add(self.num_input)
            # debug rimossa
            pass
            # Rimuovi la vecchia category_row (se esiste) e inserisci la nuova nella stessa posizione
            if form_container:
                idx = None
                for i, child in enumerate(list(form_container.children)):
                    if child is not self.category_row and isinstance(child, toga.Box) and getattr(child, 'style', None) and getattr(child.style, 'margin_bottom', None) == 15:
                        idx = i
                        form_container.remove(child)
                        break
                if idx is not None:
                    form_container.children.insert(idx, self.category_row)
                    # debug rimossa
                else:
                    form_container.add(self.category_row)
                    # debug rimossa
                # Rimuovi atleta_fields_box ovunque sia e reinseriscilo in fondo
                if self.atleta_fields_box in form_container.children:
                    form_container.remove(self.atleta_fields_box)
                # Aggiungi solo se atleta_fields_box ha ancora un _impl valido e _impl.container non è None
                if hasattr(self.atleta_fields_box, '_impl') and getattr(self.atleta_fields_box._impl, 'container', None) is not None:
                    form_container.add(self.atleta_fields_box)
                # debug rimossa
                pass
                if hasattr(form_container, 'refresh'): form_container.refresh()
            # refresh rimossi per evitare crash Toga
    # debug rimossa
        # Forza il refresh del layout (workaround per bug Toga)
    # PATCH: disabilitato refresh per debug crash Toga
    # if form_container and hasattr(form_container, 'refresh') and hasattr(form_container, '_impl') and getattr(form_container._impl, 'container', None) is not None:
    #     form_container.refresh()
        if hasattr(self.category_box, 'refresh'): self.category_box.refresh()
        if hasattr(self.extra_atleta_box, 'refresh'): self.extra_atleta_box.refresh()
        if hasattr(self.category_row, 'refresh'): self.category_row.refresh()
        if hasattr(self.atleta_fields_box, 'refresh'): self.atleta_fields_box.refresh()

    # Callback ora gestito direttamente nella closure on_role_select


    def handle_user_registration(self, widget):
        """Gestisce la registrazione di un nuovo utente"""
        # Raccogli i dati dal form
        username = self.username_input.value.strip() if self.username_input else ""
        email = self.email_input.value.strip() if self.email_input else ""
        first_name = self.first_name_input.value.strip() if self.first_name_input else ""
        last_name = self.last_name_input.value.strip() if self.last_name_input else ""
        password = self.password_input.value if self.password_input else ""
        confirm_password = self.confirm_password_input.value if self.confirm_password_input else ""

        # Combina nome e cognome
        full_name = f"{first_name} {last_name}".strip()

        # Ruolo e categoria/e
        role = self.role_select.value.lower() if self.role_select and self.role_select.value else "user"
        # Se coach: lista da checkbox, se atleta: singola selection
        if role == "coach":
            categories = [cb.text for cb in self.category_checkboxes if cb.value]
        else:
            categories = [self.category_select.value] if self.category_select and self.category_select.value else []

        # Raccogli anche i dati extra per atleta
        data_nascita = self.dob_input.value.strip() if hasattr(self, 'dob_input') and self.dob_input and self.dob_input.value else None
        numero_maglia = self.num_input.value.strip() if hasattr(self, 'num_input') and self.num_input and self.num_input.value else None

        # Validazione campi obbligatori
        if not username:
            self.show_register_status("⚠️ Inserisci un nome utente", "orange")
            return

        if not email:
            self.show_register_status("⚠️ Inserisci un indirizzo email", "orange")
            return

        if not first_name:
            self.show_register_status("⚠️ Inserisci il nome", "orange")
            return

        if not last_name:
            self.show_register_status("⚠️ Inserisci il cognome", "orange")
            return

        if not password:
            self.show_register_status("⚠️ Inserisci una password", "orange")
            return

        # Validazione formato email
        if "@" not in email or "." not in email:
            self.show_register_status("⚠️ Inserisci un indirizzo email valido", "orange")
            return

        # Validazione password
        if len(password) < 6:
            self.show_register_status("⚠️ La password deve essere di almeno 6 caratteri", "orange")
            return

        # Validazione conferma password
        if password != confirm_password:
            self.show_register_status("⚠️ Le password non coincidono", "orange")
            return

        # Validazione categorie
        if role == "coach" and (len(categories) == 0 or len(categories) > 3):
            self.show_register_status("⚠️ Seleziona da 1 a 3 categorie", "orange")
            return
        if role == "atleta" and len(categories) != 1:
            self.show_register_status("⚠️ Seleziona una categoria", "orange")
            return

        # Disabilita il pulsante durante la registrazione
        widget.enabled = False
        self.show_register_status("🔄 Registrazione in corso...", "white")

        try:
            print(f"👤 Tentativo registrazione per utente: {username} ({email}), ruolo: {role}, categorie: {categories}")

            # Effettua la registrazione tramite Supabase, passando ruolo e categorie
            result = auth_service.register(username, email, password, full_name, role, categories)

            if result["success"]:
                self.show_register_status(f"✅ {result['message']}", "lightgreen")
                print(f"✅ Registrazione completata per: {username}")

                # Se atleta, aggiungi anche in tabella giocatori su Supabase
                if role == "atleta":
                    try:
                        giocatore_data = {
                            "nome": first_name,
                            "cognome": last_name,
                            "data_nascita": data_nascita if data_nascita else None,
                            "numero_maglia": int(numero_maglia) if numero_maglia and numero_maglia.isdigit() else None,
                            "email": email,
                            "attivo": True
                        }
                        response = auth_service.supabase.table("giocatori").insert(giocatore_data).execute()
                        print(f"✅ Giocatore inserito su Supabase: {response}")
                    except Exception as e:
                        print(f"❌ Errore inserimento giocatore su Supabase: {e}")

                # Chiudi il dialog dopo 3 secondi
                self.app.add_background_task(self.delayed_close_dialog)
            else:
                self.show_register_status(f"❌ {result['message']}", "orange")
                widget.enabled = True

        except Exception as e:
            print(f"❌ Errore durante registrazione: {e}")
            self.show_register_status(f"❌ Errore di connessione: {str(e)}", "orange")
            widget.enabled = True

    def show_register_status(self, message: str, color: str = "#2c3e50"):
        """Mostra un messaggio di stato nel dialog di registrazione"""
        self.status_label.text = message
        self.status_label.style.color = color

    def close_register_dialog(self, widget=None):
        """Chiude il dialog di registrazione"""
        if self.register_dialog:
            self.register_dialog.close()

    async def delayed_close_dialog(self, widget=None):
        """Chiude il dialog dopo un delay"""
        import asyncio
        await asyncio.sleep(3)
        self.close_register_dialog()