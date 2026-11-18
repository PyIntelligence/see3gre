import os
import sys
from flask import Flask, jsonify, render_template, request, send_from_directory

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SEE3GRE_DIR = os.path.dirname(CURRENT_DIR)

if SEE3GRE_DIR not in sys.path:
    sys.path.insert(0, SEE3GRE_DIR)

from services.noticias_service import obter_noticias_automaticas

app = Flask(
    __name__,
    template_folder=os.path.join(SEE3GRE_DIR, 'templates'),
    static_folder=os.path.join(SEE3GRE_DIR, 'static'),
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

@app.route('/manifest.json')
def pwa_manifest():
    return send_from_directory(
        app.static_folder,
        'manifest.json',
        mimetype='application/manifest+json'
    )

@app.route('/sw.js')
def pwa_service_worker():
    response = send_from_directory(
        app.static_folder,
        'sw.js',
        mimetype='application/javascript'
    )
    response.headers['Cache-Control'] = 'no-cache'
    return response