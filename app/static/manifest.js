/**
 * Mausam PWA Manifest & Service Worker Registration Script
 * - Injects a valid Web App Manifest via <link rel="manifest"> pointing to /static/manifest.json
 * - Handles the beforeinstallprompt event to show an in-app Install button
 * - Registers the Service Worker for offline support
 */

(function () {
  'use strict';

  /* ─── 1. Inject <link rel="manifest"> pointing to static JSON ─── */
  (function injectManifestLink() {
    let link = document.querySelector('link[rel="manifest"]');
    if (!link) {
      link = document.createElement('link');
      link.rel = 'manifest';
      document.head.appendChild(link);
    }
    link.href = '/static/manifest.json';
  })();

  /* ─── 2. PWA Install Prompt ─── */
  let deferredInstallPrompt = null;

  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredInstallPrompt = e;

    // Show the install button if it exists in the DOM
    const installBtn = document.getElementById('pwa-install-btn');
    if (installBtn) {
      installBtn.style.display = 'flex';
    }
    console.log('[Mausam PWA] Install prompt ready.');
  });

  // Called by the install button's onclick
  window.triggerPwaInstall = async function () {
    if (!deferredInstallPrompt) {
      alert('App is already installed or your browser does not support installation.');
      return;
    }
    deferredInstallPrompt.prompt();
    const { outcome } = await deferredInstallPrompt.userChoice;
    console.log('[Mausam PWA] Install outcome:', outcome);
    deferredInstallPrompt = null;

    const installBtn = document.getElementById('pwa-install-btn');
    if (installBtn) installBtn.style.display = 'none';
  };

  // Hide install button once app is installed
  window.addEventListener('appinstalled', () => {
    console.log('[Mausam PWA] App installed successfully.');
    const installBtn = document.getElementById('pwa-install-btn');
    if (installBtn) installBtn.style.display = 'none';
    deferredInstallPrompt = null;
  });

  /* ─── 3. Register Service Worker ─── */
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker
        .register('/static/service-worker.js', { scope: '/' })
        .then((reg) => {
          console.log('[Mausam PWA] Service Worker registered. Scope:', reg.scope);

          // Check for updates every 60 seconds
          setInterval(() => reg.update(), 60000);
        })
        .catch((err) => {
          console.warn('[Mausam PWA] Service Worker registration failed:', err);
        });
    });
  }
})();
