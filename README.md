
# Sistema de Cadastro de Produtos

## Descrição do projeto

Este projeto consiste em um sistema de cadastro de produtos desenvolvido em Python utilizando o framework Flask.

O sistema permite cadastrar, consultar, editar, pesquisar e excluir produtos. Os dados são armazenados em um banco de dados relacional SQLite, utilizando Flask-SQLAlchemy.

O projeto possui relacionamento de um para muitos (1:N) entre as tabelas Categoria e Produto.

## Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML5
- CSS3
- Git
- GitHub

## Funcionalidades

- Cadastro de produtos.
- Cadastro automático de três categorias iniciais.
- Relacionamento entre categorias e produtos.
- Listagem de produtos.
- Pesquisa pelo nome do produto.
- Ordenação alfabética.
- Edição de produtos.
- Alteração de imagens.
- Exclusão de produtos e imagens antigas.
- Imagem padrão para produtos sem fotografia.
- Validação de nome e preço.
- Validação de extensão das imagens.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

### 2. Entrar na pasta

```bash
cd sistema_produtos
```

### 3. Criar ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar ambiente virtual

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
venv\Scripts\activate.bat
```

### 5. Instalar dependências

```bash
pip install -r requirements.txt
```

### 6. Executar o sistema

```bash
python app.py
```

### 7. Abrir no navegador

http://127.0.0.1:5000

O banco de dados será criado automaticamente na primeira execução.

## Comandos Git utilizados

### Inicializar o repositório

```bash
git init
```

Inicializa o controle de versão do projeto.

### Adicionar os arquivos

```bash
git add .
```

Adiciona os arquivos para serem incluídos no próximo commit.

### Criar um commit

```bash
git commit -m "Primeira versão do sistema"
```

Registra as alterações no histórico do Git.

### Definir a branch principal

```bash
git branch -M main
```

Define o nome da branch principal como main.

### Conectar ao GitHub

```bash
git remote add origin URL_DO_REPOSITORIO
```

Conecta o projeto local ao repositório remoto.

### Enviar os arquivos

```bash
git push -u origin main
```

Envia os arquivos para o GitHub.

## Banco de dados

O banco utiliza SQLite e possui duas tabelas:

- Categoria: armazena as categorias dos produtos.
- Produto: armazena os produtos e sua respectiva categoria.

O relacionamento entre as tabelas é de um para muitos (1:N).

## Autor

Projeto acadêmico desenvolvido para a disciplina de desenvolvimento web.
