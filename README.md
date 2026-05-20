# Portal da Bíblia

Um portal rápido e simples feito com vibe-coding que contém toda a bíblia construído em Python (Flask).
Acesse nosso site!
[Site do Portal da Bíblia](https://portaldabiblia.vercel.app)

## Como executar

### 1. Criar um VENV (sua escolha)
```bash
python -m venv venv
```

### 2. Baixar as bibliotecas necessárias
```bash
pip install -r requirements.txt
```

### 3. Baixar o ZIP do uemerson-silva/Obsidian-Bible-PT
Você precisa baixar o arquivo, criar uma pasta com o nome "biblia" e colar os livros dentro dela, deve ficar algo como:
```
biblia
|
|
|_______ 01 - Genesis
|
|_______ 02 - Exodus
|
|...
```

### 4. Criar o `biblia.json`
```bash
python parser_biblia.py
```

### 3. Executar o portal
```bash
python app.py
```

## Créditos:
- uemerson-silva/Obsidian-Bible-PT (bíblia NVI em Markdown)
- thiagobodruk/bible (múltiplas versões da bíblia em JSON)

## Licença
Este projeto está licenciado sobre a Apache 2.0, leia o arquivo [LICENSE](LICENSE) para mais detalhes. Ao usar o **Portal da Bíblia** em algum de seus projetos, copie o LICENSE para ele e credite Arthur Santos.