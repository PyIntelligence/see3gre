document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.querySelector('[data-nucleo-grid]');
    if (!grid) return;

    const nucleo = grid.getAttribute('data-nucleo-grid');

    try {
        const resposta = await fetch(`/api/modulos/${encodeURIComponent(nucleo)}`, {
            cache: 'no-store'
        });
        if (!resposta.ok) return;

        const modulos = await resposta.json();
        grid.innerHTML = '';

        modulos.forEach((modulo) => {
            const card = document.createElement('a');
            card.className = modulo.cardClass || 'module-card';
            card.href = modulo.url;
            card.title = modulo.title;

            if (modulo.url.startsWith('http://') || modulo.url.startsWith('https://')) {
                card.target = '_blank';
                card.rel = 'noopener noreferrer';
            }

            if (modulo.showTitle) {
                card.innerHTML = `
                    <img src="${modulo.icon}" alt="${modulo.title}">
                    <span>${modulo.title}</span>
                `;
            } else {
                card.innerHTML = `
                    <img src="${modulo.icon}" alt="${modulo.title}">
                `;
            }

            grid.appendChild(card);
        });
    } catch (erro) {
        console.error('Erro ao carregar módulos do núcleo:', erro);
    }
});