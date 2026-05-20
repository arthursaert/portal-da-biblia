// Estado da aplicação e histórico de navegação
let estruturaCompleta = {};
let ordemOriginalLivros = []; // Array para memorizar a ordem exata do JSON
let versaoSelecionada = "";
let livroSelecionado = "";
let telaAtual = "VERSOES"; // Estados: VERSOES, LIVROS, CAPITULOS, TEXTO

// Elementos do DOM
const areaTextoBiblico = document.getElementById('area-texto-biblico');
const tituloLeitura = document.getElementById('titulo-leitura-atual');
const btnVoltar = document.getElementById('btn-voltar');
const campoPesquisa = document.getElementById('campo-pesquisa');

// 1. INICIALIZAÇÃO: Busca e renderiza as versões disponíveis como botões em grade
async function inicializarPortal() {
    try {
        telaAtual = "VERSOES";
        tituloLeitura.textContent = "Selecione a Versão";
        btnVoltar.classList.add('oculto');
        campoPesquisa.classList.add('oculto');

        const response = await fetch('/api/versoes');
        const versoes = await response.json();

        if (versoes.length === 0) {
            areaTextoBiblico.innerHTML = "<div class='carregando'>Nenhuma versão encontrada na pasta 'biblias/'.</div>";
            return;
        }

        // Renderiza as versões na grade de seleção
        let html = '<div class="grade-selecao">';
        versoes.forEach(v => {
            let nomeTratado = v.nome || v.id.replace('pt_', '').toUpperCase();
            html += `<button class="btn-opcao" onclick="selecionarVersao('${v.id}')">${nomeTratado}</button>`;
        });
        html += '</div>';
        
        areaTextoBiblico.innerHTML = html;

        // Configura eventos dos controles superiores
        btnVoltar.onclick = navegarVoltar;
        campoPesquisa.oninput = filtrarLivros;

    } catch (erro) {
        console.error("Erro ao carregar versões:", erro);
        areaTextoBiblico.innerHTML = "<div class='carregando' style='color:red;'>Erro de conexão com o servidor.</div>";
    }
}

// 2. SELECIONAR VERSÃO -> CARREGA OS LIVROS DAQUELA VERSÃO
window.selecionarVersao = async function(versaoId) {
    versaoSelecionada = versaoId;
    telaAtual = "LIVROS";
    areaTextoBiblico.innerHTML = "<div class='carregando'>Carregando livros...</div>";
    
    try {
        const response = await fetch(`/api/estrutura?versao=${versaoSelecionada}`);
        estruturaCompleta = await response.json();
        
        // Memoriza a ordem exata em que os livros aparecem no arquivo JSON
        ordemOriginalLivros = Object.keys(estruturaCompleta);

        exibirGradeLivros();
    } catch (erro) {
        console.error("Erro ao carregar estrutura da versão:", erro);
        areaTextoBiblico.innerHTML = "<div class='carregando' style='color:red;'>Erro ao carregar os livros desta versão.</div>";
    }
};

function exibirGradeLivros() {
    telaAtual = "LIVROS";
    tituloLeitura.textContent = "Selecione um Livro";
    btnVoltar.classList.remove('oculto');
    campoPesquisa.classList.remove('oculto');
    campoPesquisa.value = "";

    // Renderiza usando a lista guardada na ordem cronológica
    renderizarGradeLivros(ordemOriginalLivros);
}

function renderizarGradeLivros(listaLivros) {
    let html = '<div class="grade-selecao">';
    listaLivros.forEach(livro => {
        html += `<button class="btn-opcao" onclick="selecionarLivro('${livro.replace(/'/g, "\\'")}')">${livro}</button>`;
    });
    html += '</div>';
    areaTextoBiblico.innerHTML = html;
}

// 3. FILTRAR LIVROS (Pesquisa mantendo a ordem do JSON)
function filtrarLivros() {
    if (telaAtual !== "LIVROS") return;
    const termo = campoPesquisa.value.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    
    // Filtra a partir da sequência cronológica armazenada originalmente
    const livrosFiltrados = ordemOriginalLivros.filter(livro => {
        const livroTratado = livro.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
        return livroTratado.includes(termo);
    });
    
    renderizarGradeLivros(livrosFiltrados);
}

// 4. SELECIONAR LIVRO -> EXIBIR GRADE DE CAPÍTULOS
window.selecionarLivro = function(livro) {
    livroSelecionado = livro;
    telaAtual = "CAPITULOS";
    tituloLeitura.textContent = `${livro}`;
    btnVoltar.classList.remove('oculto');
    campoPesquisa.classList.add('oculto');

    const capitulos = estruturaCompleta[livro].capitulos;
    
    let html = '<div class="grade-capitulos">';
    capitulos.forEach(cap => {
        html += `<button class="btn-opcao" onclick="carregarTextoCapitulo(${cap})">${cap}</button>`;
    });
    html += '</div>';
    areaTextoBiblico.innerHTML = html;
};

// 5. CARREGAR E EXIBIR O TEXTO DO CAPÍTULO
window.carregarTextoCapitulo = async function(capitulo) {
    telaAtual = "TEXTO";
    areaTextoBiblico.innerHTML = "<div class='carregando'>Carregando capítulo...</div>";
    tituloLeitura.textContent = `${livroSelecionado} - Capítulo ${capitulo}`;
    
    try {
        const url = `/api/texto?versao=${versaoSelecionada}&livro=${encodeURIComponent(livroSelecionado)}&capitulo=${capitulo}`;
        const response = await fetch(url);
        const versiculos = await response.json();

        let html = '<div class="bloco-leitura">';
        for (const num in versiculos) {
            html += `
                <div class="bloco-versiculo">
                    <span class="num-versiculo">${num}</span>${versiculos[num]}
                </div>
            `;
        }
        html += '</div>';
        areaTextoBiblico.innerHTML = html;
        window.scrollTo(0, 0);
    } catch (erro) {
        console.error("Erro ao carregar texto:", erro);
        areaTextoBiblico.innerHTML = "<div class='carregando' style='color:red;'>Não foi possível renderizar o texto deste capítulo.</div>";
    }
};

// 6. GERENCIADOR DO BOTÃO VOLTAR
function navegarVoltar() {
    if (telaAtual === "TEXTO") {
        selecionarLivro(livroSelecionado);
    } else if (telaAtual === "CAPITULOS") {
        exibirGradeLivros();
    } else if (telaAtual === "LIVROS") {
        inicializarPortal();
    }
}

document.addEventListener('DOMContentLoaded', inicializarPortal);