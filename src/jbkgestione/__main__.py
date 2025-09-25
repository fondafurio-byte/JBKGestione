"""
JBK Gestione - App per la gestione di una squadra di basket
"""

__version__ = "0.0.1"

import sys
import os

# Aggiungi il path del modulo se non è disponibile
if __name__ == "__main__":
    # Ottieni il percorso della directory src
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.dirname(current_dir)
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    from jbkgestione.app import main
    main().main_loop()
else:
    from .app import main