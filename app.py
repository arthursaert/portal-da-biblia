from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# Variável global para armazenar a bíblia na memória do servidor
dados_biblia = {}

def carregar_dados():
    global dados_biblia
    caminho_json = os.path.join(os.path.dirname(__file__), 'biblia.json')
    
    if os.path.exists(caminho_json):
        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados_biblia = json.load(f)
    else:
        print("Erro: O arquivo 'biblia.json' ainda não foi gerado! Rode o parser_biblia.py primeiro.")

# Rota Principal da Aplicação Web
@app.route('/')
def index():
    return render_template('index.html')

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
    if livro in dados_biblia and capitulo in dados_biblia[livro]["capitulos"]:
        versiculos_brutos = dados_biblia[livro]["capitulos"][capitulo]
        # Ordena os versículos numericamente antes de enviar ao front-end
        versiculos_ordenados = dict(sorted(versiculos_brutos.items(), key=lambda x: int(x[0])))
        return jsonify({
            "sucesso": True,
            "livro": livro,
            "capitulo": capitulo,
            "versiculos": versiculos_ordenados
        })
    return jsonify({"sucesso": False, "erro": "Livro ou capítulo não encontrado"}), 404

# Executa o carregamento dos dados direto no escopo global para compatibilidade com o Vercel Serverless
carregar_dados()

if __name__ == '__main__':
    # Isso só roda se você executar o script localmente via terminal
    app.run(debug=True, host='0.0.0.0', port=5000)