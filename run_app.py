#!/usr/bin/env python3
"""
JBK GESTIONE - Launcher Script
==============================

Script di avvio semplificato per l'applicazione JBK Gestione.
Gestisce l'inizializzazione dell'ambiente e l'avvio dell'app.
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Verifica che tutte le dipendenze siano installate."""
    required_packages = [
        'toga',
        'supabase', 
        'python-dotenv',
        'sqlite3'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'sqlite3':
                import sqlite3
            elif package == 'toga':
                import toga
            elif package == 'supabase':
                import supabase
            elif package == 'python-dotenv':
                import dotenv
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Dipendenze mancanti:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n💡 Installa con: pip install -r requirements.txt")
        return False
    
    return True

def check_environment():
    """Verifica la configurazione dell'ambiente."""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("⚠️  File .env non trovato!")
        print("💡 Copia .env.example in .env e configura le tue credenziali Supabase")
        return False
    
    # Carica le variabili d'ambiente
    from dotenv import load_dotenv
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Credenziali Supabase mancanti in .env")
        print("💡 Configura SUPABASE_URL e SUPABASE_ANON_KEY")
        return False
    
    return True

def main():
    """Funzione principale di avvio."""
    print("🏀 JBK GESTIONE - Avvio applicazione...\n")
    
    # Verifica dipendenze
    print("🔍 Controllo dipendenze...")
    if not check_dependencies():
        input("Premi Enter per chiudere...")
        sys.exit(1)
    print("✅ Dipendenze OK\n")
    
    # Verifica ambiente
    print("🔧 Controllo configurazione...")
    if not check_environment():
        input("Premi Enter per chiudere...")
        sys.exit(1)
    print("✅ Configurazione OK\n")
    
    # Aggiungi src al path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    # Avvia l'applicazione
    print("🚀 Avvio JBK Gestione...")
    try:
        from jbkgestione.app import main as app_main
        app = app_main()
        app.main_loop()
    except KeyboardInterrupt:
        print("\n👋 Applicazione chiusa dall'utente")
    except Exception as e:
        print(f"❌ Errore durante l'avvio: {e}")
        print("💡 Controlla i log per maggiori dettagli")
        input("Premi Enter per chiudere...")
        sys.exit(1)

if __name__ == '__main__':
    main()