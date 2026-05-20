const CACHE_NAME = 'portal-biblia-v1';
const ASSETS = [
  '/',
  '/templates/index.html',
  '/static/css/style.css',
  '/static/js/app.js',
  '/manifest.json',
  '/api/livros'
];

// Instalação: Salva os arquivos estruturais no cache
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// Ativação: Limpa caches antigos
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Estratégia Stale-While-Revalidate: Carrega do cache instantaneamente, mas atualiza por trás
self.addEventListener('fetch', (e) => {
  // Ignora requisições do browser (extensões, etc)
  if (!e.request.url.startsWith(self.location.origin)) return;

  e.respondWith(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.match(e.request).then((cachedResponse) => {
        const fetchedResponse = fetch(e.request).then((networkResponse) => {
          // Salva uma cópia da nova resposta no cache (inclusive as rotas da API)
          if (networkResponse.status === 200) {
            cache.put(e.request, networkResponse.clone());
          }
          return networkResponse;
        }).catch(() => {
          // Se falhar a rede (tiver offline), retorna o que estiver no cache
          return cachedResponse;
        });

        return cachedResponse || fetchedResponse;
      });
    })
  );
});