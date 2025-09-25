// Navigazione tra le pagine
console.log('app.js loaded - START');

// Configurazione Supabase
const SUPABASE_URL = 'https://hnmzfyzlyadsflhjwsgu.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhubXpmeXpseWFkc2ZsaGp3c2d1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2NDMyMzIsImV4cCI6MjA3NDIxOTIzMn0.CxnEYe-1h2LZkfWwm0ZVJGhzFLWJOyBUAC5djVIwQHA';
let supabaseClient;

console.log('Checking for Supabase library...');
if (!window.supabase) {
  console.error('Supabase library not loaded');
  const debugMsg = document.getElementById('debug-msg');
  if (debugMsg) {
    debugMsg.textContent = 'Errore: libreria Supabase non caricata';
    debugMsg.style.color = 'red';
  }
} else {
  console.log('Supabase library found, creating client...');
  supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
  console.log('Supabase client initialized successfully');
}

// Elementi DOM
console.log('Getting DOM elements...');
const sections = {
  dashboard: document.getElementById('dashboard-section'),
  partite: document.getElementById('partite-section'),
  giocatori: document.getElementById('giocatori-section'),
  allenamenti: document.getElementById('allenamenti-section'),
  statistiche: document.getElementById('statistiche-section')
};

const loginForm = document.getElementById('login-form');
const loginSection = document.getElementById('login-section');
const dashboardSection = document.getElementById('dashboard-section');
const loginError = document.getElementById('login-error');
const logoutBtn = document.getElementById('logout-btn');

console.log('DOM elements:', {
  sections,
  loginForm,
  loginSection,
  dashboardSection,
  loginError,
  logoutBtn
});

// Verifica che tutti gli elementi esistano
if (!loginForm || !loginSection || !dashboardSection || !loginError || !logoutBtn) {
  console.error('Alcuni elementi DOM non trovati!');
  const debugMsg = document.getElementById('debug-msg');
  if (debugMsg) {
    debugMsg.textContent = 'Errore: elementi DOM mancanti';
    debugMsg.style.color = 'red';
  }
} else {
  console.log('Tutti gli elementi DOM trovati correttamente');
}

function showSection(page) {
  Object.values(sections).forEach(sec => sec.style.display = 'none');
  if (sections[page]) sections[page].style.display = 'block';
}

// Gestione visibilità app
function showApp() {
  console.log('showApp called');
  const loginSection = document.getElementById('login-section');
  const appContent = document.getElementById('app-content');

  if (loginSection) {
    loginSection.classList.remove('show');
    loginSection.classList.add('hide');
    console.log('login-section hidden via class');
  } else {
    console.error('login-section not found');
  }

  if (appContent) {
    appContent.classList.remove('hide');
    appContent.classList.add('show');
    console.log('app-content shown via class');
  } else {
    console.error('app-content not found');
  }
}

function showLogin() {
  console.log('showLogin called');
  const loginSection = document.getElementById('login-section');
  const appContent = document.getElementById('app-content');

  if (loginSection) {
    loginSection.classList.remove('hide');
    loginSection.classList.add('show');
    console.log('login-section shown via class');
  } else {
    console.error('login-section not found');
  }

  if (appContent) {
    appContent.classList.remove('show');
    appContent.classList.add('hide');
    console.log('app-content hidden via class');
  } else {
    console.error('app-content not found');
  }
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
    }
  });
});

// Mostra dashboard di default dopo login
function showDefaultAfterLogin() {
  showSection('dashboard');
  loadDashboard();
}

// Controllo sessione all'avvio
console.log('Setting up DOMContentLoaded listener...');
window.addEventListener('DOMContentLoaded', async () => {
  console.log('DOMContentLoaded fired');
  const debugMsg = document.getElementById('debug-msg');
  if (debugMsg) {
    debugMsg.textContent = 'JS caricato, controllo sessione...';
  }

  if (!supabaseClient) {
    console.error('Supabase client not available');
    if (debugMsg) {
      debugMsg.textContent += ' Errore: Supabase non disponibile';
      debugMsg.style.color = 'red';
    }
    return;
  }

  try {
    const { data: sessionData } = await supabaseClient.auth.getSession();
    console.log('Session data:', sessionData);

    if (debugMsg) {
      debugMsg.textContent += ' Sessione controllata.';
    }

    if (sessionData && sessionData.session) {
      console.log('Session found, showing app');
      if (debugMsg) {
        debugMsg.textContent += ' Sessione trovata, mostro app.';
      }
      showApp();
      showDefaultAfterLogin();
    } else {
      console.log('No session, showing login');
      if (debugMsg) {
        debugMsg.textContent += ' Nessuna sessione, mostro login.';
      }
      showLogin();
    }
  } catch (error) {
    console.error('Error during session check:', error);
    if (debugMsg) {
      debugMsg.textContent += ' Errore controllo sessione: ' + error.message;
      debugMsg.style.color = 'red';
    }
  }
});

// Fallback nel caso DOMContentLoaded non si triggeri
setTimeout(() => {
  console.log('Fallback timeout check');
  const debugMsg = document.getElementById('debug-msg');
  if (debugMsg && debugMsg.textContent === '') {
    console.log('DOMContentLoaded might not have fired, running fallback');
    debugMsg.textContent = 'Fallback: controllo sessione...';
    // Simula il DOMContentLoaded
    const event = new Event('DOMContentLoaded');
    window.dispatchEvent(event);
  }
}, 1000);

// Secondo fallback - controllo diretto se l'app è già inizializzata
setTimeout(async () => {
  console.log('Second fallback check');
  const loginSection = document.getElementById('login-section');
  const appContent = document.getElementById('app-content');

  // Se entrambi gli elementi sono ancora nascosti/mostrati in modo anomalo, forza l'inizializzazione
  if (loginSection && appContent &&
      !loginSection.classList.contains('show') &&
      !loginSection.classList.contains('hide') &&
      !appContent.classList.contains('show') &&
      !appContent.classList.contains('hide')) {

    console.log('App not properly initialized, forcing session check');
    const debugMsg = document.getElementById('debug-msg');
    if (debugMsg) {
      debugMsg.textContent = 'Forzando inizializzazione...';
    }

    if (!supabaseClient) {
      console.error('Supabase client not available in fallback');
      if (debugMsg) {
        debugMsg.textContent += ' Errore: Supabase non disponibile';
        debugMsg.style.color = 'red';
      }
      return;
    }

    try {
      const { data: sessionData } = await supabaseClient.auth.getSession();
      console.log('Fallback session data:', sessionData);

      if (sessionData && sessionData.session) {
        console.log('Fallback: Session found, showing app');
        showApp();
        showDefaultAfterLogin();
      } else {
        console.log('Fallback: No session, showing login');
        showLogin();
      }
    } catch (error) {
      console.error('Error in fallback session check:', error);
      if (debugMsg) {
        debugMsg.textContent += ' Errore fallback: ' + error.message;
        debugMsg.style.color = 'red';
      }
    }
  }
}, 2000);

// Login
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
    showApp();
    dashboardSection.style.display = 'block';
    loadDashboard();
  }
});

logoutBtn.addEventListener('click', async () => {
  await supabaseClient.auth.signOut();
  showLogin();
  showSection('login');
});

// Carica dati dashboard
async function loadDashboard() {
  console.log('loadDashboard called');
  const section = document.getElementById('dashboard-section');
  if (!section) {
    console.log('dashboard-section not found');
    return;
  }
  console.log('dashboard-section found, loading data');
  section.innerHTML = '<div>Caricamento...</div>';
  // Fetch dati partite (come anteprima dashboard)
  const { data, error } = await supabaseClient.from('partite').select('*');
  if (error) {
    console.log('Error fetching partite:', error);
    section.innerHTML = '<div>Errore: ' + error.message + '</div>';
    return;
  }
  if (!data || data.length === 0) {
    console.log('No partite found');
    section.innerHTML = '<div>Nessuna partita trovata.</div>';
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
  section.innerHTML = html;
}

// Visualizzazione dati per ogni sezione
function loadPartite() {
  const el = document.getElementById('partite-section');
  if (!el) return;
  el.innerHTML = '<h2>Partite</h2><button onclick="mostraFormNuovaPartita()">Aggiungi Partita</button><div>Caricamento partite...</div>';
  supabaseClient.from('partite').select('*').then(({ data, error }) => {
    if (error) { el.innerHTML += '<div style="color:red">Errore: '+error.message+'</div>'; return; }
    if (!data || data.length === 0) { el.innerHTML += '<div>Nessuna partita trovata.</div>'; return; }
    let html = '<table style="width:100%;border-collapse:collapse;margin-top:1rem;">';
    html += '<tr style="background:#b71c1c;color:#fff;"><th>Data</th><th>Avversario</th><th>Punti</th><th>Risultato</th><th>Azioni</th></tr>';
    data.forEach(p => {
      html += `<tr><td>${p.data||''}</td><td>${p.avversario||''}</td><td>${p.punti||''}</td><td>${p.risultato||''}</td><td><button onclick="gestisciConvocati(${p.id})">Convocati</button></td></tr>`;
    });
    html += '</table>';
    el.innerHTML = '<h2>Partite</h2><button onclick="mostraFormNuovaPartita()">Aggiungi Partita</button>' + html;
  });
}

function loadGiocatori() {
  const el = document.getElementById('giocatori-section');
  if (!el) return;
  el.innerHTML = '<h2>Giocatori</h2><button onclick="mostraFormNuovoGiocatore()">Aggiungi Giocatore</button><div>Caricamento giocatori...</div>';
  supabaseClient.from('giocatori').select('*').then(({ data, error }) => {
    if (error) { el.innerHTML += '<div style="color:red">Errore: '+error.message+'</div>'; return; }
    if (!data || data.length === 0) { el.innerHTML += '<div>Nessun giocatore trovato.</div>'; return; }
    let html = '<table style="width:100%;border-collapse:collapse;margin-top:1rem;">';
    html += '<tr style="background:#b71c1c;color:#fff;"><th>Nome</th><th>Cognome</th><th>Ruolo</th><th>Numero</th></tr>';
    data.forEach(g => {
      html += `<tr><td>${g.nome||''}</td><td>${g.cognome||''}</td><td>${g.ruolo||''}</td><td>${g.numero||''}</td></tr>`;
    });
    html += '</table>';
    el.innerHTML = '<h2>Giocatori</h2><button onclick="mostraFormNuovoGiocatore()">Aggiungi Giocatore</button>' + html;
  });
}

function loadAllenamenti() {
  const el = document.getElementById('allenamenti-section');
  if (!el) return;
  el.innerHTML = '<h2>Allenamenti</h2><button onclick="mostraFormNuovoAllenamento()">Aggiungi Allenamento</button><div>Caricamento allenamenti...</div>';
  supabaseClient.from('allenamenti').select('*').then(({ data, error }) => {
    if (error) { el.innerHTML += '<div style="color:red">Errore: '+error.message+'</div>'; return; }
    if (!data || data.length === 0) { el.innerHTML += '<div>Nessun allenamento trovato.</div>'; return; }
    let html = '<table style="width:100%;border-collapse:collapse;margin-top:1rem;">';
    html += '<tr style="background:#b71c1c;color:#fff;"><th>Data</th><th>Luogo</th><th>Note</th></tr>';
    data.forEach(a => {
      html += `<tr><td>${a.data||''}</td><td>${a.luogo||''}</td><td>${a.note||''}</td></tr>`;
    });
    html += '</table>';
    el.innerHTML = '<h2>Allenamenti</h2><button onclick="mostraFormNuovoAllenamento()">Aggiungi Allenamento</button>' + html;
  });
}

function loadDashboard() {
  const section = document.getElementById('dashboard-section');
  if (!section) return;

  section.innerHTML = '<h2>Dashboard</h2><div>Caricamento dati...</div>';

  // Carica dati da tutte le tabelle per creare statistiche riepilogative
  Promise.all([
    supabaseClient.from('partite').select('*'),
    supabaseClient.from('giocatori').select('*'),
    supabaseClient.from('allenamenti').select('*')
  ]).then(([partiteRes, giocatoriRes, allenamentiRes]) => {
    const partite = partiteRes.data || [];
    const giocatori = giocatoriRes.data || [];
    const allenamenti = allenamentiRes.data || [];

    console.log('Dashboard data loaded:', { partite: partite.length, giocatori: giocatori.length, allenamenti: allenamenti.length });

    let html = '<h2>Dashboard</h2>';

    // Statistiche riepilogative
    html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">';
    html += `<div style="background: #f5f5f5; padding: 1rem; border-radius: 8px; text-align: center;">
      <h3>${partite.length}</h3>
      <p>Partite Totali</p>
    </div>`;
    html += `<div style="background: #f5f5f5; padding: 1rem; border-radius: 8px; text-align: center;">
      <h3>${giocatori.length}</h3>
      <p>Giocatori</p>
    </div>`;
    html += `<div style="background: #f5f5f5; padding: 1rem; border-radius: 8px; text-align: center;">
      <h3>${allenamenti.length}</h3>
      <p>Allenamenti</p>
    </div>`;
    html += '</div>';

    // Ultime partite
    if (partite.length > 0) {
      html += '<h3>Ultime Partite</h3>';
      html += '<table style="width:100%;border-collapse:collapse;margin-top:1rem;">';
      html += '<tr style="background:#b71c1c;color:#fff;"><th>Data</th><th>Avversario</th><th>Risultato</th></tr>';
      partite.slice(-3).reverse().forEach(partita => {
        html += `<tr style="border-bottom:1px solid #eee;">
          <td>${partita.data || ''}</td>
          <td>${partita.avversario || ''}</td>
          <td>${partita.risultato || ''}</td>
        </tr>`;
      });
      html += '</table>';
    }

    // Prossimi allenamenti
    if (allenamenti.length > 0) {
      html += '<h3>Prossimi Allenamenti</h3>';
      html += '<table style="width:100%;border-collapse:collapse;margin-top:1rem;">';
      html += '<tr style="background:#b71c1c;color:#fff;"><th>Data</th><th>Luogo</th><th>Note</th></tr>';
      allenamenti.slice(-3).reverse().forEach(allenamento => {
        html += `<tr style="border-bottom:1px solid #eee;">
          <td>${allenamento.data || ''}</td>
          <td>${allenamento.luogo || ''}</td>
          <td>${allenamento.note || ''}</td>
        </tr>`;
      });
      html += '</table>';
    }

    section.innerHTML = html;
  }).catch(error => {
    console.error('Error loading dashboard:', error);
    section.innerHTML = '<h2>Dashboard</h2><div style="color:red">Errore nel caricamento dei dati: ' + error.message + '</div>';
  });
}

function loadStatistiche() {
  const section = document.getElementById('statistiche-section');
  if (!section) return;

  section.innerHTML = '<h2>Statistiche</h2><div>Caricamento statistiche...</div>';

  // Carica tutti i dati per calcolare statistiche
  Promise.all([
    supabaseClient.from('partite').select('*'),
    supabaseClient.from('giocatori').select('*'),
    supabaseClient.from('allenamenti').select('*')
  ]).then(([partiteRes, giocatoriRes, allenamentiRes]) => {
    const partite = partiteRes.data || [];
    const giocatori = giocatoriRes.data || [];
    const allenamenti = allenamentiRes.data || [];

    console.log('Statistics data loaded:', { partite: partite.length, giocatori: giocatori.length, allenamenti: allenamenti.length });

    let html = '<h2>Statistiche Squadra</h2>';

    // Calcola statistiche delle partite
    const vittorie = partite.filter(p => p.risultato && p.risultato.toLowerCase().includes('vinto')).length;
    const pareggi = partite.filter(p => p.risultato && p.risultato.toLowerCase().includes('pareggio')).length;
    const sconfitte = partite.filter(p => p.risultato && !p.risultato.toLowerCase().includes('vinto') && !p.risultato.toLowerCase().includes('pareggio')).length;

    // Statistiche partite
    html += '<h3>Risultati Partite</h3>';
    html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 2rem;">';
    html += `<div style="background: #4caf50; color: white; padding: 1rem; border-radius: 8px; text-align: center;">
      <h3>${vittorie}</h3>
      <p>Vittorie</p>
    </div>`;
    html += `<div style="background: #ff9800; color: white; padding: 1rem; border-radius: 8px; text-align: center;">
      <h3>${pareggi}</h3>
      <p>Pareggi</p>
    </div>`;
    html += `<div style="background: #f44336; color: white; padding: 1rem; border-radius: 8px; text-align: center;">
      <h3>${sconfitte}</h3>
      <p>Sconfitte</p>
    </div>`;
    html += `<div style="background: #2196f3; color: white; padding: 1rem; border-radius: 8px; text-align: center;">
      <h3>${partite.length}</h3>
      <p>Totale Partite</p>
    </div>`;
    html += '</div>';

    // Statistiche giocatori per ruolo
    const ruoli = {};
    giocatori.forEach(g => {
      const ruolo = g.ruolo || 'Non specificato';
      ruoli[ruolo] = (ruoli[ruolo] || 0) + 1;
    });

    html += '<h3>Giocatori per Ruolo</h3>';
    html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 2rem;">';
    Object.entries(ruoli).forEach(([ruolo, count]) => {
      html += `<div style="background: #f5f5f5; padding: 1rem; border-radius: 8px; text-align: center;">
        <h3>${count}</h3>
        <p>${ruolo}</p>
      </div>`;
    });
    html += '</div>';

    // Statistiche allenamenti
    const mesi = {};
    allenamenti.forEach(a => {
      if (a.data) {
        const mese = new Date(a.data).getMonth() + 1;
        mesi[mese] = (mesi[mese] || 0) + 1;
      }
    });

    html += '<h3>Allenamenti per Mese</h3>';
    html += '<table style="width:100%;border-collapse:collapse;margin-top:1rem;">';
    html += '<tr style="background:#b71c1c;color:#fff;"><th>Mese</th><th>Allenamenti</th></tr>';
    Object.entries(mesi).sort(([a], [b]) => a - b).forEach(([mese, count]) => {
      const nomeMese = new Date(2024, mese - 1, 1).toLocaleString('it-IT', { month: 'long' });
      html += `<tr style="border-bottom:1px solid #eee;">
        <td>${nomeMese}</td>
        <td>${count}</td>
      </tr>`;
    });
    html += '</table>';

    section.innerHTML = html;
  }).catch(error => {
    console.error('Error loading statistics:', error);
    section.innerHTML = '<h2>Statistiche</h2><div style="color:red">Errore nel caricamento delle statistiche: ' + error.message + '</div>';
  });
}

// Placeholder per funzioni mancanti
function mostraFormNuovaPartita() { alert('Funzione in sviluppo'); }
function mostraFormNuovoGiocatore() { alert('Funzione in sviluppo'); }
function mostraFormNuovoAllenamento() { alert('Funzione in sviluppo'); }
function gestisciConvocati(id) { alert('Funzione in sviluppo per partita ' + id); }

// Service Worker per PWA - TEMPORANEAMENTE DISABILITATO
/*
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('service-worker.js').then(registration => {
      registration.update(); // Forza aggiornamento
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;
        if (newWorker) {
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // Nuovo SW disponibile, ricarica pagina
              window.location.reload();
            }
          });
        }
      });
    });
  });
}
*/

console.log('app.js fully loaded');
