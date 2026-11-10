const modules = [
    {
        id: 'pwa-area-1',
        title: 'Área Operacional (PWA)',
        icon: 'assets/icons/operacional.png',
        url: '/spokes/pwa_area_1/'
    },
    {
        id: 'pwa-area-2',
        title: 'Gestão Financeira (PWA)',
        icon: 'assets/icons/financeiro.png',
        url: '/spokes/pwa_area_2/'
    },
    {
        id: 'powerbi-dashboard',
        title: 'Painel Power BI',
        icon: 'assets/icons/powerbi.png',
        url: '/spokes/powerbi_service/dashboard'
    }
];

document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('modules-grid');
    
    modules.forEach(module => {
        const card = document.createElement('a');
        card.className = 'module-card';
        card.href = module.url;
        card.innerHTML = `
            <img src="${module.icon}" alt="${module.title}">
            <span>${module.title}</span>
        `;
        grid.appendChild(card);
    });
});