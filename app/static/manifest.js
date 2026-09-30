/**
 * Mausam PWA Manifest & Service Worker Registration Script
 * Generates the web app manifest dynamically via Blob URL and registers the Service Worker.
 */

(function () {
  'use strict';

  const manifestData = {
    name: 'Mausam - Personalized Weather',
    short_name: 'Mausam',
    description: 'Personalized mobile-first weather application with human-centric insights',
    start_url: '/',
    scope: '/',
    display: 'standalone',
    orientation: 'portrait-primary',
    theme_color: '#1E88E5',
    background_color: '#0B1E3F',
    icons: [
      {
        src: '/static/icons/icon-192.png',
        sizes: '192x192',
        type: 'image/png',
        purpose: 'any'
      },
      {
        src: '/static/icons/icon-512.png',
        sizes: '512x512',
        type: 'image/png',
        purpose: 'any'
      },
      {
        src: '/static/icons/icon-maskable.png',
        sizes: '512x512',
        type: 'image/png',
        purpose: 'maskable'
      }
    ],
    shortcuts: [
      {
        name: 'Today',
        short_name: 'Today',
        description: "View today's weather and hero overview",
        url: '/#hero',
        icons: [{ src: '/static/icons/icon-192.png', sizes: '192x192' }]
      },
      {
        name: 'Alerts',
        short_name: 'Alerts',
        description: 'Check active severe weather warnings',
        url: '/#alerts',
        icons: [{ src: '/static/icons/icon-192.png', sizes: '192x192' }]
      },
      {
        name: 'Saved Cities',
        short_name: 'Cities',
        description: 'Manage and compare your saved locations',
        url: '/#saved-cities',
        icons: [{ src: '/static/icons/icon-192.png', sizes: '192x192' }]
      }
    ]
  };

  // Convert manifest object to Blob and inject <link rel="manifest">
  try {
    const stringManifest = JSON.stringify(manifestData);
    const blob = new Blob([stringManifest], { type: 'application/json' });
    const manifestURL = URL.createObjectURL(blob);

    let manifestLink = document.querySelector('link[rel="manifest"]');
    if (!manifestLink) {
      manifestLink = document.createElement('link');
      manifestLink.rel = 'manifest';
      document.head.appendChild(manifestLink);
    }
    manifestLink.href = manifestURL;
  } catch (err) {
    console.warn('[Mausam PWA] Could not inject dynamic manifest blob:', err);
  }

  // Register Service Worker
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker
        .register('/static/service-worker.js', { scope: '/' })
        .then((reg) => {
          console.log('[Mausam PWA] Service Worker registered with scope:', reg.scope);
        })
        .catch((err) => {
          console.warn('[Mausam PWA] Service Worker registration failed:', err);
        });
    });
  }
})();
