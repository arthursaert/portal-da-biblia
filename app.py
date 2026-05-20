from flask import Flask, render_template, jsonify, request
import os
import json

app = Flask(__name__)

# Caminho para a pasta onde ficam os JSONs das bíblias
PASTA_BIBLIAS = os.path.join(os.path.dirname(__file__), 'biblias')

def obter_versoes_disponiveis():
    """
    Varre a pasta 'biblias/', descobre os arquivos .json e cria um nome 
    amigável para a interface (ex: 'biblia_pt_acf.json' -> 'PT ACF')
    """
    versoes = []
    if not os.path.exists(PASTA_BIBLIAS):
        return versoes

    for arquivo in sorted(os.listdir(PASTA_BIBLIAS)):
        if arquivo.endswith('.json'):
            # Remove a extensão .json
            nome_base = arquivo[:-5]
            
            # Remove o prefixo 'biblia_' se ele existir
            if nome_base.startswith('biblia_'):
                nome_base = nome_base[7:]
            
            # Formata o nome para exibição (substitui underscores por espaços e põe em maiúsculo)
            # 'pt_acf' vira 'PT ACF'
            nome_exibicao = nome_base.replace('_', ' ').upper()
            
            versoes.append({
                'id': arquivo,          # Nome do arquivo real (ex: 'biblia_pt_acf.json')
                'nome': nome_exibicao   # Nome bonito (ex: 'PT ACF')
            })
    return versoes

def carregar_dados_biblia(arquivo_versao):
    """Carrega o arquivo JSON de uma versão específica com segurança."""
    caminho_arquivo = os.path.join(PASTA_BIBLIAS, arquivo_versao)
    if not os.path.exists(caminho_arquivo):
        # Se não achar a versão pedida, tenta pegar a primeira disponível
        versoes = obter_versoes_disponiveis()
        if versoes:
            caminho_arquivo = os.path.join(PASTA_BIBLIAS, versoes[0]['id'])
        else:
            return {}
            
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    # Renderiza a página principal do portal
    return render_template('index.html')

@app.route('/api/versoes')
def api_versoes():
    """Rota para o Frontend descobrir quais versões existem no sistema."""
    return jsonify(obter_versoes_disponiveis())

@app.route('/api/estrutura')
def api_estrutura():
    """Retorna os livros e a quantidade de capítulos com base na versão selecionada."""
    arquivo_versao = request.args.get('versao')
    dados_biblia = carregar_dados_biblia(arquivo_versao)
    
    estrutura = {}
    for nome_livro, dados in dados_biblia.items():
        # Guarda o ID de ordenação do livro e a lista de capítulos disponíveis
        estrutura[nome_livro] = {
            'id': dados.get('id', 99),
            'capitulos': sorted([int(c) for c in dados.get('capitulos', {}).keys()])
        }
    
    # Ordena os livros pelo ID interno deles (Gênesis=1, Êxodo=2...)
    estrutura_ordenada = dict(sorted(estrutura.items(), key=lambda item: item[1]['id']))
    return jsonify(estrutura_ordenada)

@app.route('/leitura/<versao>/<livro_url>/<capitulo>')
def link_direto_leitura(versao, livro_url, capitulo):
    # Entrega o template base. O JavaScript vai ler a URL limpa e renderizar os versículos.
    return render_template('index.html')

@app.route('/api/texto')
def api_texto():
    """Retorna os versículos de um capítulo específico da versão selecionada."""
    arquivo_versao = request.args.get('versao')
    livro = request.args.get('livro')
    capitulo = request.args.get('capitulo')
    
    dados_biblia = carregar_dados_biblia(arquivo_versao)
    
    if livro in dados_biblia and capitulo in dados_biblia[livro]['capitulos']:
        versiculos = dados_biblia[livro]['capitulos'][capitulo]
        # Garante a ordenação correta dos versículos numéricos
        versiculos_ordenados = dict(sorted(versiculos.items(), key=lambda item: int(item[0])))
        return jsonify(versiculos_ordenados)
        
    return jsonify({"erro": "Capítulo ou livro não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)