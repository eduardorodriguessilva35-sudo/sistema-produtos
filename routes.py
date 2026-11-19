
import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from werkzeug.utils import secure_filename

from app import app
from models import db, Produto, Categoria


EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif'}


def extensao_permitida(nome):
    return (
        '.' in nome and
        nome.rsplit('.', 1)[1].lower()
        in EXTENSOES_PERMITIDAS
    )


def validar_preco(valor):
    try:
        preco = float(valor.replace(',', '.'))

        if preco <= 0:
            return None

        return preco

    except (ValueError, AttributeError):
        return None


def salvar_imagem(arquivo):
    if not arquivo or not arquivo.filename:
        return None, None

    if not extensao_permitida(arquivo.filename):
        return None, 'Formato de imagem inválido.'

    nome_seguro = secure_filename(arquivo.filename)

    if not nome_seguro:
        return None, 'Nome de arquivo inválido.'

    extensao = nome_seguro.rsplit('.', 1)[1].lower()

    novo_nome = f'{uuid.uuid4().hex}.{extensao}'

    pasta = os.path.join(
        current_app.root_path,
        'static',
        'uploads'
    )

    os.makedirs(pasta, exist_ok=True)

    arquivo.save(os.path.join(pasta, novo_nome))

    return novo_nome, None


def remover_imagem(nome):
    if not nome or nome == 'padrao.png':
        return

    caminho = os.path.join(
        current_app.root_path,
        'static',
        'uploads',
        nome
    )

    if os.path.isfile(caminho):
        os.remove(caminho)


@app.route('/')
def index():
    busca = request.args.get('busca', '').strip()

    consulta = Produto.query

    if busca:
        consulta = consulta.filter(
            Produto.nome.ilike(f'%{busca}%')
        )

    produtos = consulta.order_by(
        Produto.nome.asc()
    ).all()

    return render_template(
        'index.html',
        produtos=produtos,
        busca=busca
    )


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    categorias = Categoria.query.order_by(
        Categoria.nome.asc()
    ).all()

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        preco = validar_preco(
            request.form.get('preco', '').strip()
        )

        categoria_id = request.form.get('categoria_id', type=int)

        if len(nome) < 3:
            flash('O nome precisa ter pelo menos 3 caracteres.', 'erro')
            return render_template(
                'cadastrar.html',
                categorias=categorias
            )

        if preco is None:
            flash('Informe um preço numérico maior que zero.', 'erro')
            return render_template(
                'cadastrar.html',
                categorias=categorias
            )

        categoria = db.session.get(Categoria, categoria_id)

        if not categoria:
            flash('Selecione uma categoria válida.', 'erro')
            return render_template(
                'cadastrar.html',
                categorias=categorias
            )

        imagem = 'padrao.png'

        arquivo = request.files.get('imagem')

        if arquivo and arquivo.filename:
            imagem_salva, erro = salvar_imagem(arquivo)

            if erro:
                flash(erro, 'erro')
                return render_template(
                    'cadastrar.html',
                    categorias=categorias
                )

            imagem = imagem_salva

        produto = Produto(
            nome=nome,
            preco=preco,
            categoria_id=categoria.id,
            imagem=imagem
        )

        try:
            db.session.add(produto)
            db.session.commit()
            flash('Produto cadastrado com sucesso!', 'sucesso')

        except Exception:
            db.session.rollback()

            if imagem != 'padrao.png':
                remover_imagem(imagem)

            flash('Erro ao cadastrar o produto.', 'erro')

        return redirect(url_for('index'))

    return render_template(
        'cadastrar.html',
        categorias=categorias
    )


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    produto = db.get_or_404(Produto, id)

    categorias = Categoria.query.order_by(
        Categoria.nome.asc()
    ).all()

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        preco = validar_preco(
            request.form.get('preco', '').strip()
        )

        categoria_id = request.form.get('categoria_id', type=int)

        if len(nome) < 3:
            flash('O nome precisa ter pelo menos 3 caracteres.', 'erro')

        elif preco is None:
            flash('Informe um preço numérico maior que zero.', 'erro')

        else:
            categoria = db.session.get(Categoria, categoria_id)

            if not categoria:
                flash('Selecione uma categoria válida.', 'erro')
            else:
                imagem_antiga = produto.imagem
                imagem_nova = None

                arquivo = request.files.get('imagem')

                if arquivo and arquivo.filename:
                    imagem_nova, erro = salvar_imagem(arquivo)

                    if erro:
                        flash(erro, 'erro')

                if (
                    (not arquivo or not arquivo.filename)
                    or imagem_nova is not None
                ):
                    produto.nome = nome
                    produto.preco = preco
                    produto.categoria_id = categoria.id

                    if imagem_nova:
                        produto.imagem = imagem_nova

                    try:
                        db.session.commit()

                        if imagem_nova:
                            remover_imagem(imagem_antiga)

                        flash('Produto atualizado com sucesso!', 'sucesso')
                        return redirect(url_for('index'))

                    except Exception:
                        db.session.rollback()

                        if imagem_nova:
                            remover_imagem(imagem_nova)

                        flash('Erro ao atualizar o produto.', 'erro')

    return render_template(
        'editar.html',
        produto=produto,
        categorias=categorias
    )


@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    produto = db.get_or_404(Produto, id)

    imagem = produto.imagem

    try:
        db.session.delete(produto)
        db.session.commit()

        remover_imagem(imagem)

        flash('Produto excluído com sucesso!', 'sucesso')

    except Exception:
        db.session.rollback()
        flash('Erro ao excluir o produto.', 'erro')

    return redirect(url_for('index'))
