const CACHE_NAME = 'see3gre-pwa-v1';

const ASSETS_ESSENCIAIS = [
    '/',
    '/sobre',
    '/servicos',
    '/noticias',
    '/transparencia',
    '/contato',
    '/static/css/main.css',
    '/static/js/main.js',
    '/static/img/icon-3gre.svg',
    '/static/img/icon-3gre-maskable.svg',
    '/static/img/cabecalho_abaixo.png',
    '/static/img/nudea.png',
    '/static/img/nuafs.png',
    '/static/img/nucom.png',
    '/static/img/nudpe.png',
    '/static/img/nutci.png'
];

// Instalação: guarda os arquivos base no cache
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_ESSENCIAIS))
    );
    self.skipWaiting();
});

// Ativação: remove versões antigas do cache
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

// Interceptação de requisições
self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;

    const url = new URL(event.request.url);
    if (url.origin !== self.location.origin) return;

    // Arquivos estáticos (/static/): Cache-First para abrir instantaneamente
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

    // Páginas HTML e API: Network-First com fallback para cache offline
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