const CACHE_NAME = 'jbkgestione-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/static/style.css',
  '/static/icon-192.png',
  '/static/icon-512.png',
  '/app.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
