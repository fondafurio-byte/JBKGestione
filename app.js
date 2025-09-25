// Navigazione tra le pagine
console.log('app.js loaded');
const sections = {
  dashboard: document.getElementById('dashboard-section'),
  partite: document.getElementById('partite-section'),
  giocatori: document.getElementById('giocatori-section'),
  allenamenti: document.getElementById('allenamenti-section'),
  statistiche: document.getElementById('statistiche-section'),
  convocati: document.getElementById('convocati-section')
};

function showSection(page) {
  Object.values(sections).forEach(sec => sec.style.display = 'none');
  if (sections[page]) sections[page].style.display = 'block';
}

document.querySelectorAll('.nav-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    const page = btn.getAttribute('data-page');
    if (page) {
      showSection(page);
      if (page === 'dashboard') loadDashboard();
      if (page === 'partite') loadPartite();
      if (page === 'giocatori') loadGiocatori();
      if (page === 'allenamenti') loadAllenamenti();
      if (page === 'statistiche') loadStatistiche();
      if (page === 'convocati') loadConvocati();
    }
  });
});

// Visualizzazione dati per ogni sezione (placeholder, da completare con fetch Supabase)
function loadPartite() {
  const el = document.getElementById('partite-section');
  if (!el) return;
  el.innerHTML = '<h2>Partite</h2><div>Caricamento partite...</div>';
  supabaseClient.from('partite').select('*').then(({ data, error }) => {
    if (error) { el.innerHTML += '<div style="color:red">Errore: '+error.message+'</div>'; return; }
    if (!data || data.length === 0) { el.innerHTML += '<div>Nessuna partita trovata.</div>'; return; }
    let html = '<table style="width:100%;border-collapse:collapse;margin-top:1rem;">';
    html += '<tr style="background:#b71c1c;color:#fff;"><th>Data</th><th>Avversario</th><th>Punti</th><th>Risultato</th></tr>';
    data.forEach(p => {
      html += `<tr><td>${p.data||''}</td><td>${p.avversario||''}</td><td>${p.punti||''}</td><td>${p.risultato||''}</td></tr>`;
    });
    html += '</table>';
    el.innerHTML = '<h2>Partite</h2>' + html;
  });
}

function loadGiocatori() {
  const el = document.getElementById('giocatori-section');
  if (!el) return;
  el.innerHTML = '<h2>Giocatori</h2><div>Caricamento giocatori...</div>';
  supabaseClient.from('giocatori').select('*').then(({ data, error }) => {
    if (error) { el.innerHTML += '<div style="color:red">Errore: '+error.message+'</div>'; return; }
    if (!data || data.length === 0) { el.innerHTML += '<div>Nessun giocatore trovato.</div>'; return; }
    let html = '<table style="width:100%;border-collapse:collapse;margin-top:1rem;">';
    html += '<tr style="background:#b71c1c;color:#fff;"><th>Nome</th><th>Cognome</th><th>Ruolo</th><th>Numero</th></tr>';
    data.forEach(g => {
      html += `<tr><td>${g.nome||''}</td><td>${g.cognome||''}</td><td>${g.ruolo||''}</td><td>${g.numero||''}</td></tr>`;
    });
    html += '</table>';
    el.innerHTML = '<h2>Giocatori</h2>' + html;
  });
}

function loadAllenamenti() {
  const el = document.getElementById('allenamenti-section');
  if (!el) return;
  el.innerHTML = '<h2>Allenamenti</h2><div>Caricamento allenamenti...</div>';
  supabaseClient.from('allenamenti').select('*').then(({ data, error }) => {
    if (error) { el.innerHTML += '<div style="color:red">Errore: '+error.message+'</div>'; return; }
    if (!data || data.length === 0) { el.innerHTML += '<div>Nessun allenamento trovato.</div>'; return; }
    let html = '<table style="width:100%;border-collapse:collapse;margin-top:1rem;">';
    html += '<tr style="background:#b71c1c;color:#fff;"><th>Data</th><th>Luogo</th><th>Note</th></tr>';
    data.forEach(a => {
      html += `<tr><td>${a.data||''}</td><td>${a.luogo||''}</td><td>${a.note||''}</td></tr>`;
    });
    html += '</table>';
    el.innerHTML = '<h2>Allenamenti</h2>' + html;
  });
}

function loadStatistiche() {
  const el = document.getElementById('statistiche-section');
  el.innerHTML = '<h2>Statistiche</h2><div>Caricamento statistiche...</div>';
  // Placeholder: da implementare logica statistiche reali
  el.innerHTML += '<div>Funzionalità in sviluppo.</div>';
}

function loadConvocati() {
  const el = document.getElementById('convocati-section');
  el.innerHTML = '<h2>Convocati</h2><div>Caricamento convocati...</div>';
  // Placeholder: da implementare logica convocati reali
  el.innerHTML += '<div>Funzionalità in sviluppo.</div>';
}

// Mostra dashboard di default dopo login
function showDefaultAfterLogin() {
  showSection('dashboard');
  loadDashboard();
}
// Controllo sessione all'avvio
window.addEventListener('DOMContentLoaded', async () => {
  console.log('DOMContentLoaded fired');
  document.getElementById('debug-msg').textContent = 'JS caricato, controllo sessione...';
  const { data: sessionData } = await supabaseClient.auth.getSession();
  console.log('Session data:', sessionData);
  document.getElementById('debug-msg').textContent += ' Sessione controllata.';
  if (sessionData && sessionData.session) {
    console.log('Session found, showing app');
    document.getElementById('debug-msg').textContent += ' Sessione trovata, mostro app.';
    loginSection.style.display = 'none';
    showDefaultAfterLogin();
  } else {
    console.log('No session, showing login');
    document.getElementById('debug-msg').textContent += ' Nessuna sessione, mostro login.';
    loginSection.style.display = 'block';
    dashboardSection.style.display = 'none';
  }
});
// Configurazione Supabase
const SUPABASE_URL = 'https://hnmzfyzlyadsflhjwsgu.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhubXpmeXpseWFkc2ZsaGp3c2d1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2NDMyMzIsImV4cCI6MjA3NDIxOTIzMn0.CxnEYe-1h2LZkfWwm0ZVJGhzFLWJOyBUAC5djVIwQHA';
if (!window.supabase) {
  console.error('Supabase library not loaded');
  document.getElementById('debug-msg').textContent = 'Errore: libreria Supabase non caricata';
} else {
  const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
  console.log('Supabase client initialized');
}

// Login
const loginForm = document.getElementById('login-form');
const loginSection = document.getElementById('login-section');
const dashboardSection = document.getElementById('dashboard-section');
const loginError = document.getElementById('login-error');
const logoutBtn = document.getElementById('logout-btn');



loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  console.log('Login form submitted');
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
    console.log('Username not found:', profileError);
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
    console.log('Login error:', error);
    loginError.textContent = error.message;
    loginError.style.display = 'block';
  } else {
    console.log('Login successful');
    loginSection.style.display = 'none';
    dashboardSection.style.display = 'block';
    loadDashboard();
  }
});


logoutBtn.addEventListener('click', async () => {
  await supabaseClient.auth.signOut();
  dashboardSection.style.display = 'none';
  loginSection.style.display = 'block';
  showSection('login');
});

// Carica dati dashboard

async function loadDashboard() {
  console.log('loadDashboard called');
  const dashboardContent = document.getElementById('dashboard-content');
  if (!dashboardContent) {
    console.log('dashboard-content not found');
    return;
  }
  console.log('dashboard-content found, loading data');
  dashboardContent.textContent = 'Caricamento...';
  // Fetch dati partite (come anteprima dashboard)
  const { data, error } = await supabaseClient.from('partite').select('*');
  if (error) {
    console.log('Error fetching partite:', error);
    dashboardContent.textContent = 'Errore: ' + error.message;
    return;
  }
  if (!data || data.length === 0) {
    console.log('No partite found');
    dashboardContent.textContent = 'Nessuna partita trovata.';
    return;
  }
  console.log('Partite loaded:', data.length);
  let html = '<h2>Ultime Partite</h2>';
  html += '<table style="width:100%;border-collapse:collapse;margin-top:1rem;">';
  html += '<tr style="background:#b71c1c;color:#fff;"><th>Data</th><th>Avversario</th><th>Punti</th><th>Risultato</th></tr>';
  data.slice(-5).reverse().forEach(partita => {
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
console.log('app.js fully loaded');
