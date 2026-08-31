const CACHE_NAME = 'lpu-examprep-v1';
const ASSETS = [
  '/',
  '/static/css/styles.css',
  '/static/js/app.js',
  '/static/js/api.js',
  '/static/js/components.js',
  '/static/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      return cachedResponse || fetch(event.request);
    })
  );
});
