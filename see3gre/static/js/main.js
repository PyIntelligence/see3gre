// Lista de núcleos e módulos acessíveis a partir do Portal Central Hub (SEE3GRE)
const modules = [
    {
        id: 'nudea-subportal',
        title: 'NUDEA - Núcleo de Desenvolvimento da Escola e da Aprendizagem',
        icon: '/static/img/nudea.png',
        url: '/nudea'
    },
    {
        id: 'nuafs-modulo',
        title: 'NUAFS - Núcleo Administrativo Financeiro Suprimento e Logística',
        icon: '/static/img/nuafs.png',
        url: '/spokes/nuafs/'
    },
    {
        id: 'nucom-modulo',
        title: 'NUCOM - Núcleo de Comunicação',
        icon: '/static/img/nucom.png',
        url: '/spokes/nucom/'
    },
    {
        id: 'nudpe-modulo',
        title: 'NUDPE - Núcleo de Desenvolvimento e Protagonismo Estudantil',
        icon: '/static/img/nudpe.png',
        url: '/spokes/nudpe/'
    },
    {
        id: 'nutci-subportal',
        title: 'NUTCI - Núcleo de Tecnologia, Ciência e Informação',
        icon: '/static/img/nutci.png',
        url: '/nutci'
    }
];

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (token) {
        localStorage.setItem('sso_token', token);
    }

    const grid = document.getElementById('modules-grid');
    if (!grid) return;

    modules.forEach(module => {
        const card = document.createElement('a');
        card.className = 'module-card';
        card.href = module.url;
        card.title = module.title;

        if (module.url.startsWith('http://') || module.url.startsWith('https://')) {
            card.target = '_blank';
            card.rel = 'noopener noreferrer';
        }

        card.innerHTML = `
            <img src="${module.icon}" alt="${module.title}">
        `;
        grid.appendChild(card);
    });
});