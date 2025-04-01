import os
from dotenv import load_dotenv, dotenv_values
from flask import Flask, flash, render_template, redirect, request
import mysql.connector
from helpers import validateInt, validateFloat, error

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")
db = mysql.connector.connect(user= os.getenv("DB_USER"), password= os.getenv("DB_PASSWORD"),
                            host=os.getenv("DB_HOST"), database=os.getenv("DB_SCHEMA"))
cursor = db.cursor()


@app.route("/")
def home():
    query = "SELECT * FROM produtos "

    order = request.args.get("order") or "recente"
    ordering = {"recente": " ",
                "asc": "ORDER BY valor ASC", 
                "desc": "ORDER BY valor DESC",
                "a-z": "ORDER BY nome ASC",
                "z-a": "ORDER BY nome DESC",
                "more-quant": "ORDER BY quantidade DESC",
                "less-quant": "ORDER BY quantidade ASC",}
    
    query += ordering[order]
    cursor.execute(query)
    produtos = cursor.fetchall()
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
        # unir todos os dados em um tuple
        dadosNovoProduto = (nome.title(), quantidade, valor, categoria)
        
        # inserir no banco de dados
        query = "INSERT INTO produtos (nome, quantidade, valor, categoria) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(query, dadosNovoProduto)
        except:
            flash("Erro: ocorreu um erro ao adicionar o produto no banco de dados. Tente novamente.")
            db.rollback()
            return redirect("/")
            
        db.commit()
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
    query = "DELETE FROM produtos WHERE id = %s"
    try:
        cursor.execute(query, (id,))
    except:
        flash("Erro: ocorreu um erro ao excluir produto. Tente novamente.")
        db.rollback()
        return redirect("/")
    
    db.commit()
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
        dadosProdutoEditado = (nome.title(), quantidade, valor, categoria, id)
        # editando o banco de dados
        query = "UPDATE produtos SET nome = %s, quantidade = %s, valor = %s, categoria = %s WHERE id = %s"
        try:
            cursor.execute(query, dadosProdutoEditado)
        except:
            flash("Erro: ocorreu um erro ao editar produto. Tente novamente")
            db.rollback()
            return redirect("/")

        db.commit()
        flash("Produto editado com sucesso.")
        return redirect("/")
    else:
        # validando id 
        id = validateInt(request.args.get("id"))
        if id < 1:
            return error("Id inválido: deve ser maior que 0", 403)
        
        # buscando valores atuais do produto
        query = "SELECT id, nome, quantidade, valor, categoria FROM produtos WHERE id = %s"
        try:
            cursor.execute(query, (id,))
        except:
            flash("Erro: produto não encontrado no banco de dados.")
            return redirect("/")
    
        produto = cursor.fetchall()
        return render_template("edit.html", produto=produto[0])
    

@app.route("/search")
def search():
    q = request.args.get("q")
    query = "SELECT * FROM produtos WHERE id = %s OR nome LIKE %s OR categoria LIKE %s"
    if q:
        try:
            cursor.execute(query, (q, q, q,))
        except:
            flash(f'Erro: não foi possível pesquisar por "{q}"')
            return redirect("/")

        produtos = cursor.fetchall()
        return render_template("home.html", produtos=produtos, search=q)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)