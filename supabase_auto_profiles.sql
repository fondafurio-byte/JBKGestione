-- ========================================
-- TRIGGER AUTOMATICO PER CREAZIONE PROFILI
-- ========================================
-- Esegui questo SQL in Supabase per creare automaticamente 
-- i profili quando si aggiungono nuovi utenti

-- Prima aggiungiamo la colonna username alla tabella profiles
ALTER TABLE public.profiles ADD COLUMN IF NOT EXISTS username TEXT UNIQUE;
ALTER TABLE public.profiles ADD COLUMN IF NOT EXISTS categories JSONB DEFAULT '[]'::jsonb;

-- Funzione per creare automaticamente il profilo
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email, username, full_name, role, categories)
  VALUES (
    new.id,
    new.email,
    COALESCE(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1)),
    COALESCE(new.raw_user_meta_data->>'full_name', ''),
    COALESCE(new.raw_user_meta_data->>'role', 'user'),
    COALESCE(new.raw_user_meta_data->>'categories', '[]')::jsonb
  );
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger che si attiva quando viene creato un nuovo utente
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Query per creare profili per utenti esistenti senza profilo
INSERT INTO public.profiles (id, email, username, full_name, role, categories)
SELECT 
  au.id,
  au.email,
  COALESCE(au.raw_user_meta_data->>'username', split_part(au.email, '@', 1)),
  COALESCE(au.raw_user_meta_data->>'full_name', ''),
  COALESCE(au.raw_user_meta_data->>'role', 'user'),
  COALESCE(au.raw_user_meta_data->>'categories', '[]')::jsonb
FROM auth.users au
LEFT JOIN public.profiles p ON au.id = p.id
WHERE p.id IS NULL;

-- Messaggio di conferma
SELECT 'Trigger creato con successo! Profili creati per utenti esistenti.' as message;