// Lista de módulos e sistemas acessíveis a partir do Portal Central Hub
const modules = [
    {
        id: 'nudea-subportal',
        title: 'Subportal NUDEA',
        icon: '/static/img/nudea.png',
        url: 'nudea.html'
    },
    {
        id: 'pwa-area-1',
        title: 'Área Operacional (PWA)',
        icon: '/static/img/operacional.png',
        url: '/spokes/pwa_area_1/'
    },
    {
        id: 'pwa-area-2',
        title: 'Gestão Financeira (PWA)',
        icon: '/static/img/financeiro.png',
        url: '/spokes/pwa_area_2/'
    },
    {
        id: 'powerbi-dashboard',
        title: 'Painel Power BI',
        icon: '/static/img/powerbi.png',
        url: '/spokes/powerbi_service/dashboard'
    }
];

document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('modules-grid');
    if (!grid) return;

    // Renderização dinâmica dos botões/cards no grid
    modules.forEach(module => {
        const card = document.createElement('a');
        card.className = 'module-card';
        card.href = module.url;

        // Caso a URL seja externa (começando com http), abre em nova aba
        if (module.url.startsWith('http://') || module.url.startsWith('https://')) {
            card.target = '_blank';
            card.rel = 'noopener noreferrer';
        }

        card.innerHTML = `
            <img src="${module.icon}" alt="${module.title}" onerror="this.src='https://via.placeholder.com/64?text=Ícone'">
            <span>${module.title}</span>
        `;
        grid.appendChild(card);
    });

    // Evento de Logout para a barra superior
    const btnLogout = document.getElementById('btn-logout');
    if (btnLogout) {
        btnLogout.addEventListener('click', () => {
            // Lógica para encerramento de sessão (ex: remoção de token SSO)
            console.log('Sessão encerrada.');
            window.location.reload();
        });
    }
});