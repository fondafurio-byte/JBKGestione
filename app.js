// Controllo sessione all'avvio
window.addEventListener('DOMContentLoaded', async () => {
  const { data: sessionData } = await supabaseClient.auth.getSession();
  if (sessionData && sessionData.session) {
    loginSection.style.display = 'none';
    dashboardSection.style.display = 'block';
    loadDashboard();
  } else {
    loginSection.style.display = 'block';
    dashboardSection.style.display = 'none';
  }
});
// Configurazione Supabase
const SUPABASE_URL = 'https://hnmzfyzlyadsflhjwsgu.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhubXpmeXpseWFkc2ZsaGp3c2d1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2NDMyMzIsImV4cCI6MjA3NDIxOTIzMn0.CxnEYe-1h2LZkfWwm0ZVJGhzFLWJOyBUAC5djVIwQHA';
const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

// Login
const loginForm = document.getElementById('login-form');
const loginSection = document.getElementById('login-section');
const dashboardSection = document.getElementById('dashboard-section');
const loginError = document.getElementById('login-error');
const logoutBtn = document.getElementById('logout-btn');



loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  loginError.style.display = 'none';

  // 1. Cerca email associata allo username
  const { data: profiles, error: profileError } = await supabaseClient
    .from('profiles')
    .select('email')
    .eq('username', username)
    .single();

  if (profileError || !profiles || !profiles.email) {
    loginError.textContent = 'Username non trovato';
    loginError.style.display = 'block';
    return;
  }

  // 2. Login con email trovata
  const { data, error } = await supabaseClient.auth.signInWithPassword({
    email: profiles.email,
    password: password
  });
  if (error) {
    loginError.textContent = error.message;
    loginError.style.display = 'block';
  } else {
    loginSection.style.display = 'none';
    dashboardSection.style.display = 'block';
    loadDashboard();
  }
});


logoutBtn.addEventListener('click', async () => {
  await supabaseClient.auth.signOut();
  dashboardSection.style.display = 'none';
  loginSection.style.display = 'block';
});

// Carica dati dashboard

async function loadDashboard() {
  const dashboardContent = document.getElementById('dashboard-content');
  dashboardContent.textContent = 'Caricamento...';
  // Fetch dati partite
  const { data, error } = await supabaseClient.from('partite').select('*');
  if (error) {
    dashboardContent.textContent = 'Errore: ' + error.message;
    return;
  }
  if (!data || data.length === 0) {
    dashboardContent.textContent = 'Nessuna partita trovata.';
    return;
  }
  // Visualizza tabella partite stile app Python
  let html = '<table style="width:100%;border-collapse:collapse;margin-top:1rem;">';
  html += '<tr style="background:#b71c1c;color:#fff;"><th>Data</th><th>Avversario</th><th>Punti</th><th>Risultato</th></tr>';
  data.forEach(partita => {
    html += `<tr style="border-bottom:1px solid #eee;">
      <td>${partita.data || ''}</td>
      <td>${partita.avversario || ''}</td>
      <td>${partita.punti || ''}</td>
      <td>${partita.risultato || ''}</td>
    </tr>`;
  });
  html += '</table>';
  dashboardContent.innerHTML = html;
}

// Service Worker per PWA
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('service-worker.js');
  });
}
