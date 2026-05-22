import json
import os
import glob
import gc  # Garante a limpeza de memória do computador
from weasyprint import HTML
from pypdf import PdfWriter  # Junta os livros de forma ultra rápida

# Configuração focada na pasta 'static' para download direto no seu site
PASTA_BIBLIAS_FONTE = "biblias"
PASTA_SAIDA_PDF = os.path.join("static", "biblias", "pdf")

def garantir_pastas():
    os.makedirs(PASTA_SAIDA_PDF, exist_ok=True)

def extrair_nome_versao(caminho_arquivo):
    nome_base = os.path.splitext(os.path.basename(caminho_arquivo))[0]
    if nome_base.startswith("pt_"):
        sigla = nome_base.split("pt_")[1]
        return f"PT {sigla.upper()}"
    return nome_base.upper()

# ==================== ESTILO CSS DO PDF ====================
CSS_ESTILO_PDF = """
@page {
    size: A4;
    margin: 20mm;
}
body {
    font-family: 'Times New Roman', Times, serif;
    line-height: 1.5;
    color: #000000;
}
.capa {
    page-break-after: always;
    text-align: center;
    padding-top: 40%;
}
.capa h1 {
    font-size: 38pt;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.capa p {
    font-size: 20pt;
    font-style: italic;
}
.bloco-capitulo {
    page-break-before: always;
}
.cabecalho-capitulo {
    text-align: center;
    margin-bottom: 40px;
}
/* Estilo unificado para o Livro + Capítulo na mesma linha */
.cabecalho-capitulo h2 {
    font-size: 26pt;
    text-transform: uppercase;
    margin: 0;
    font-weight: bold;
}
.versiculo-linha {
    font-size: 13pt;
    text-align: justify;
    margin-bottom: 12px;
    display: block;
}
.versiculo-num {
    font-size: 10pt;
    font-weight: bold;
    margin-right: 8px;
}
"""

# ==================== GERADOR DE PDF OTIMIZADO ====================
def gerar_pdf_biblia(caminho_json):
    versao = extrair_nome_versao(caminho_json)
    nome_safe = versao.replace(' ', '_')
    print(f"\n=== Criando PDF: {versao} ===")
    
    with open(caminho_json, 'r', encoding='utf-8') as f:
        dados_biblia = json.load(f)
        
    escritor_pdf = PdfWriter()
    temp_pdfs = []
    
    # 1. Gera a capa do PDF
    html_capa = f"<html><head><meta charset='UTF-8'><style>{CSS_ESTILO_PDF}</style></head><body><div class='capa'><h1>Bíblia Sagrada</h1><p>{versao}</p></div></body></html>"
    caminho_capa_temp = f"temp_capa_{nome_safe}.pdf"
    HTML(string=html_capa).write_pdf(caminho_capa_temp)
    escritor_pdf.append(caminho_capa_temp)
    temp_pdfs.append(caminho_capa_temp)

    # 2. Processa livro por livro (Evita travamentos e lentidão)
    for nome_livro, info_livro in dados_biblia.items():
        print(f" -> Processando: {nome_livro}")
        
        html_livro = f"<html><head><meta charset='UTF-8'><style>{CSS_ESTILO_PDF}</style></head><body>"
        capitulos_ordenados = sorted(info_livro["capitulos"].keys(), key=int)
        
        for num_capitulo in capitulos_ordenados:
            # CORREÇÃO AQUI: Nome do livro e número juntos dentro da mesma tag h2
            html_livro += f"""
            <div class="bloco-capitulo">
                <div class="cabecalho-capitulo">
                    <h2>{nome_livro} {num_capitulo}</h2>
                </div>
            """
            
            versiculos = info_livro["capitulos"][num_capitulo]
            versiculos_ordenados = sorted(versiculos.keys(), key=int)
            
            for num_versiculo in versiculos_ordenados:
                texto_versiculo = versiculos[num_versiculo]
                html_livro += f'<span class="versiculo-linha"><span class="versiculo-num">{num_versiculo}</span>{texto_versiculo}</span>'
            
            html_livro += "</div>"

        html_livro += "</body></html>"
        
        # Renderiza o PDF deste livro isolado
        caminho_livro_temp = f"temp_{nome_safe}_{nome_livro.lower().replace(' ', '_')}.pdf"
        HTML(string=html_livro).write_pdf(caminho_livro_temp)
        escritor_pdf.append(caminho_livro_temp)
        temp_pdfs.append(caminho_livro_temp)
        
        # Limpa o cache de RAM do livro processado
        gc.collect()

    # 3. Salva o PDF final unificado dentro de static
    caminho_pdf_final = os.path.join(PASTA_SAIDA_PDF, f"Biblia_{nome_safe}.pdf")
    print(" -> Juntando todos os livros no arquivo final...")
    with open(caminho_pdf_final, "wb") as f_out:
        escritor_pdf.write(f_out)
    escritor_pdf.close()
    
    # Apaga os arquivos temporários criados
    for temp_file in temp_pdfs:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
    print(f"=== {versao} gerada com sucesso em: {caminho_pdf_final} ===\n")
    return nome_safe, versao


if __name__ == "__main__":
    garantir_pastas()
    arquivos_json = glob.glob(os.path.join(PASTA_BIBLIAS_FONTE, "*.json"))
    
    if not arquivos_json:
        print(f"Aviso: Coloque seus arquivos JSON dentro da pasta '{PASTA_BIBLIAS_FONTE}'.")
    else:
        biblias_processadas = []
        for caminho in arquivos_json:
            try:
                info_salvamento = gerar_pdf_biblia(caminho)
                biblias_processadas.append(info_salvamento)
            except Exception as e:
                print(f"Erro ao processar {caminho}: {e}")
                
        # Gerador do código HTML para você colar no index.html do site
        print("=========================================================")
        print("CÓDIGO HTML PARA COLOCAR NO INÍCIO DO SEU SITE:")
        print("=========================================================\n")
        print('<div class="downloads-biblias">')
        print('    <h3>Baixar Bíblia Sagrada em PDF</h3>')
        print('    <ul class="lista-downloads">')
        for nome_safe, versao in biblias_processadas:
            print(f'        <li>')
            print(f'            <span class="versao-nome">{versao}</span> - ')
            print(f'            <a href="{{{{ url_for(\'static\', filename=\'biblias/pdf/Biblia_{nome_safe}.pdf\') }}}}" class="btn-download" download>Clique aqui para baixar o PDF</a>')
            print(f'        </li>')
        print('    </ul>')
        print('</div>')
        print("\n=========================================================")