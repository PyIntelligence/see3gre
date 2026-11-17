// Lista de núcleos e módulos acessíveis a partir do Portal Central Hub (SEE3GRE)
const modules = [
    {
        id: 'nudea-subportal',
        title: 'NUDEA - Núcleo de Desenvolvimento da Escola e da Aprendizagem',
        icon: '/static/img/nudea.jpeg',
        url: 'nudea.html'
    },
    {
        id: 'nuafs-modulo',
        title: 'NUAFS - Núcleo Administrativo Financeiro Suprimento e Logística',
        icon: '/static/img/nuafs.jpeg',
        url: '/spokes/nuafs/'
    },
    {
        id: 'nucom-modulo',
        title: 'NUCOM - Núcleo de Comunicação',
        icon: '/static/img/nucom.jpeg',
        url: '/spokes/nucom/'
    },
    {
        id: 'nudpe-modulo',
        title: 'NUDPE - Núcleo de Desenvolvimento e Protagonismo Estudantil',
        icon: '/static/img/nudpe.jpeg',
        url: '/spokes/nudpe/'
    },
    {
        id: 'nutci-modulo',
        title: 'NUTCI - Núcleo de Tecnologia, Ciência e Informação',
        icon: '/static/img/nutci.jpeg',
        url: '/spokes/nutci/'
    }
];

document.addEventListener('DOMContentLoaded', () => {
    // Captura opcional de token SSO via URL, caso seja enviado na autenticação
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (token) {
        localStorage.setItem('sso_token', token);
    }

    const grid = document.getElementById('modules-grid');
    if (!grid) return;

    // Renderização dinâmica dos cards dos núcleos no grid
    modules.forEach(module => {
        const card = document.createElement('a');
        card.className = 'module-card';
        card.href = module.url;
        card.title = module.title;

        // Caso a URL seja externa (começando com http), abre em nova aba
        if (module.url.startsWith('http://') || module.url.startsWith('https://')) {
            card.target = '_blank';
            card.rel = 'noopener noreferrer';
        }

        // Como as artes .jpeg já contêm o título e o botão "Acessar", renderizamos apenas a imagem
        card.innerHTML = `
            <img src="${module.icon}" alt="${module.title}">
        `;
        grid.appendChild(card);
    });

    // Evento de Logout para a barra superior (caso esteja presente no HTML)
    const btnLogout = document.getElementById('btn-logout');
    if (btnLogout) {
        btnLogout.addEventListener('click', () => {
            localStorage.removeItem('sso_token');
            console.log('Sessão encerrada.');
            window.location.reload();
        });
    }
});