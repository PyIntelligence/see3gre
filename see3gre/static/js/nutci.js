// Lista de módulos e sistemas acessíveis a partir do Subportal NUTCI
const nutciModules = [
    {
        id: 'nutci-relatorio-projeto',
        title: 'Relatório de Projeto - NUTCI',
        icon: '/static/img/nutci/relatorio-nutci.png',
        url: 'https://makers-bonds-lap-carries.trycloudflare.com/'
    }
];

document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('nutci-modules-grid');
    if (!grid) return;

    nutciModules.forEach(module => {
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