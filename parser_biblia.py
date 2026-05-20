import os
import json
import re

# Dicionário de tradução de Inglês para Português para os 66 livros da Bíblia
DICIONARIO_LIVROS = {
    "Genesis": "Gênesis",
    "Exodus": "Êxodo",
    "Leviticus": "Levítico",
    "Numbers": "Números",
    "Deuteronomy": "Deuteronômio",
    "Joshua": "Josué",
    "Judges": "Juízes",
    "Ruth": "Rute",
    "1 Samuel": "1 Samuel",
    "2 Samuel": "2 Samuel",
    "1 Kings": "1 Reis",
    "2 Kings": "2 Reis",
    "1 Chronicles": "1 Crônicas",
    "2 Chronicles": "2 Crônicas",
    "Ezra": "Esdras",
    "Nehemiah": "Neemias",
    "Esther": "Ester",
    "Job": "Jó",
    "Psalms": "Salmos",
    "Proverbs": "Provérbios",
    "Ecclesiastes": "Eclesiastes",
    "Song of Solomon": "Cânticos",
    "Isaiah": "Isaías",
    "Jeremiah": "Jeremias",
    "Lamentations": "Lamentações de Jeremias",
    "Ezekiel": "Ezequiel",
    "Daniel": "Daniel",
    "Hosea": "Oséias",
    "Joel": "Joel",
    "Amos": "Amós",
    "Obadiah": "Obadias",
    "Jonah": "Jonas",
    "Micah": "Miquéias",
    "Nahum": "Naum",
    "Habakkuk": "Habacuque",
    "Zephaniah": "Sofonias",
    "Haggai": "Ageu",
    "Zechariah": "Zacarias",
    "Malachi": "Malaquias",
    "Matthew": "Mateus",
    "Mark": "Marcos",
    "Luke": "Lucas",
    "John": "João",
    "Acts": "Atos dos Apóstolos",
    "Romans": "Romanos",
    "1 Corinthians": "1 Coríntios",
    "2 Corinthians": "2 Coríntios",
    "Galatians": "Gálatas",
    "Ephesians": "Efésios",
    "Philippians": "Filipenses",
    "Colossians": "Colossenses",
    "1 Thessalonians": "1 Tessalonicenses",
    "2 Thessalonians": "2 Tessalonicenses",
    "1 Timothy": "1 Timóteo",
    "2 Timothy": "2 Timóteo",
    "Titus": "Tito",
    "Philemon": "Filemom",
    "Hebrews": "Hebreus",
    "James": "Tiago",
    "1 Peter": "1 Pedro",
    "2 Peter": "2 Pedro",
    "1 John": "1 João",
    "2 John": "2 João",
    "3 John": "3 João",
    "Jude": "Judas",
    "Revelation": "Apocalipse"
}

def mapear_biblia(diretorio_raiz):
    dados_biblia = {}

    # Regex para capturar o número e o nome do livro (ex: "02 - Exodus")
    regex_livro = re.compile(r"^(\d+)\s*-\s*(.+)$")
    
    for root, dirs, files in os.walk(diretorio_raiz):
        for file in files:
            if file.endswith('.md'):
                caminho_arquivo = os.path.join(root, file)
                
                caminho_relativo = os.path.relpath(caminho_arquivo, diretorio_raiz)
                partes = caminho_relativo.split(os.sep)
                
                if len(partes) >= 3:
                    pasta_livro = partes[0]      # Ex: "02 - Exodus"
                    pasta_capitulo = partes[1]   # Ex: "Exodus 11"
                    nome_arquivo = partes[2]     # Ex: "Exodus 11.2.md"
                    
                    # Extrair ordem e nome contido na pasta
                    match_livro = regex_livro.match(pasta_livro)
                    if match_livro:
                        id_livro = int(match_livro.group(1))
                        nome_original_livro = match_livro.group(2).strip()
                    else:
                        id_livro = 99
                        nome_original_livro = pasta_livro
                    
                    # Traduz o nome do livro se ele existir no dicionário, senão mantém o original
                    nome_livro = DICIONARIO_LIVROS.get(nome_original_livro, nome_original_livro)
                        
                    # Extrair número do capítulo de forma segura
                    nums_capitulo = re.findall(r'\d+', pasta_capitulo)
                    num_capitulo = int(nums_capitulo[-1]) if nums_capitulo else 1
                    
                    # Extrair número do versículo do nome do arquivo
                    nome_sem_ext = os.path.splitext(nome_arquivo)[0]
                    if '.' in nome_sem_ext:
                        num_versiculo = int(nome_sem_ext.split('.')[-1])
                    else:
                        nums_ver = re.findall(r'\d+', nome_sem_ext)
                        num_versiculo = int(nums_ver[-1]) if nums_ver else 1

                    # Tenta ler em UTF-8; se falhar por caracteres especiais antigos, usa Windows-1252
                    try:
                        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                            texto_versiculo = f.read().strip()
                    except UnicodeDecodeError:
                        with open(caminho_arquivo, 'r', encoding='windows-1252') as f:
                            texto_versiculo = f.read().strip()

                    # Estruturar os dados no dicionário usando o nome traduzido
                    if nome_livro not in dados_biblia:
                        dados_biblia[nome_livro] = {
                            "id": id_livro,
                            "capitulos": {}
                        }
                        
                    if str(num_capitulo) not in dados_biblia[nome_livro]["capitulos"]:
                        dados_biblia[nome_livro]["capitulos"][str(num_capitulo)] = {}
                        
                    dados_biblia[nome_livro]["capitulos"][str(num_capitulo)][str(num_versiculo)] = texto_versiculo

    # Ordenar os livros pelo ID interno deles (01, 02, 03...)
    dados_ordenados = dict(sorted(dados_biblia.items(), key=lambda item: item[1]["id"]))

    # Salvar tudo no arquivo JSON final
    with open('biblia.json', 'w', encoding='utf-8') as f_json:
        json.dump(dados_ordenados, f_json, ensure_ascii=False, indent=2)
        
    print("Sucesso! O arquivo 'biblia.json' foi gerado com os nomes em português.")

if __name__ == "__main__":
    mapear_biblia('biblia')