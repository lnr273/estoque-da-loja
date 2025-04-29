import os
import datetime
from flask import Flask, flash, render_template, redirect, request
from sqlalchemy import MetaData, create_engine, Table, Column, Integer, String, Float, Enum, DateTime, insert, select, delete, update, desc, or_, and_
from sqlalchemy.exc import SQLAlchemyError
from helpers import validateInt, validateFloat, error

# VER MUDANÇAS FEITAS NO ARQUIVO DO PYTHOANYWHERE

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

CATEGORIAS = [
    "Cama",
    "Mesa",
    "Banho",
    "Plástico",
    "Cozinha"
]

# criando path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
caminho_db = os.path.join(BASE_DIR, "estoque.db")
# conectando com banco de dados
engine = create_engine(f"sqlite:///{caminho_db}", echo=True)
db = MetaData()
produtosDb = Table("produtos", db,
    Column("id", Integer, primary_key=True),
    Column("nome", String(35), nullable=False),
    Column("quantidade", Integer, nullable=False),
    Column("valor", Float, nullable=False),
    Column("categoria", Enum(*CATEGORIAS), nullable=False),
    Column("last_update", DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now),
)


@app.route("/")
def home():
    order = request.args.get("order") or "recente"
    ordering = {"recente": desc(produtosDb.c.last_update),
                "asc": produtosDb.c.valor, 
                "desc": desc(produtosDb.c.valor),
                "a-z": produtosDb.c.nome,
                "z-a": desc(produtosDb.c.nome),
                "more-quant": desc(produtosDb.c.quantidade),
                "less-quant": produtosDb.c.quantidade}
    
    stmt = select(produtosDb).order_by(ordering[order])
    with engine.connect() as conn:
        try:
            produtos = conn.execute(stmt).fetchall()
        except SQLAlchemyError as e:
            flash(f"Ocorreu um erro ao buscar produtos: {e}")
            produtos = {}

    return render_template("home.html", produtos=produtos)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # verificar nome
        nome = request.form.get("nome")
        if not nome:
            return error("Nome inválido", 403)
        # verificar quantidade
        quantidade = validateInt(request.form.get("quantidade"))
        if quantidade < 1:
            return error("Quantidade inválido: deve ser maior que 0", 403) 
        # verificar valor
        valor = validateFloat(request.form.get("valor"))
        if valor < 0:
            return error("Valor inválido: deve ser maior que 0", 403)
        categoria = request.form.get("categoria")
        if not categoria:
            return error("Categoria inválida", 403)
        # unir todos os dados em um dict
        dadosNovoProduto = {
            "nome": nome.title(), 
            "quantidade": quantidade, 
            "valor": valor, 
            "categoria": categoria,
        }

        # verificar se item já existe
        stmt1 = select(produtosDb).where(produtosDb.c.nome == dadosNovoProduto["nome"])
        with engine.connect() as conn:
            try:
                copia = conn.execute(stmt1).fetchall()
            except:
                return error("ERRO: Produtos não encontrados", 404)
            # loop nos produtos para achar cópia
            if copia:
                return error(f'ERRO: Produto com nome "{dadosNovoProduto["nome"]}" já existe', 400)

        # inserir no banco de dados caso não exista
            stmt2 = insert(produtosDb).values(dadosNovoProduto)
            try:
                conn.execute(stmt2)
                conn.commit()
            except SQLAlchemyError as e:
                return error(f"ERRO: Não foi possível adicionar produto: {e}", 400)
            
        # notificar sucesso e redirecionar para home
        flash("Produto adicionado com sucesso.")
        return redirect("/")
    else:
        return render_template("add.html")


@app.route("/delete")
def delete():
    # validando id
    id = validateInt(request.args.get("id"))
    if id < 1:
        return error("Id inválido", 403)
    
    # deletando do banco de dados
    stmt = produtosDb.delete().where(produtosDb.c.id == id)
    with engine.connect() as conn:
        try:
            conn.execute(stmt)
            conn.commit()
        except SQLAlchemyError as e:
            return error(f"ERRO: Não foi possível deletar produto: {e}", 400)

    flash("Produto excluído com sucesso.")
    return redirect("/")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # verificar id
        id = validateInt(request.form.get("id"))
        if id < 1:
            return error("Id inválido", 403)
        # verificar nome
        nome = request.form.get("nome")
        if not nome:
            return error("Nome inválido", 403)
        # verificar quantidade
        quantidade = validateInt(request.form.get("quantidade"))
        if quantidade < 1:
            return error("Quantidade inválida: deve ser maior que 0", 403)
        # verificar valor
        valor = validateFloat(request.form.get("valor"))
        if valor < 0:
            return error("Valor inválido: deve ser maior que 0", 403)
        categoria = request.form.get("categoria")
        if not categoria:
            return error("Categoria inválida", 403)
        # união de todos os dados para a query
        dadosProdutoEditado = {"nome": nome.title(), 
                               "quantidade": quantidade, 
                               "valor": valor, 
                               "categoria": categoria,}

        # editando o banco de dados
        stmt1 = select(produtosDb).where(
            and_(
                    produtosDb.c.nome == dadosProdutoEditado["nome"],
                    produtosDb.c.id != id
                )
        )
        with engine.connect() as conn:
            try:
                copia = conn.execute(stmt1).fetchone()
            except SQLAlchemyError as e:
                return error(f"ERRO: Não foi possível verificar a existência de cópia: {e}", 400)
            if copia:
                return error(f"ERRO: Produto com nome {dadosProdutoEditado["nome"]} já existe", 400)
            
            stmt2 = update(produtosDb).where(produtosDb.c.id == id).values(dadosProdutoEditado)
            try:
                conn.execute(stmt2)
                conn.commit()
            except SQLAlchemyError as e:
                return error(f"ERRO: Não foi possível editar produto: {e}", 400)

        flash("Produto editado com sucesso.")
        return redirect("/")
    else:
        # validando id 
        id = validateInt(request.args.get("id"))
        if id < 1:
            return error("Id inválido: deve ser maior que 0", 403)
        
        # buscando valores atuais do produto
        stmt = select(produtosDb).where(produtosDb.c.id == id)
        with engine.connect() as conn:
            try:
                produto = conn.execute(stmt).fetchone()
            except SQLAlchemyError as e:
                return error(f"ERRO: Não foi possível buscar produto: {e}", 400)
        return render_template("edit.html", produto=produto)
    

@app.route("/search")
def search():
    q = request.args.get("q")
    if q:
        stmt = select(produtosDb).where(
            or_(
                (produtosDb.c.id.like("%"+ q +"%")),
                (produtosDb.c.nome.like("%"+ q +"%")),
                (produtosDb.c.categoria.like("%"+ q +"%"))
            )
        )
        with engine.connect() as conn:
            try:
                produtos = conn.execute(stmt).fetchall()
            except SQLAlchemyError as e:
                flash(f"Ocorreu um erro ao buscar produto: {e}")

        return render_template("home.html", produtos=produtos, search=q)

    return redirect("/")


if __name__ == "__main__":
    db.create_all(bind=engine)
    app.run(debug=True)