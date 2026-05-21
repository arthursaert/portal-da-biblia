import json

def converter_formato_nvi(arquivo_origem, arquivo_destino):
    try:
        # Mudado para utf-8-sig para ignorar o caractere oculto BOM
        with open(arquivo_origem, 'r', encoding='utf-8-sig') as f:
            dados_antigos = json.load(f)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_origem}' não foi encontrado nesta pasta.")
        return

    dados_novos = {}
    
    # Percorre cada livro do repositório do MaatheusGois
    for id_sequencial, livro in enumerate(dados_antigos, start=1):
        nome_livro = livro["name"]
        capitulos_originais = livro["chapters"]
        
        dicionario_capitulos = {}
        
        # Percorre os capítulos (idx_cap começa em 0, então somamos 1)
        for idx_cap, versiculos_lista in enumerate(capitulos_originais):
            num_capitulo = str(idx_cap + 1)
            dicionario_versiculos = {}
            
            # Percorre os versículos (idx_ver começa em 0, então somamos 1)
            for idx_ver, texto_versiculo in enumerate(versiculos_lista):
                num_versiculo = str(idx_ver + 1)
                dicionario_versiculos[num_versiculo] = texto_versiculo.strip()
            
            # Só adiciona o capítulo se ele tiver versículos
            if dicionario_versiculos:
                dicionario_capitulos[num_capitulo] = dicionario_versiculos
        
        # Monta a estrutura final idêntica à que o seu app usa
        dados_novos[nome_livro] = {
            "id": id_sequencial,
            "capitulos": dicionario_capitulos
        }
        
    # Salva o resultado final ordenado e com caracteres brasileiros corretos
    with open(arquivo_destino, 'w', encoding='utf-8') as f_json:
        json.dump(dados_novos, f_json, ensure_ascii=False, indent=2)
        
    print(f"Sucesso! Bíblia NVI convertida e salva em '{arquivo_destino}' com ordem numérica perfeita.")

if __name__ == "__main__":
    converter_formato_nvi('nvi.json', 'biblia.json')