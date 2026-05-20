const CACHE_NAME = 'portal-biblia-v1';
const ASSETS = [
  '/',
  '/templates/index.html',
  '/static/css/style.css',
  '/static/js/app.js',
  '/manifest.json'
];

// Instalação do Service Worker e Cache dos arquivos estáticos básicos
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS);
    })
  );
});

// Ativação e limpeza de caches antigos
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      );
    })
  );
});

// Estratégia de Cache: Network First (Tenta buscar atualizações na rede, se falhar usa o Cache)
self.addEventListener('fetch', event => {
  // Ignora requisições de API para não travar os dados dinâmicos do backend
  if (event.request.url.includes('/api/')) {
    return;
  }

  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.match(event.request);
    })
  );
});