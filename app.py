from flask import Flask, render_template, jsonify
import json
import os
import urllib.parse

app = Flask(__name__)

# Variável global para armazenar a bíblia na memória do servidor
dados_biblia = {}

def carregar_dados():
    global dados_biblia
    caminho_json = os.path.join(os.path.dirname(__file__), 'biblia.json')
    
    if os.path.exists(caminho_json):
        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados_brutos = json.load(f)
            
        # Normaliza as chaves do dicionário para garantir correspondência exata
        dados_biblia = {}
        for livro, conteudo in dados_brutos.items():
            # Força o nome do livro a ser limpo e bem decodificado
            nome_normalizado = urllib.parse.unquote(livro).strip()
            dados_biblia[nome_normalizado] = conteudo
    else:
        print("Erro: O arquivo 'biblia.json' ainda não foi gerado! Rode o parser_biblia.py primeiro.")

# Rota Principal da Aplicação Web
@app.route('/')
def index():
    return render_template('index.html')

# Rota para servir o Service Worker na raiz do site (Obrigatório para PWA)
@app.route('/sw.js')
def serve_sw():
    return app.send_static_file('js/sw.js'), 200, {'Content-Type': 'application/javascript'}

# Rota para servir o Manifest
@app.route('/manifest.json')
def serve_manifest():
    return app.send_static_file('manifest.json'), 200, {'Content-Type': 'application/json'}

# API: Retorna a lista de todos os livros disponíveis para preencher os menus
@app.route('/api/livros', methods=['GET'])
def obter_livros():
    lista_livros = []
    for nome_livro, conteudo in dados_biblia.items():
        lista_livros.append({
            "nome": nome_livro,
            "total_capitulos": len(conteudo["capitulos"])
        })
    return jsonify(lista_livros)

# API: Retorna o texto completo de um capítulo específico de um livro
@app.route('/api/texto/<livro>/<capitulo>', methods=['GET'])
def obter_capitulo(livro, capitulo):
    # Decodifica explicitamente o nome do livro vindo da URL (ex: "Jo%C3%A3o" vira "João")
    livro_decodificado = urllib.parse.unquote(livro).strip()
    capitulo_str = str(capitulo).strip()

    if livro_decodificado in dados_biblia:
        capitulos_do_livro = dados_biblia[livro_decodificado]["capitulos"]
        
        # Procura o capítulo tratando tanto como String quanto garantindo que exista
        if capitulo_str in capitulos_do_livro:
            versiculos_brutos = capitulos_do_livro[capitulo_str]
            # Ordena os versículos numericamente antes de enviar ao front-end
            versiculos_ordenados = dict(sorted(versiculos_brutos.items(), key=lambda x: int(x[0])))
            
            return jsonify({
                "sucesso": True,
                "livro": livro_decodificado,
                "capitulo": capitulo_str,
                "versiculos": versiculos_ordenados
            })
            
    return jsonify({"sucesso": False, "erro": f"Livro '{livro_decodificado}' ou capitulo '{capitulo_str}' nao encontrado"}), 404

# Executa o carregamento dos dados direto no escopo global para compatibilidade com o Vercel Serverless
carregar_dados()

if __name__ == '__main__':
    # Isso só roda se você executar o script localmente via terminal
    app.run(debug=True, host='0.0.0.0', port=5000)