const CACHE_NAME = 'see3gre-pwa-v11';

const ASSETS_ESSENCIAIS = [
    '/',
    '/sobre',
    '/servicos',
    '/noticias',
    '/transparencia',
    '/contato',
    '/nudea',
    '/nutci',
    '/static/css/main.css?v=2',
    '/static/js/main.js?v=2',
    '/static/js/nutci.js',
    '/static/img/icon-3gre.svg',
    '/static/img/icon-3gre-180.png',
    '/static/img/icon-3gre-192.png',
    '/static/img/icon-3gre-512.png',
    '/static/img/cabecalho_abaixo.png',
    '/static/img/nudea.png',
    '/static/img/nuafs.png',
    '/static/img/nucom.png',
    '/static/img/nudpe.png',
    '/static/img/nutci.png',
    '/static/img/nudea/quadros_escolas.png',
    '/static/img/nutci/relatorio-nutci.png'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_ESSENCIAIS))
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(
                keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
            )
        )
    );
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;

    const url = new URL(event.request.url);
    if (url.origin !== self.location.origin) return;

    if (url.pathname.startsWith('/static/')) {
        event.respondWith(
            caches.match(event.request).then((cached) => {
                return cached || fetch(event.request).then((networkResp) => {
                    const clone = networkResp.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                    return networkResp;
                });
            })
        );
        return;
    }

    event.respondWith(
        fetch(event.request)
            .then((networkResp) => {
                const clone = networkResp.clone();
                caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                return networkResp;
            })
            .catch(() => caches.match(event.request))
    );
});