import os
import sys
from flask import Flask, jsonify, render_template, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists('/app/templates'):
    TEMPLATE_DIR = '/app/templates'
    STATIC_DIR = '/app/static'
    API_DIR = '/app/api'
else:
    TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'see3gre', 'templates'))
    STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'see3gre', 'static'))
    API_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'see3gre', 'api'))

if API_DIR not in sys.path:
    sys.path.insert(0, API_DIR)

from noticias_service import obter_noticias_automaticas

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path='/static'
)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', active_page='inicio')

@app.route('/sobre')
@app.route('/sobre.html')
def sobre():
    return render_template('sobre.html', active_page='sobre')

@app.route('/servicos')
@app.route('/servicos.html')
def servicos():
    return render_template('servicos.html', active_page='servicos')

@app.route('/noticias')
@app.route('/noticias.html')
def noticias():
    pacote_noticias = obter_noticias_automaticas()
    return render_template('noticias.html', active_page='noticias', pacote=pacote_noticias)

@app.route('/api/noticias')
def api_noticias():
    forcar = request.args.get('refresh') == '1'
    return jsonify(obter_noticias_automaticas(forcar_atualizacao=forcar))

@app.route('/transparencia')
@app.route('/transparencia.html')
def transparencia():
    return render_template('transparencia.html', active_page='transparencia')

@app.route('/contato')
@app.route('/contato.html')
def contato():
    return render_template('contato.html', active_page='contato')

@app.route('/nudea')
@app.route('/nudea.html')
def nudea():
    return render_template('nudea.html', active_page='inicio')

@app.route('/quadro')
@app.route('/quadro.html')
def quadro():
    return render_template('quadro.html', active_page='inicio')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)