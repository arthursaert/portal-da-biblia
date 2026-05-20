import json
import os

# Dicionário mapeando as abreviações do repositório do Thiago Bodruk para os nomes em português
MAPA_ABREVIACOES = {
    "gn": "Gênesis", "ex": "Êxodo", "lv": "Levítico", "nm": "Números", "dt": "Deuteronômio",
    "js": "Josué", "jz": "Juízes", "rt": "Rute", "1sm": "1 Samuel", "2sm": "2 Samuel",
    "1rs": "1 Reis", "2rs": "2 Reis", "1cr": "1 Crônicas", "2cr": "2 Crônicas", "ez": "Esdras",
    "ne": "Neemias", "et": "Ester", "jó": "Jó", "ps": "Salmos", "pv": "Provérbios",
    "ec": "Eclesiastes", "ct": "Cânticos", "is": "Isaías", "jr": "Jeremias", "lm": "Lamentações de Jeremias",
    "ezk": "Ezequiel", "dn": "Daniel", "os": "Oséias", "jl": "Joel", "am": "Amós",
    "ob": "Obadias", "jn": "Jonas", "mq": "Miquéias", "na": "Naum", "hc": "Habacuque",
    "sf": "Sofonias", "ag": "Ageu", "zc": "Zacarias", "ml": "Malaquias", "mt": "Mateus",
    "mc": "Marcos", "lc": "Lucas", "jo": "João", "at": "Atos dos Apóstolos", "rm": "Romanos",
    "1co": "1 Coríntios", "2co": "2 Coríntios", "gl": "Gálatas", "ef": "Efésios", "fp": "Filipenses",
    "cl": "Colossenses", "1ts": "1 Tessalonicenses", "2ts": "2 Tessalonicenses", "1tm": "1 Timóteo",
    "2tm": "2 Timóteo", "tt": "Tito", "fm": "Filemom", "hb": "Hebreus", "tg": "Tiago",
    "1pe": "1 Pedro", "2pe": "2 Pedro", "1jo": "1 João", "2jo": "2 João", "3jo": "3 João",
    "jd": "Judas", "ap": "Apocalipse"
}

def converter_formato_thiago(arquivo_entrada, nome_versao_saida):
    """
    arquivo_entrada: Caminho do arquivo baixado (ex: 'pt_acf.json')
    nome_versao_saida: Nome final que você quer no sistema (ex: 'acf' ou 'almeida')
    """
    if not os.path.exists(arquivo_entrada):
        print(f"Erro: O arquivo de entrada '{arquivo_entrada}' não foi encontrado.")
        return

    # Garante que a pasta 'biblias' existe
    os.makedirs('biblias', exist_ok=True)

    print(f"Lendo e convertendo '{arquivo_entrada}'...")
    
    # MUDANÇA AQUI: Mudamos de encoding='utf-8' para 'utf-8-sig' para ignorar o caractere BOM automático
    with open(arquivo_entrada, 'r', encoding='utf-8-sig') as f:
        dados_thiago = json.load(f)

    dados_convertidos = {}
    
    # Varre a lista de livros do formato do Thiago
    for id_livro, item_livro in enumerate(dados_thiago, start=1):
        abbrev = item_livro.get("abbrev", "").lower()
        capitulos_lista = item_livro.get("chapters", [])
        
        # Obtém o nome bonito em português. Se não achar, usa o nome que estiver lá
        nome_livro = MAPA_ABREVIACOES.get(abbrev, item_livro.get("name", abbrev.upper()))
        
        # Estrutura inicial do livro no formato padrão do seu Portal
        dados_convertidos[nome_livro] = {
            "id": id_livro,
            "capitulos": {}
        }
        
        # Varre os capítulos (que vêm em listas)
        for index_cap, versiculos_lista in enumerate(capitulos_lista, start=1):
            num_capitulo_str = str(index_cap)
            dados_convertidos[nome_livro]["capitulos"][num_capitulo_str] = {}
            
            # Varre os versículos (que também vêm em listas)
            for index_ver, texto_versiculo in enumerate(versiculos_lista, start=1):
                num_versiculo_str = str(index_ver)
                dados_convertidos[nome_livro]["capitulos"][num_capitulo_str][num_versiculo_str] = texto_versiculo.strip()

    # Caminho do arquivo final convertido
    arquivo_saida = f"biblias/biblia_{nome_versao_saida.lower()}.json"
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f_out:
        json.dump(dados_convertidos, f_out, ensure_ascii=False, indent=2)
        
    print(f"🎉 Sucesso! Arquivo convertido e salvo em: {arquivo_saida}\n")

if __name__ == "__main__":
    # Converte o arquivo baixado
    converter_formato_thiago('pt_acf.json', 'acf')