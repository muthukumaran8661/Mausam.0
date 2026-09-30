/**
 * Mausam Service Worker
 * Strategy:
 * - App Shell assets: Cache-First with background revalidation
 * - Weather & Data API (/api/*): Network-First with Cache fallback
 * - Navigation fallback: Offline page
 */

const CACHE_NAME = 'mausam-v1.0.0';
const APP_SHELL = [
  '/',
  '/static/styles.css',
  '/static/app.js',
  '/static/manifest.js',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
  '/static/icons/icon.svg',
  '/static/offline.html'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Mausam SW] Pre-caching App Shell assets');
      return cache.addAll(APP_SHELL);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[Mausam SW] Removing old cache version:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);

  // Strategy 1: API requests (/api/*) -> Network-First, fallback to Cache
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(request).then((cachedResponse) => {
            if (cachedResponse) {
              return cachedResponse;
            }
            // Return synthetic offline JSON if no cache exists
            return new Response(
              JSON.stringify({
                is_offline: true,
                freshness_text: 'Offline mode',
                detail: 'Device is offline and no cached weather data is available.'
              }),
              {
                headers: { 'Content-Type': 'application/json' },
                status: 200
              }
            );
          });
        })
    );
    return;
  }

  // Strategy 2: HTML Navigation -> Network-first with offline.html fallback
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .catch(() => {
          return caches.match('/static/offline.html').then((offlineResp) => {
            return offlineResp || caches.match('/');
          });
        })
    );
    return;
  }

  // Strategy 3: App shell static files -> Cache-First
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        // Asynchronously update in background
        fetch(request).then((freshResponse) => {
          if (freshResponse && freshResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => cache.put(request, freshResponse));
          }
        }).catch(() => {});
        return cachedResponse;
      }
      return fetch(request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const clone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
        }
        return networkResponse;
      });
    })
  );
});
