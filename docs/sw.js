/* The Big Prompt Library — service worker (Q4.6 PWA) */
const CACHE_VERSION = 'tbpl-v1';
const RAW_PREFIX    = 'https://raw.githubusercontent.com/Yuuqq/TheBigPromptLibrary/main/';

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_VERSION).map(k => caches.delete(k)))
        ).then(() => self.clients.claim())
    );
});

/**
 * Strategy:
 *   - Same-origin GETs (HTML/CSS/JS at the Pages domain): cache-first then update in background
 *   - GitHub raw markdown + index JSON: stale-while-revalidate (network preferred, cache fallback)
 *   - GitHub API (api.github.com): network only (rate-limited & dynamic)
 *   - Other origins (CDN libs): cache-first
 */
self.addEventListener('fetch', (event) => {
    const req = event.request;
    if (req.method !== 'GET') return;
    const url = new URL(req.url);

    if (url.hostname === 'api.github.com') {
        return; // network-only
    }

    if (url.href.startsWith(RAW_PREFIX)) {
        event.respondWith(staleWhileRevalidate(req));
        return;
    }

    if (url.origin === self.location.origin) {
        event.respondWith(cacheFirst(req));
        return;
    }

    // Third-party CDNs (jsdelivr, fonts)
    event.respondWith(cacheFirst(req));
});

async function cacheFirst(req) {
    const cache = await caches.open(CACHE_VERSION);
    const cached = await cache.match(req);
    if (cached) return cached;
    try {
        const fresh = await fetch(req);
        if (fresh.ok && (req.url.startsWith('http://') || req.url.startsWith('https://'))) {
            cache.put(req, fresh.clone()).catch(() => {});
        }
        return fresh;
    } catch (e) {
        if (cached) return cached;
        throw e;
    }
}

async function staleWhileRevalidate(req) {
    const cache = await caches.open(CACHE_VERSION);
    const cached = await cache.match(req);
    const fetchPromise = fetch(req).then(fresh => {
        if (fresh.ok) cache.put(req, fresh.clone()).catch(() => {});
        return fresh;
    }).catch(() => cached);
    return cached || fetchPromise;
}
