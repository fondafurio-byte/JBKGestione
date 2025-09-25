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

// === IBRIDO PWA/NATIVO DETECTION ===
let isPWA = false;
let isOnline = navigator.onLine;

// Rilevamento PWA (Progressive Web App)
function checkPWAStatus() {
  // Controlla se è in modalità standalone (installata come app)
  isPWA = window.matchMedia('(display-mode: standalone)').matches ||
           window.navigator.standalone === true ||
           document.referrer.includes('android-app://');

  console.log('🔍 PWA Status:', isPWA ? 'INSTALLATA (Standalone)' : 'WEB (Browser)');

  // Aggiorna UI basata sulla modalità
  updateUIBasedOnMode();

  return isPWA;
}

// Aggiorna l'interfaccia basata sulla modalità (PWA vs Web)
function updateUIBasedOnMode() {
  const body = document.body;
  const header = document.querySelector('header h1');

  if (isPWA) {
    // Modalità PWA - stile più nativo
    body.classList.add('pwa-mode');
    if (header) {
      header.textContent = '🏀 JBK Gestione';
      const small = document.createElement('small');
      small.style.cssText = 'font-size: 0.6em; color: #666; margin-left: 5px;';
      small.textContent = 'v1.0';
      header.appendChild(small);
    }

    // Aggiungi indicatore PWA
    addPWABadge();

    // Abilita notifiche push se supportate
    requestNotificationPermission();

  } else {
    // Modalità Web - stile browser standard
    body.classList.remove('pwa-mode');
    if (header) {
      header.textContent = '🌐 JBK Gestione';
      const small = document.createElement('small');
      small.style.cssText = 'font-size: 0.6em; color: #666; margin-left: 5px;';
      small.textContent = 'Web';
      header.appendChild(small);
    }
  }
}

// Aggiungi badge PWA nell'header
function addPWABadge() {
  const header = document.querySelector('header');
  if (header && !document.querySelector('.pwa-badge')) {
    const badge = document.createElement('div');
    badge.className = 'pwa-badge';
    badge.textContent = '📱 PWA';
    badge.style.cssText = `
      position: absolute;
      top: 10px;
      right: 10px;
      background: #4CAF50;
      color: white;
      padding: 2px 8px;
      border-radius: 10px;
      font-size: 0.7em;
      font-weight: bold;
    `;
    header.style.position = 'relative';
    header.appendChild(badge);
  }
}

// Richiedi permesso notifiche (solo in PWA)
async function requestNotificationPermission() {
  if ('Notification' in window && isPWA) {
    const permission = await Notification.requestPermission();
    console.log('📢 Notification permission:', permission);
  }
}

// Gestione connettività
function handleConnectivityChange() {
  isOnline = navigator.onLine;
  console.log('🌐 Connectivity changed:', isOnline ? 'ONLINE' : 'OFFLINE');

  // Mostra indicatore di connessione
  showConnectivityStatus();

  if (!isOnline) {
    // Modalità offline - salva dati localmente
    console.log('💾 Switching to offline mode');
  }
}

// Mostra stato connessione
function showConnectivityStatus() {
  let statusDiv = document.querySelector('.connectivity-status');
  if (!statusDiv) {
    statusDiv = document.createElement('div');
    statusDiv.className = 'connectivity-status';
    statusDiv.style.cssText = `
      position: fixed;
      top: 60px;
      right: 10px;
      padding: 5px 10px;
      border-radius: 5px;
      font-size: 0.8em;
      z-index: 1000;
    `;
    document.body.appendChild(statusDiv);
  }

  if (isOnline) {
    statusDiv.textContent = '🟢 Online';
    statusDiv.style.background = '#4CAF50';
    statusDiv.style.color = 'white';
    setTimeout(() => statusDiv.remove(), 3000); // Rimuovi dopo 3 secondi
  } else {
    statusDiv.textContent = '🔴 Offline';
    statusDiv.style.background = '#f44336';
    statusDiv.style.color = 'white';
  }
}

// Inizializzazione ibrida
function initHybridFeatures() {
  console.log('🚀 Initializing hybrid features...');

  // Rileva modalità PWA
  checkPWAStatus();

  // Gestione connettività
  window.addEventListener('online', handleConnectivityChange);
  window.addEventListener('offline', handleConnectivityChange);

  // Rileva cambiamenti display mode (installazione PWA)
  window.matchMedia('(display-mode: standalone)').addEventListener('change', (e) => {
    isPWA = e.matches;
    console.log('🔄 Display mode changed:', isPWA ? 'standalone' : 'browser');
    updateUIBasedOnMode();
  });

  // Install prompt per PWA
  let deferredPrompt;
  window.addEventListener('beforeinstallprompt', (e) => {
    console.log('📱 PWA install prompt available');
    e.preventDefault();
    deferredPrompt = e;

    // Mostra pulsante installa se non è già PWA
    if (!isPWA) {
      showInstallButton(deferredPrompt);
    }
  });
}

// Mostra pulsante installa PWA
function showInstallButton(deferredPrompt) {
  const header = document.querySelector('header');
  if (header && !document.querySelector('.install-btn')) {
    const installBtn = document.createElement('button');
    installBtn.className = 'install-btn';
    installBtn.textContent = '📱 Installa App';
    installBtn.style.cssText = `
      position: absolute;
      top: 10px;
      right: 10px;
      background: #2196F3;
      color: white;
      border: none;
      padding: 8px 15px;
      border-radius: 5px;
      cursor: pointer;
      font-size: 0.9em;
    `;

    installBtn.addEventListener('click', async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        console.log('📱 PWA install outcome:', outcome);
        if (outcome === 'accepted') {
          isPWA = true;
          updateUIBasedOnMode();
        }
        deferredPrompt = null;
        installBtn.remove();
      }
    });

    header.style.position = 'relative';
    header.appendChild(installBtn);
  }
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

  // Inizializza funzionalità ibride PWA/Native
  initHybridFeatures();

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

  // Clear existing content
  section.innerHTML = '';

  const loadingDiv = document.createElement('div');
  loadingDiv.textContent = 'Caricamento...';
  section.appendChild(loadingDiv);

  // Fetch dati partite (come anteprima dashboard)
  const { data, error } = await supabaseClient.from('partite').select('*');
  if (error) {
    console.log('Error fetching partite:', error);
    section.innerHTML = '';
    const errorDiv = document.createElement('div');
    errorDiv.textContent = 'Errore: ' + error.message;
    section.appendChild(errorDiv);
    return;
  }
  if (!data || data.length === 0) {
    console.log('No partite found');
    section.innerHTML = '';
    const noDataDiv = document.createElement('div');
    noDataDiv.textContent = 'Nessuna partita trovata.';
    section.appendChild(noDataDiv);
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
  const section = document.getElementById('partite-section');
  if (!section) return;

  // Clear existing content
  section.innerHTML = '';

  // Create title
  const h2 = document.createElement('h2');
  h2.textContent = 'Partite';
  section.appendChild(h2);

  // Create actions bar
  const actionsBar = document.createElement('div');
  actionsBar.className = 'actions-bar';

  const addButton = document.createElement('button');
  addButton.onclick = showAddPartitaForm;
  addButton.className = 'btn-add';
  addButton.textContent = '➕ Aggiungi Partita';
  actionsBar.appendChild(addButton);

  const select = document.createElement('select');
  select.id = 'filtro-tipologia';
  select.onchange = function() { filtraPartite(this.value); };

  const options = [
    { value: 'tutte', text: 'Tutte le Partite' },
    { value: 'pre-stagione', text: 'Pre-stagione' },
    { value: 'stagione regolare', text: 'Stagione Regolare' },
    { value: 'post-stagione', text: 'Post-stagione' },
    { value: 'tornei', text: 'Tornei' }
  ];

  options.forEach(opt => {
    const option = document.createElement('option');
    option.value = opt.value;
    option.textContent = opt.text;
    select.appendChild(option);
  });

  actionsBar.appendChild(select);
  section.appendChild(actionsBar);

  // Create content container
  const content = document.createElement('div');
  content.id = 'partite-content';

  const loadingDiv = document.createElement('div');
  loadingDiv.textContent = 'Caricamento partite...';
  content.appendChild(loadingDiv);

  section.appendChild(content);

  filtraPartite('tutte');
}

function filtraPartite(tipologia) {
  const content = document.getElementById('partite-content');
  if (!content) return;

  // Clear existing content
  content.innerHTML = '';

  const loadingDiv = document.createElement('div');
  loadingDiv.textContent = 'Caricamento partite...';
  content.appendChild(loadingDiv);

  let query = supabaseClient.from('partite').select('*').order('data', { ascending: false });

  if (tipologia !== 'tutte') {
    query = query.eq('tipologia', tipologia);
  }

  query.then(({ data, error }) => {
    if (error) {
      content.innerHTML = '';
      const errorDiv = document.createElement('div');
      errorDiv.style.color = 'red';
      errorDiv.textContent = 'Errore: ' + error.message;
      content.appendChild(errorDiv);
      return;
    }

    if (!data || data.length === 0) {
      content.innerHTML = '';
      const noDataDiv = document.createElement('div');
      noDataDiv.textContent = 'Nessuna partita trovata.';
      content.appendChild(noDataDiv);
      return;
    }

    // Clear loading content
    content.innerHTML = '';

    const partiteList = document.createElement('div');
    partiteList.className = 'partite-list';

    data.forEach(p => {
      const casaIcon = p.in_casa ? '🏠' : '✈️';
      const vsPrefix = p.in_casa ? 'vs' : '@';
      const risultato = (p.risultato_nostro !== null && p.risultato_avversario !== null) ?
        ` (${p.risultato_nostro}-${p.risultato_avversario})` : '';

      const tipologiaColors = {
        'pre-stagione': '#ff9800',
        'stagione regolare': '#4caf50',
        'post-stagione': '#2196f3',
        'tornei': '#9c27b0'
      };
      const bgColor = tipologiaColors[p.tipologia] || '#607d8b';

      // Create partita card
      const card = document.createElement('div');
      card.className = 'partita-card';

      // Create partita info
      const info = document.createElement('div');
      info.className = 'partita-info';

      // Create header
      const header = document.createElement('div');
      header.className = 'partita-header';

      const icon = document.createElement('span');
      icon.className = 'partita-icon';
      icon.textContent = casaIcon;
      header.appendChild(icon);

      const strong = document.createElement('strong');
      strong.textContent = `${vsPrefix} ${p.avversario}${risultato}`;
      header.appendChild(strong);

      const tipologia = document.createElement('span');
      tipologia.className = 'partita-tipologia';
      tipologia.style.backgroundColor = bgColor;
      tipologia.textContent = p.tipologia || 'stagione regolare';
      header.appendChild(tipologia);

      info.appendChild(header);

      // Create details
      const details = document.createElement('div');
      details.className = 'partita-details';
      details.textContent = `📅 ${p.data} ⏰ ${p.ora || 'N/A'}`;
      info.appendChild(details);

      card.appendChild(info);

      // Create actions
      const actions = document.createElement('div');
      actions.className = 'partita-actions';

      const convocatiBtn = document.createElement('button');
      convocatiBtn.className = 'btn-convocati';
      convocatiBtn.title = 'Convocati';
      convocatiBtn.textContent = '👥';
      convocatiBtn.onclick = () => gestisciConvocati(p.id);
      actions.appendChild(convocatiBtn);

      const editBtn = document.createElement('button');
      editBtn.className = 'btn-edit';
      editBtn.textContent = '✏️';
      editBtn.onclick = () => editPartita(p.id);
      actions.appendChild(editBtn);

      const deleteBtn = document.createElement('button');
      deleteBtn.className = 'btn-delete';
      deleteBtn.textContent = '🗑️';
      deleteBtn.onclick = () => deletePartita(p.id);
      actions.appendChild(deleteBtn);

      card.appendChild(actions);
      partiteList.appendChild(card);
    });

    content.appendChild(partiteList);
  });
}

function loadGiocatori() {
  const section = document.getElementById('giocatori-section');
  if (!section) return;

  section.innerHTML = `
    <h2>Giocatori</h2>
    <div class="actions-bar">
      <button onclick="showAddGiocatoreForm()" class="btn-add">➕ Aggiungi Giocatore</button>
      <button onclick="loadGiocatoriList()" class="btn-list">📋 Lista Giocatori</button>
    </div>
    <div id="giocatori-content">
      <div>Caricamento giocatori...</div>
    </div>
  `;

  loadGiocatoriList();
}

function loadAllenamenti() {
  const section = document.getElementById('allenamenti-section');
  if (!section) return;

  section.innerHTML = `
    <h2>Allenamenti</h2>
    <div class="actions-bar">
      <button onclick="showAddAllenamentoForm()" class="btn-add">➕ Aggiungi Allenamento</button>
    </div>
    <div id="allenamenti-content">
      <div>Caricamento allenamenti...</div>
    </div>
  `;

  loadAllenamentiList();
}

function loadAllenamentiList() {
  const content = document.getElementById('allenamenti-content');
  if (!content) return;

  content.innerHTML = '<div>Caricamento allenamenti...</div>';

  supabaseClient.from('allenamenti').select('*').order('data', { ascending: false }).then(({ data, error }) => {
    if (error) {
      content.innerHTML = '<div style="color:red">Errore: ' + error.message + '</div>';
      return;
    }

    if (!data || data.length === 0) {
      content.innerHTML = '<div>Nessun allenamento trovato.</div>';
      return;
    }

    let html = '<div class="allenamenti-list">';
    data.forEach(a => {
      html += `
        <div class="allenamento-card">
          <div class="allenamento-info">
            <div class="allenamento-header">
              <strong>💪 Allenamento</strong>
            </div>
            <div class="allenamento-details">
              📅 ${a.data} ${a.ora ? `⏰ ${a.ora}` : ''}<br>
              📍 ${a.luogo || 'Luogo non specificato'}
              ${a.note ? `<br>📝 ${a.note}` : ''}
            </div>
          </div>
          <div class="allenamento-actions">
            <button onclick="editAllenamento(${a.id})" class="btn-edit">✏️</button>
            <button onclick="deleteAllenamento(${a.id})" class="btn-delete">🗑️</button>
          </div>
        </div>
      `;
    });
    html += '</div>';

    content.innerHTML = html;
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

function loadGiocatoriList() {
  const content = document.getElementById('giocatori-content');
  if (!content) return;

  content.innerHTML = '<div>Caricamento giocatori...</div>';

  supabaseClient.from('giocatori').select('*').then(({ data, error }) => {
    if (error) {
      content.innerHTML = '<div style="color:red">Errore: ' + error.message + '</div>';
      return;
    }

    if (!data || data.length === 0) {
      content.innerHTML = '<div>Nessun giocatore trovato.</div>';
      return;
    }

    let html = '<div class="giocatori-list">';
    data.forEach(g => {
      const numeroText = g.numero_maglia ? `#${g.numero_maglia}` : 'N/A';
      const idoneitaIcon = g.idoneita_sportiva ? '✅' : '❌';
      const idoneitaText = g.idoneita_sportiva ? 'Idoneo' : 'Non Idoneo';

      html += `
        <div class="giocatore-card">
          <div class="giocatore-info">
            <strong>${numeroText} - ${g.nome} ${g.cognome}</strong><br>
            <small>Ruolo: ${g.ruolo || 'N/A'} | ${idoneitaIcon} ${idoneitaText}</small>
          </div>
          <div class="giocatore-actions">
            <button onclick="editGiocatore(${g.id})" class="btn-edit">✏️</button>
            <button onclick="deleteGiocatore(${g.id})" class="btn-delete">🗑️</button>
          </div>
        </div>
      `;
    });
    html += '</div>';

    content.innerHTML = html;
  });
}

function showAddGiocatoreForm() {
  showGiocatoreForm();
}

function editGiocatore(id) {
  // Prima carica i dati del giocatore
  supabaseClient.from('giocatori').select('*').eq('id', id).single().then(({ data, error }) => {
    if (error) {
      alert('Errore nel caricamento del giocatore: ' + error.message);
      return;
    }
    showGiocatoreForm(data);
  });
}

function showGiocatoreForm(giocatore = null) {
  const isEdit = giocatore !== null;
  const title = isEdit ? 'Modifica Giocatore' : 'Nuovo Giocatore';

  const formHtml = `
    <div id="giocatore-modal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>${title}</h3>
          <button onclick="closeModal()" class="btn-close">×</button>
        </div>
        <form id="giocatore-form" onsubmit="saveGiocatore(event, ${isEdit ? giocatore.id : 'null'})">
          <div class="form-group">
            <label for="nome">Nome:</label>
            <input type="text" id="nome" name="nome" required value="${giocatore?.nome || ''}">
          </div>
          <div class="form-group">
            <label for="cognome">Cognome:</label>
            <input type="text" id="cognome" name="cognome" required value="${giocatore?.cognome || ''}">
          </div>
          <div class="form-group">
            <label for="ruolo">Ruolo:</label>
            <select id="ruolo" name="ruolo">
              <option value="">Seleziona ruolo</option>
              <option value="Playmaker" ${giocatore?.ruolo === 'Playmaker' ? 'selected' : ''}>Playmaker</option>
              <option value="Guardia" ${giocatore?.ruolo === 'Guardia' ? 'selected' : ''}>Guardia</option>
              <option value="Ala" ${giocatore?.ruolo === 'Ala' ? 'selected' : ''}>Ala</option>
              <option value="Centro" ${giocatore?.ruolo === 'Centro' ? 'selected' : ''}>Centro</option>
            </select>
          </div>
          <div class="form-group">
            <label for="numero_maglia">Numero Maglia:</label>
            <input type="number" id="numero_maglia" name="numero_maglia" min="1" max="99" value="${giocatore?.numero_maglia || ''}">
          </div>
          <div class="form-group">
            <label for="anno_nascita">Anno Nascita:</label>
            <input type="number" id="anno_nascita" name="anno_nascita" min="1950" max="2010" value="${giocatore?.anno_nascita || ''}">
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" id="idoneita_sportiva" name="idoneita_sportiva" ${giocatore?.idoneita_sportiva ? 'checked' : ''}>
              Idoneità Sportiva
            </label>
          </div>
          <div class="form-group" id="data-scadenza-group" style="display: ${giocatore?.idoneita_sportiva ? 'block' : 'none'}">
            <label for="data_scadenza_idoneita">Data Scadenza Idoneità:</label>
            <input type="date" id="data_scadenza_idoneita" name="data_scadenza_idoneita" value="${giocatore?.data_scadenza_idoneita || ''}">
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-save">${isEdit ? 'Salva Modifiche' : 'Aggiungi Giocatore'}</button>
            <button type="button" onclick="closeModal()" class="btn-cancel">Annulla</button>
          </div>
        </form>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', formHtml);

  // Gestisci il toggle del campo data scadenza
  const idoneitaCheckbox = document.getElementById('idoneita_sportiva');
  const dataScadenzaGroup = document.getElementById('data-scadenza-group');

  idoneitaCheckbox.addEventListener('change', function() {
    dataScadenzaGroup.style.display = this.checked ? 'block' : 'none';
  });
}

function saveGiocatore(event, giocatoreId) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const giocatore = {
    nome: formData.get('nome'),
    cognome: formData.get('cognome'),
    ruolo: formData.get('ruolo'),
    numero_maglia: formData.get('numero_maglia') ? parseInt(formData.get('numero_maglia')) : null,
    anno_nascita: formData.get('anno_nascita') ? parseInt(formData.get('anno_nascita')) : null,
    idoneita_sportiva: formData.get('idoneita_sportiva') === 'on',
    data_scadenza_idoneita: formData.get('data_scadenza_idoneita') || null
  };

  const isEdit = giocatoreId !== null && giocatoreId !== 'null';

  if (isEdit) {
    // Aggiorna giocatore esistente
    supabaseClient.from('giocatori').update(giocatore).eq('id', giocatoreId).then(({ error }) => {
      if (error) {
        alert('Errore nell\'aggiornamento: ' + error.message);
      } else {
        alert('Giocatore aggiornato con successo!');
        closeModal();
        loadGiocatoriList();
      }
    });
  } else {
    // Crea nuovo giocatore
    supabaseClient.from('giocatori').insert([giocatore]).then(({ error }) => {
      if (error) {
        alert('Errore nell\'aggiunta: ' + error.message);
      } else {
        alert('Giocatore aggiunto con successo!');
        closeModal();
        loadGiocatoriList();
      }
    });
  }
}

function deleteGiocatore(id) {
  if (!confirm('Sei sicuro di voler eliminare questo giocatore?')) {
    return;
  }

  supabaseClient.from('giocatori').delete().eq('id', id).then(({ error }) => {
    if (error) {
      alert('Errore nell\'eliminazione: ' + error.message);
    } else {
      alert('Giocatore eliminato con successo!');
      loadGiocatoriList();
    }
  });
}

function showAddPartitaForm() {
  showPartitaForm();
}

function editPartita(id) {
  // Prima carica i dati della partita
  supabaseClient.from('partite').select('*').eq('id', id).single().then(({ data, error }) => {
    if (error) {
      alert('Errore nel caricamento della partita: ' + error.message);
      return;
    }
    showPartitaForm(data);
  });
}

function showPartitaForm(partita = null) {
  const isEdit = partita !== null;
  const title = isEdit ? 'Modifica Partita' : 'Nuova Partita';

  const formHtml = `
    <div id="partita-modal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>${title}</h3>
          <button onclick="closeModal()" class="btn-close">×</button>
        </div>
        <form id="partita-form" onsubmit="savePartita(event, ${isEdit ? partita.id : 'null'})">
          <div class="form-group">
            <label for="data">Data:</label>
            <input type="date" id="data" name="data" required value="${partita?.data || ''}">
          </div>
          <div class="form-group">
            <label for="ora">Ora:</label>
            <input type="time" id="ora" name="ora" value="${partita?.ora || ''}">
          </div>
          <div class="form-group">
            <label for="avversario">Avversario:</label>
            <input type="text" id="avversario" name="avversario" required value="${partita?.avversario || ''}">
          </div>
          <div class="form-group">
            <label for="luogo">Luogo:</label>
            <input type="text" id="luogo" name="luogo" placeholder="Palestra, indirizzo..." value="${partita?.luogo || ''}">
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" id="in_casa" name="in_casa" ${partita?.in_casa ? 'checked' : ''}>
              Partita in casa
            </label>
          </div>
          <div class="form-group">
            <label for="tipologia">Tipologia:</label>
            <select id="tipologia" name="tipologia">
              <option value="stagione regolare" ${partita?.tipologia === 'stagione regolare' ? 'selected' : ''}>Stagione Regolare</option>
              <option value="pre-stagione" ${partita?.tipologia === 'pre-stagione' ? 'selected' : ''}>Pre-stagione</option>
              <option value="post-stagione" ${partita?.tipologia === 'post-stagione' ? 'selected' : ''}>Post-stagione</option>
              <option value="tornei" ${partita?.tipologia === 'tornei' ? 'selected' : ''}>Tornei</option>
            </select>
          </div>
          <div class="form-group">
            <label for="risultato_nostro">Risultato Nostro:</label>
            <input type="number" id="risultato_nostro" name="risultato_nostro" min="0" value="${partita?.risultato_nostro || ''}">
          </div>
          <div class="form-group">
            <label for="risultato_avversario">Risultato Avversario:</label>
            <input type="number" id="risultato_avversario" name="risultato_avversario" min="0" value="${partita?.risultato_avversario || ''}">
          </div>
          <div class="form-group">
            <label for="note">Note:</label>
            <textarea id="note" name="note" rows="3">${partita?.note || ''}</textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-save">${isEdit ? 'Salva Modifiche' : 'Aggiungi Partita'}</button>
            <button type="button" onclick="closeModal()" class="btn-cancel">Annulla</button>
          </div>
        </form>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', formHtml);
}

function savePartita(event, partitaId) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const partita = {
    data: formData.get('data'),
    ora: formData.get('ora') || null,
    avversario: formData.get('avversario'),
    luogo: formData.get('luogo') || null,
    in_casa: formData.get('in_casa') === 'on',
    tipologia: formData.get('tipologia'),
    risultato_nostro: formData.get('risultato_nostro') ? parseInt(formData.get('risultato_nostro')) : null,
    risultato_avversario: formData.get('risultato_avversario') ? parseInt(formData.get('risultato_avversario')) : null,
    note: formData.get('note') || null
  };

  const isEdit = partitaId !== null && partitaId !== 'null';

  if (isEdit) {
    // Aggiorna partita esistente
    supabaseClient.from('partite').update(partita).eq('id', partitaId).then(({ error }) => {
      if (error) {
        alert('Errore nell\'aggiornamento: ' + error.message);
      } else {
        alert('Partita aggiornata con successo!');
        closeModal();
        filtraPartite(document.getElementById('filtro-tipologia').value);
      }
    });
  } else {
    // Crea nuova partita
    supabaseClient.from('partite').insert([partita]).then(({ error }) => {
      if (error) {
        alert('Errore nell\'aggiunta: ' + error.message);
      } else {
        alert('Partita aggiunta con successo!');
        closeModal();
        filtraPartite(document.getElementById('filtro-tipologia').value);
      }
    });
  }
}

function deletePartita(id) {
  if (!confirm('Sei sicuro di voler eliminare questa partita?')) {
    return;
  }

  supabaseClient.from('partite').delete().eq('id', id).then(({ error }) => {
    if (error) {
      alert('Errore nell\'eliminazione: ' + error.message);
    } else {
      alert('Partita eliminata con successo!');
      filtraPartite(document.getElementById('filtro-tipologia').value);
    }
  });
}

function showAddAllenamentoForm() {
  showAllenamentoForm();
}

function editAllenamento(id) {
  // Prima carica i dati dell'allenamento
  supabaseClient.from('allenamenti').select('*').eq('id', id).single().then(({ data, error }) => {
    if (error) {
      alert('Errore nel caricamento dell\'allenamento: ' + error.message);
      return;
    }
    showAllenamentoForm(data);
  });
}

function showAllenamentoForm(allenamento = null) {
  const isEdit = allenamento !== null;
  const title = isEdit ? 'Modifica Allenamento' : 'Nuovo Allenamento';

  const formHtml = `
    <div id="allenamento-modal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>${title}</h3>
          <button onclick="closeModal()" class="btn-close">×</button>
        </div>
        <form id="allenamento-form" onsubmit="saveAllenamento(event, ${isEdit ? allenamento.id : 'null'})">
          <div class="form-group">
            <label for="data">Data:</label>
            <input type="date" id="data" name="data" required value="${allenamento?.data || ''}">
          </div>
          <div class="form-group">
            <label for="ora">Ora:</label>
            <input type="time" id="ora" name="ora" value="${allenamento?.ora || ''}">
          </div>
          <div class="form-group">
            <label for="luogo">Luogo:</label>
            <input type="text" id="luogo" name="luogo" required placeholder="Palestra, indirizzo..." value="${allenamento?.luogo || ''}">
          </div>
          <div class="form-group">
            <label for="note">Note:</label>
            <textarea id="note" name="note" rows="3" placeholder="Note sull'allenamento...">${allenamento?.note || ''}</textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-save">${isEdit ? 'Salva Modifiche' : 'Aggiungi Allenamento'}</button>
            <button type="button" onclick="closeModal()" class="btn-cancel">Annulla</button>
          </div>
        </form>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', formHtml);
}

function saveAllenamento(event, allenamentoId) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const allenamento = {
    data: formData.get('data'),
    ora: formData.get('ora') || null,
    luogo: formData.get('luogo'),
    note: formData.get('note') || null
  };

  const isEdit = allenamentoId !== null && allenamentoId !== 'null';

  if (isEdit) {
    // Aggiorna allenamento esistente
    supabaseClient.from('allenamenti').update(allenamento).eq('id', allenamentoId).then(({ error }) => {
      if (error) {
        alert('Errore nell\'aggiornamento: ' + error.message);
      } else {
        alert('Allenamento aggiornato con successo!');
        closeModal();
        loadAllenamentiList();
      }
    });
  } else {
    // Crea nuovo allenamento
    supabaseClient.from('allenamenti').insert([allenamento]).then(({ error }) => {
      if (error) {
        alert('Errore nell\'aggiunta: ' + error.message);
      } else {
        alert('Allenamento aggiunto con successo!');
        closeModal();
        loadAllenamentiList();
      }
    });
  }
}

function deleteAllenamento(id) {
  if (!confirm('Sei sicuro di voler eliminare questo allenamento?')) {
    return;
  }

  supabaseClient.from('allenamenti').delete().eq('id', id).then(({ error }) => {
    if (error) {
      alert('Errore nell\'eliminazione: ' + error.message);
    } else {
      alert('Allenamento eliminato con successo!');
      loadAllenamentiList();
    }
  });
}

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

function closeModal() {
  const modals = ['giocatore-modal', 'partita-modal', 'allenamento-modal'];
  modals.forEach(modalId => {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.remove();
    }
  });
}

console.log('app.js fully loaded');
