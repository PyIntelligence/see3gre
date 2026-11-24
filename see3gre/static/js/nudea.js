// Lista de módulos e sistemas acessíveis a partir do Subportal NUDEA
const nudeaModules = [
    {
        id: 'quadro-escolar',
        title: 'Quadro Escolar',
        icon: '/static/img/nudea/quadros_escolares.png',
        url: 'quadro.html'
    },
    {
        id: 'outro-servico-nudea',
        title: 'Outro Módulo NUDEA',
        url: '/spokes/nudea_servico/',
        svg: `<svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#004085" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>`
    }
];

document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('nudea-modules-grid');
    if (!grid) return;

    nudeaModules.forEach(module => {
        const card = document.createElement('a');
        card.className = 'sub-module-card';
        card.href = module.url;
        card.title = module.title;

        // Abre links externos em nova aba, caso algum módulo futuro aponte direto para fora
        if (module.url.startsWith('http://') || module.url.startsWith('https://')) {
            card.target = '_blank';
            card.rel = 'noopener noreferrer';
        }

        // Prioriza a imagem .png quando "icon" estiver definido; caso contrário, usa o SVG
        const visualIcon = module.icon
            ? `<img src="${module.icon}" alt="${module.title}" style="width: 88px; height: 88px; object-fit: contain; border-radius: 12px;">`
            : (module.svg || '');

        card.innerHTML = `
            ${visualIcon}
            <span>${module.title}</span>
        `;
        grid.appendChild(card);
    });
});