import os
import json
import re

# Dicionário de tradução exato para mapear as pastas padrão
DICIONARIO_LIVROS = {
    "Genesis": "Gênesis", "Exodus": "Êxodo", "Leviticus": "Levítico", "Numbers": "Números",
    "Deuteronomy": "Deuteronômio", "Joshua": "Josué", "Judges": "Juízes", "Ruth": "Rute",
    "1 Samuel": "1 Samuel", "2 Samuel": "2 Samuel", "1 Kings": "1 Reis", "2 Kings": "2 Reis",
    "1 Chronicles": "1 Crônicas", "2 Chronicles": "2 Crônicas", "Ezra": "Esdras", "Nehemiah": "Neemias",
    "Esther": "Ester", "Job": "Jó", "Psalms": "Salmos", "Psalm": "Salmos", "Proverbs": "Provérbios",
    "Ecclesiastes": "Eclesiastes", "Song of Solomon": "Cânticos", "Isaiah": "Isaías", "Jeremiah": "Jeremias",
    "Lamentations": "Lamentações de Jeremias", "Ezekiel": "Ezequiel", "Daniel": "Daniel", "Hosea": "Oséias",
    "Joel": "Joel", "Amos": "Amós", "Obadiah": "Obadias", "Jonah": "Jonas", "Micah": "Miquéias",
    "Nahum": "Naum", "Habakkuk": "Habacuque", "Zephaniah": "Sofonias", "Haggai": "Ageu",
    "Zechariah": "Zacarias", "Malachi": "Malaquias", "Matthew": "Mateus", "Mark": "Marcos",
    "Luke": "Lucas", "John": "João", "Acts": "Atos dos Apóstolos", "Romans": "Romanos",
    "1 Corinthians": "1 Coríntios", "2 Corinthians": "2 Coríntios", "Galatians": "Gálatas", "Ephesians": "Efésios",
    "Philippians": "Filipenses", "Colossians": "Colossenses", "1 Thessalonians": "1 Tessalonicenses",
    "2 Thessalonians": "2 Tessalonicenses", "1 Timothy": "1 Timóteo", "2 Timothy": "2 Timóteo",
    "Titus": "Tito", "Philemon": "Filemom", "Hebrews": "Hebreus", "James": "Tiago",
    "1 Peter": "1 Pedro", "2 Peter": "2 Pedro", "1 John": "1 João", "2 John": "2 João",
    "3 John": "3 João", "Jude": "Judas", "Revelation": "Apocalipse"
}

def mapear_biblia(diretorio_raiz):
    dados_biblia = {}
    regex_livro = re.compile(r"^(\d+)\s*-\s*(.+)$")
    
    for root, dirs, files in os.walk(diretorio_raiz):
        for file in files:
            if file.endswith('.md'):
                caminho_arquivo = os.path.join(root, file)
                caminho_relativo = os.path.relpath(caminho_arquivo, diretorio_raiz)
                partes = caminho_relativo.split(os.sep)
                
                if len(partes) >= 3:
                    pasta_livro = partes[0].strip()
                    pasta_capitulo = partes[1]
                    nome_arquivo = partes[2]
                    
                    # Força a conversão manual se a pasta for no estilo "John 1", "John 2", etc.
                    match_john = re.match(r"^John\s+(\d+)$", pasta_livro, re.IGNORECASE)
                    if match_john:
                        num_john = match_john.group(1)
                        nome_original_livro = f"{num_john} John"
                        id_livro = 60 + int(num_john) # Define um ID para ordenar depois de 1 Pedro e 2 Pedro
                    else:
                        match_livro = regex_livro.match(pasta_livro)
                        if match_livro:
                            id_livro = int(match_livro.group(1))
                            nome_original_livro = match_livro.group(2).strip()
                        else:
                            id_livro = 99
                            nome_original_livro = pasta_livro
                    
                    # Busca o nome traduzido no dicionário (ex: "1 John" vira "1 João")
                    nome_livro = DICIONARIO_LIVROS.get(nome_original_livro, nome_original_livro)
                        
                    nums_capitulo = re.findall(r'\d+', pasta_capitulo)
                    num_capitulo = int(nums_capitulo[-1]) if nums_capitulo else 1
                    
                    nome_sem_ext = os.path.splitext(nome_arquivo)[0]
                    if '.' in nome_sem_ext:
                        num_versiculo = int(nome_sem_ext.split('.')[-1])
                    else:
                        nums_ver = re.findall(r'\d+', nome_sem_ext)
                        num_versiculo = int(nums_ver[-1]) if nums_ver else 1

                    try:
                        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                            texto_versiculo = f.read().strip()
                    except UnicodeDecodeError:
                        with open(caminho_arquivo, 'r', encoding='windows-1252') as f:
                            texto_versiculo = f.read().strip()

                    if nome_livro not in dados_biblia:
                        dados_biblia[nome_livro] = {"id": id_livro, "capitulos": {}}
                        
                    if str(num_capitulo) not in dados_biblia[nome_livro]["capitulos"]:
                        dados_biblia[nome_livro]["capitulos"][str(num_capitulo)] = {}
                        
                    dados_biblia[nome_livro]["capitulos"][str(num_capitulo)][str(num_versiculo)] = texto_versiculo

    # --- PROCESSO DE ORDENAÇÃO COMPLETA ---
    dados_completamente_ordenados = {}
    livros_ordenados = sorted(dados_biblia.items(), key=lambda item: item[1]["id"])
    
    for nome_livro, conteudo_livro in livros_ordenados:
        capitulos_ordenados = sorted(conteudo_livro["capitulos"].items(), key=lambda c: int(c[0]))
        novo_dicionario_capitulos = {}
        
        for num_capitulo, versiculos in capitulos_ordenados:
            versiculos_ordenados = sorted(versiculos.items(), key=lambda v: int(v[0]))
            novo_dicionario_capitulos[num_capitulo] = dict(versiculos_ordenados)
            
        dados_completamente_ordenados[nome_livro] = {
            "id": conteudo_livro["id"],
            "capitulos": novo_dicionario_capitulos
        }

    with open('biblia.json', 'w', encoding='utf-8') as f_json:
        json.dump(dados_completamente_ordenados, f_json, ensure_ascii=False, indent=2)
        
    print("Sucesso! O arquivo 'biblia.json' foi gerado com '1 João', '2 João' e '3 João' corrigidos e ordenados.")

if __name__ == "__main__":
    mapear_biblia('biblia')