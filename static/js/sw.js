// Apenas um console.log para saber se ele carregou
console.log("Service Worker carregado com sucesso");

self.addEventListener('install', (event) => {
  // Nada de cache, nada de network, nada de erro possível
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(clients.claim());
});222