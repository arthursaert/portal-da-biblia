document.addEventListener('DOMContentLoaded', () => {
    const btnVoltar = document.getElementById('btn-voltar');
    const tituloLeitura = document.getElementById('titulo-leitura-atual');
    const areaTextoBiblico = document.getElementById('area-texto-biblico');

    // Estado da navegação do usuário
    let bancoDadosLivros = [];
    let livroSelecionado = "";
    let capituloSelecionado = "";

    // 1. Inicialização: Busca a lista de livros da API do Flask
    function carregarMenuLivros() {
        livroSelecionado = "";
        capituloSelecionado = "";
        
        tituloLeitura.textContent = "Selecione um Livro";
        btnVoltar.classList.add('oculto');
        areaTextoBiblico.innerHTML = '<div class="carregando">Carregando livros...</div>';

        // Caso os livros já tenham sido baixados uma vez, evita nova requisição HTTP
        if (bancoDadosLivros.length > 0) {
            renderizarGradeLivros(bancoDadosLivros);
            return;
        }

        fetch('/api/livros')
            .then(response => response.json())
            .then(livros => {
                bancoDadosLivros = livros;
                renderizarGradeLivros(livros);
            })
            .catch(err => {
                console.error('Erro ao buscar livros:', err);
                areaTextoBiblico.innerHTML = '<div class="carregando" style="color:red;">Falha ao conectar com o servidor.</div>';
            });
    }

    // 2. Renderiza a lista de livros no formato de botões organizados em grade
    function renderizarGradeLivros(livros) {
        areaTextoBiblico.innerHTML = '';
        const grade = document.createElement('div');
        grade.className = 'grade-selecao';

        livros.forEach(livro => {
            const botao = document.createElement('button');
            botao.className = 'btn-opcao';
            botao.textContent = livro.nome;
            botao.addEventListener('click', () => carregarMenuCapitulos(livro.nome, livro.total_capitulos));
            grade.appendChild(botao);
        });

        areaTextoBiblico.appendChild(grade);
    }

    // 3. Renderiza os botões numéricos dos capítulos baseados no livro escolhido
    function carregarMenuCapitulos(nomeLivro, totalCapitulos) {
        livroSelecionado = nomeLivro;
        
        tituloLeitura.textContent = nomeLivro;
        btnVoltar.textContent = "← Escolher Outro Livro";
        btnVoltar.classList.remove('oculto');
        
        areaTextoBiblico.innerHTML = '';
        const gradeCapitulos = document.createElement('div');
        gradeCapitulos.className = 'grade-capitulos';

        for (let i = 1; i <= totalCapitulos; i++) {
            const botaoCap = document.createElement('button');
            botaoCap.className = 'btn-opcao';
            botaoCap.textContent = i;
            botaoCap.addEventListener('click', () => carregarTextoCapitulo(nomeLivro, i));
            gradeCapitulos.appendChild(botaoCap);
        }

        areaTextoBiblico.appendChild(gradeCapitulos);
    }

    // 4. Faz a requisição dos versículos e injeta linha por linha na tela
    function carregarTextoCapitulo(livro, capitulo) {
        capituloSelecionado = capitulo;
        
        btnVoltar.textContent = `← Ver Capítulos de ${livro}`;
        tituloLeitura.textContent = `${livro} — Capítulo ${capitulo}`;
        areaTextoBiblico.innerHTML = '<div class="carregando">Carregando textos sagrados...</div>';

        fetch(`/api/texto/${encodeURIComponent(livro)}/${capitulo}`)
            .then(response => response.json())
            .then(data => {
                if (data.sucesso) {
                    areaTextoBiblico.innerHTML = '';
                    
                    const containerLeitura = document.createElement('div');
                    containerLeitura.className = 'bloco-leitura';

                    Object.keys(data.versiculos).forEach(numVer => {
                        const blocoVersiculo = document.createElement('div');
                        blocoVersiculo.className = 'bloco-versiculo';

                        const spanNumero = document.createElement('span');
                        spanNumero.className = 'num-versiculo';
                        spanNumero.textContent = numVer;

                        const spanTexto = document.createElement('span');
                        spanTexto.className = 'texto-versiculo';
                        spanTexto.textContent = data.versiculos[numVer];

                        blocoVersiculo.appendChild(spanNumero);
                        blocoVersiculo.appendChild(spanTexto);
                        containerLeitura.appendChild(blocoVersiculo);
                    });

                    areaTextoBiblico.appendChild(containerLeitura);
                    // Rola a página suavemente para o topo do texto
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                } else {
                    areaTextoBiblico.innerHTML = `<div class="carregando" style="color:red;">Erro: ${data.erro}</div>`;
                }
            })
            .catch(err => {
                console.error('Erro na requisição do texto:', err);
                areaTextoBiblico.innerHTML = '<div class="carregando" style="color:red;">Erro técnico ao carregar o conteúdo.</div>';
            });
    }

    // 5. Gerenciador do Botão de Voltar (Sabe se volta para os capítulos ou para os livros)
    btnVoltar.addEventListener('click', () => {
        if (capituloSelecionado !== "") {
            // Se estava lendo o texto, volta para a seleção de capítulos daquele livro
            const livroAtivo = bancoDadosLivros.find(l => l.nome === livroSelecionado);
            carregarMenuCapitulos(livroAtivo.nome, livroAtivo.total_capitulos);
            capituloSelecionado = "";
        } else if (livroSelecionado !== "") {
            // Se estava na tela de capítulos, volta para a tela inicial de livros
            carregarMenuLivros();
        }
    });

    // Inicializa carregando a tela de livros assim que entra no site
    carregarMenuLivros();
});