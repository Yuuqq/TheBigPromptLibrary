/* The Big Prompt Library — service worker (Q4.6 PWA)
 *
 * Cache strategy (post-review hardening):
 *   - Same-origin HTML/JS/CSS (the app shell): NETWORK-FIRST with cache fallback.
 *     Avoids users getting stuck on stale builds after a deploy.
 *   - GitHub raw markdown + index JSON: stale-while-revalidate (cached UI loads
 *     instantly; next navigation sees fresh data).
 *   - GitHub API (api.github.com): network-only (rate-limited & dynamic).
 *   - Third-party CDNs (jsdelivr, fonts): cache-first (immutable URLs).
 *
 * Cache versioning:
 *   CACHE_VERSION is bumped manually when shipping a breaking SW change.
 *   For day-to-day deploys we don't need to bump it because same-origin is now
 *   network-first — the cache is just a fallback for offline use.
 */
const CACHE_VERSION = 'tbpl-v2';
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

self.addEventListener('fetch', (event) => {
    const req = event.request;
    if (req.method !== 'GET') return;
    let url;
    try { url = new URL(req.url); } catch (e) { return; }

    if (url.hostname === 'api.github.com') {
        return; // network-only
    }

    if (url.href.startsWith(RAW_PREFIX)) {
        event.respondWith(staleWhileRevalidate(req));
        return;
    }

    if (url.origin === self.location.origin) {
        // Network-first so deploys land immediately for returning users.
        event.respondWith(networkFirst(req));
        return;
    }

    // Third-party CDNs (jsdelivr, fonts): immutable, safe to cache-first.
    event.respondWith(cacheFirst(req));
});

async function networkFirst(req) {
    const cache = await caches.open(CACHE_VERSION);
    try {
        const fresh = await fetch(req);
        if (fresh && fresh.ok && (req.url.startsWith('http://') || req.url.startsWith('https://'))) {
            cache.put(req, fresh.clone()).catch(() => {});
        }
        return fresh;
    } catch (e) {
        const cached = await cache.match(req);
        if (cached) return cached;
        throw e;
    }
}

async function cacheFirst(req) {
    const cache = await caches.open(CACHE_VERSION);
    const cached = await cache.match(req);
    if (cached) return cached;
    try {
        const fresh = await fetch(req);
        if (fresh && fresh.ok && (req.url.startsWith('http://') || req.url.startsWith('https://'))) {
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
        if (fresh && fresh.ok) cache.put(req, fresh.clone()).catch(() => {});
        return fresh;
    }).catch(() => cached);
    return cached || fetchPromise;
}
