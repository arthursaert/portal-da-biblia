const CACHE_NAME = 'portal-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/static/css/style.css',
  '/static/js/app.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      // O 'addAll' é o ponto crítico. Se UM desses arquivos falhar, tudo falha.
      return cache.addAll(ASSETS);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});