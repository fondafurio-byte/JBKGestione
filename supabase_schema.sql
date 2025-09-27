-- ========================================
-- SCHEMA SQL PER JBK GESTIONE - SUPABASE
-- ========================================

-- ========================================
-- 1. TABELLA PROFILI UTENTI
-- ========================================
CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    full_name TEXT,
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('admin', 'edit', 'user', 'coach', 'atleta')),
    categories JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS per profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Politiche per profiles
CREATE POLICY "Users can view own profile" ON public.profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Admins can view all profiles" ON public.profiles
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Admins can update all profiles" ON public.profiles
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- ========================================
-- 2. TABELLA GIOCATORI
-- ========================================
CREATE TABLE public.giocatori (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    cognome TEXT NOT NULL,
    data_nascita DATE,
    posizione TEXT,
    numero_maglia INTEGER,
    telefono TEXT,
    email TEXT,
    note TEXT,
    attivo BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS per giocatori
ALTER TABLE public.giocatori ENABLE ROW LEVEL SECURITY;

-- Politiche per giocatori
CREATE POLICY "Everyone can view giocatori" ON public.giocatori
    FOR SELECT USING (true);

CREATE POLICY "Admins can insert giocatori" ON public.giocatori
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Admins can update giocatori" ON public.giocatori
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Admins can delete giocatori" ON public.giocatori
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- ========================================
-- 3. TABELLA ALLENAMENTI
-- ========================================
CREATE TABLE public.allenamenti (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    ora TIME,
    luogo TEXT,
    tipo TEXT DEFAULT 'allenamento',
    categoria TEXT,
    note TEXT,
    presenze JSONB DEFAULT '[]'::jsonb,
    assenze_giustificate JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS per allenamenti
ALTER TABLE public.allenamenti ENABLE ROW LEVEL SECURITY;

-- Politiche per allenamenti
CREATE POLICY "Everyone can view allenamenti" ON public.allenamenti
    FOR SELECT USING (true);

CREATE POLICY "Admins can insert allenamenti" ON public.allenamenti
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Admins can update allenamenti" ON public.allenamenti
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Admins can delete allenamenti" ON public.allenamenti
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- ========================================
-- 4. TABELLA PARTITE
-- ========================================
CREATE TABLE public.partite (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    ora TIME,
    avversario TEXT NOT NULL,
    luogo TEXT,
    casa_trasferta TEXT DEFAULT 'casa' CHECK (casa_trasferta IN ('casa', 'trasferta')),
    categoria TEXT,
    risultato_nostro INTEGER,
    risultato_avversario INTEGER,
    note TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS per partite
ALTER TABLE public.partite ENABLE ROW LEVEL SECURITY;

-- Politiche per partite
CREATE POLICY "Everyone can view partite" ON public.partite
    FOR SELECT USING (true);

CREATE POLICY "Admins can insert partite" ON public.partite
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Admins can update partite" ON public.partite
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Admins can delete partite" ON public.partite
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- ========================================
-- 5. TABELLA CONVOCATI
-- ========================================
CREATE TABLE public.convocati (
    id SERIAL PRIMARY KEY,
    partita_id INTEGER REFERENCES public.partite(id) ON DELETE CASCADE,
    giocatore_id INTEGER REFERENCES public.giocatori(id) ON DELETE CASCADE,
    convocato BOOLEAN DEFAULT false,
    rifiutata BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(partita_id, giocatore_id)
);

-- RLS per convocati
ALTER TABLE public.convocati ENABLE ROW LEVEL SECURITY;

-- Politiche per convocati
CREATE POLICY "Everyone can view convocati" ON public.convocati
    FOR SELECT USING (true);

CREATE POLICY "Admins can insert convocati" ON public.convocati
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Admins can update convocati" ON public.convocati
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Admins can delete convocati" ON public.convocati
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- ========================================
-- 6. TABELLA STATISTICHE GIOCATORI
-- ========================================
CREATE TABLE public.statistiche_giocatori (
    id SERIAL PRIMARY KEY,
    partita_id INTEGER REFERENCES public.partite(id) ON DELETE CASCADE,
    giocatore_id INTEGER REFERENCES public.giocatori(id) ON DELETE CASCADE,
    punti INTEGER DEFAULT 0,
    rimbalzi INTEGER DEFAULT 0,
    assist INTEGER DEFAULT 0,
    palle_rubate INTEGER DEFAULT 0,
    palle_perse INTEGER DEFAULT 0,
    falli INTEGER DEFAULT 0,
    minuti_giocati INTEGER DEFAULT 0,
    valutazione DECIMAL(5,2) DEFAULT 0,
    plus_minus INTEGER DEFAULT 0,
    note TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(partita_id, giocatore_id)
);

-- RLS per statistiche_giocatori
ALTER TABLE public.statistiche_giocatori ENABLE ROW LEVEL SECURITY;

-- Politiche per statistiche_giocatori
CREATE POLICY "Everyone can view statistiche_giocatori" ON public.statistiche_giocatori
    FOR SELECT USING (true);

CREATE POLICY "Admins can insert statistiche_giocatori" ON public.statistiche_giocatori
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Admins can update statistiche_giocatori" ON public.statistiche_giocatori
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Admins can delete statistiche_giocatori" ON public.statistiche_giocatori
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- ========================================
-- 7. FUNZIONI E TRIGGER PER UPDATED_AT
-- ========================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger per tutte le tabelle
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_giocatori_updated_at BEFORE UPDATE ON public.giocatori
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_allenamenti_updated_at BEFORE UPDATE ON public.allenamenti
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_partite_updated_at BEFORE UPDATE ON public.partite
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_convocati_updated_at BEFORE UPDATE ON public.convocati
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_statistiche_giocatori_updated_at BEFORE UPDATE ON public.statistiche_giocatori
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- 8. FUNZIONI HELPER PER L'APP
-- ========================================

-- Funzione per verificare se l'utente è admin
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = auth.uid() AND role = 'admin'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Funzione per ottenere il ruolo dell'utente corrente
CREATE OR REPLACE FUNCTION get_user_role()
RETURNS TEXT AS $$
BEGIN
    RETURN (
        SELECT role FROM public.profiles
        WHERE id = auth.uid()
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ========================================
-- 9. INSERIMENTO DATI DI TEST
-- ========================================

-- Inserisci alcuni giocatori di esempio (solo se non esistono)
INSERT INTO public.giocatori (nome, cognome, posizione, numero_maglia, attivo) VALUES
('Marco', 'Rossi', 'Playmaker', 1, true),
('Luca', 'Bianchi', 'Guardia', 2, true),
('Andrea', 'Verdi', 'Ala', 3, true),
('Matteo', 'Neri', 'Centro', 4, true),
('Simone', 'Gialli', 'Ala-Centro', 5, true)
ON CONFLICT DO NOTHING;

-- ========================================
-- 10. INDICI PER PERFORMANCE
-- ========================================
CREATE INDEX IF NOT EXISTS idx_profiles_role ON public.profiles(role);
CREATE INDEX IF NOT EXISTS idx_profiles_categories ON public.profiles USING GIN(categories);
CREATE INDEX IF NOT EXISTS idx_giocatori_attivo ON public.giocatori(attivo);
CREATE INDEX IF NOT EXISTS idx_allenamenti_data ON public.allenamenti(data);
CREATE INDEX IF NOT EXISTS idx_allenamenti_categoria ON public.allenamenti(categoria);
CREATE INDEX IF NOT EXISTS idx_partite_data ON public.partite(data);
CREATE INDEX IF NOT EXISTS idx_partite_categoria ON public.partite(categoria);
CREATE INDEX IF NOT EXISTS idx_convocati_partita ON public.convocati(partita_id);
CREATE INDEX IF NOT EXISTS idx_convocati_giocatore ON public.convocati(giocatore_id);
CREATE INDEX IF NOT EXISTS idx_statistiche_partita ON public.statistiche_giocatori(partita_id);
CREATE INDEX IF NOT EXISTS idx_statistiche_giocatore ON public.statistiche_giocatori(giocatore_id);

-- ========================================
-- 11. COMMENTI SULLE TABELLE
-- ========================================
COMMENT ON TABLE public.profiles IS 'Profili utenti con ruoli admin/user';
COMMENT ON TABLE public.giocatori IS 'Anagrafica giocatori della squadra';
COMMENT ON TABLE public.allenamenti IS 'Allenamenti con presenze/assenze';
COMMENT ON TABLE public.partite IS 'Partite della squadra';
COMMENT ON TABLE public.convocati IS 'Convocazioni per le partite';
COMMENT ON TABLE public.statistiche_giocatori IS 'Statistiche individuali per partita';