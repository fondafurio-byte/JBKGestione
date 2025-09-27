#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Test delle sezioni dashboard
try:
    from jbkgestione.app import JBKGestione
    from jbkgestione.supabase_db import SupabaseDBManager
    import toga

    print("🔍 Test creazione sezioni dashboard...")

    # Crea un'istanza minima dell'app per testare
    app = JBKGestione()

    # Inizializza il database
    app.supabase_db = SupabaseDBManager()

    # Test creazione sezione statistiche
    print("📊 Test creazione sezione statistiche...")
    stat_section = app.crea_sezione_statistiche_squadra()
    print(f"📊 Sezione statistiche creata: {type(stat_section)}")

    # Test creazione sezione valutazione
    print("⭐ Test creazione sezione valutazione...")
    val_section = app.crea_sezione_valutazione_squadra()
    print(f"⭐ Sezione valutazione creata: {type(val_section)}")

    print("✅ Test completato con successo!")

except Exception as e:
    print(f"❌ Errore durante il test: {e}")
    import traceback
    traceback.print_exc()
