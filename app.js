// Configurazione Supabase
const SUPABASE_URL = 'https://hnmzfyzlyadsflhjwsgu.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhubXpmeXpseWFkc2ZsaGp3c2d1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2NDMyMzIsImV4cCI6MjA3NDIxOTIzMn0.CxnEYe-1h2LZkfWwm0ZVJGhzFLWJOyBUAC5djVIwQHA';
const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

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
  // Login con Supabase
  const { data, error } = await supabase.auth.signInWithPassword({
    email: username,
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
  await supabase.auth.signOut();
  dashboardSection.style.display = 'none';
  loginSection.style.display = 'block';
});

// Carica dati dashboard
async function loadDashboard() {
  const dashboardContent = document.getElementById('dashboard-content');
  dashboardContent.textContent = 'Caricamento...';
  // Esempio: fetch dati partite
  const { data, error } = await supabase.from('partite').select('*');
  if (error) {
    dashboardContent.textContent = 'Errore: ' + error.message;
  } else {
    dashboardContent.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
  }
}

// Service Worker per PWA
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('service-worker.js');
  });
}
