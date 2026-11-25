const CACHE_NAME = 'see3gre-pwa-v16';

const ASSETS_ESSENCIAIS = [
    '/',
    '/sobre',
    '/servicos',
    '/noticias',
    '/transparencia',
    '/contato',
    '/nudea',
    '/quadro',
    '/nutci',
    '/static/css/main.css?v=2',
    '/static/js/main.js?v=2',
    '/static/js/subportal_auto.js?v=1',
    '/static/img/icon-3gre.svg',
    '/static/img/icon-3gre-180.png',
    '/static/img/icon-3gre-192.png',
    '/static/img/icon-3gre-512.png',
    '/static/img/cabecalho_abaixo.png'
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

    // Nunca cacheia a API dinâmica de módulos para novos botões aparecerem na hora
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(fetch(event.request));
        return;
    }

    // Cache dinâmico automático para qualquer imagem ou asset em /static/
    if (url.pathname.startsWith('/static/')) {
        event.respondWith(
            caches.match(event.request).then((cached) => {
                if (cached) return cached;
                return fetch(event.request).then((networkResp) => {
                    if (networkResp && networkResp.status === 200) {
                        const clone = networkResp.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                    }
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