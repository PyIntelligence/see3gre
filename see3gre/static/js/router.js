/**
 * Router Module - Portal Central SEE3GRE
 * Gerencia a navegação e roteamento entre o Hub Central, Subportais e Satélites.
 */

export class Router {
    constructor() {
        this.init();
    }

    /**
     * Inicializa os ouvintes de eventos de navegação
     */
    init() {
        // Intercepta cliques em elementos com o atributo 'data-link'
        document.addEventListener('click', (e) => {
            const target = e.target.closest('[data-link]');
            if (target) {
                e.preventDefault();
                const destination = target.getAttribute('href') || target.dataset.url;
                this.navigate(destination);
            }
        });
    }

    /**
     * Executa o redirecionamento com suporte a links internos, proxies e externos
     * @param {string} url - URL ou rota de destino
     * @param {boolean} forceNewTab - Força abertura em nova aba
     */
    navigate(url, forceNewTab = false) {
        if (!url) return;

        const isExternal = url.startsWith('http://') || url.startsWith('https://');

        if (forceNewTab || isExternal) {
            window.open(url, '_blank', 'noopener,noreferrer');
            return;
        }

        window.location.href = url;
    }

    /**
     * Utilitário para extrair parâmetros de busca da URL (útil para tokens de autenticação SSO)
     * @param {string} paramName - Nome da variável na URL (ex: ?token=xyz)
     * @returns {string|null}
     */
    getQueryParam(paramName) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(paramName);
    }
}

// Instância única para reutilização nos scripts das páginas
export const router = new Router();