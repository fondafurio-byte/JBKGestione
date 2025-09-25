const CACHE_NAME = 'jbkgestione-cache-v4';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/static/style.css?v=4',
  '/static/icon-192.png',
  '/static/icon-512.png',
  '/static/supabase.min.js?v=4',
  '/app.js?v=4'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
