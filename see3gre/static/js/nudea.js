// const nudeaModules = [
//     {
//         id: 'quadro-escolar',
//         title: 'Quadro Escolar',
//         icon: '/static/img/quadro.png',
//         url: 'https://quadro-escolar.onrender.com' 
//     },
//     {
//         id: 'outro-servico-nudea',
//         title: 'Outro Módulo NUDEA',
//         icon: '/static/img/servico.png',
//         url: '/spokes/nudea_servico/'
//     }
// ];

const nudeaModules = [
    {
        id: 'quadro-escolar',
        title: 'Quadro Escolar',
        icon: '/static/img/quadro.png',
        url: 'quadro.html' // <-- Alterado: Agora aponta para a página interna do Iframe
    },
    {
        id: 'outro-servico-nudea',
        title: 'Outro Módulo NUDEA',
        icon: '/static/img/servico.png',
        url: '/spokes/nudea_servico/'
    }
];

document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('nudea-modules-grid');
    if (!grid) return;

    nudeaModules.forEach(module => {
        const card = document.createElement('a');
        card.className = 'module-card';
        card.href = module.url;

        // Abre links externos (Render) em nova aba
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
});