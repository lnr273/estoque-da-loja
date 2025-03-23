from flask import Flask, flash, render_template, redirect, request, session
import mysql.connector
from helpers import validateInt, validateFloat, error


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = mysql.connector.connect(user= "root", password= "1234",
                            host="localhost", database="estoquedaloja")
cursor = db.cursor()


@app.route("/")
def home():
    query = "SELECT id, nome, quantidade, valor FROM produtos "

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
            return render_template("error.html", message="Nome inválido")
        # verificar quantidade
        quantidade = validateInt(request.form.get("quantidade"))
        if quantidade < 1:
            return error("Quantidade inválido: deve ser maior que 0", 403) 
        # verificar valor
        valor = validateFloat(request.form.get("valor"))
        if valor < 0:
            return error("Valor inválido: deve ser maior que 0", 403)
        # unir todos os dados em um tuple
        dadosNovoProduto = (nome, quantidade, valor)
        
        # inserir no banco de dados
        query = "INSERT INTO produtos (nome, quantidade, valor) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, dadosNovoProduto)
            db.commit()
        except:
            flash("Erro: ocorreu um erro ao adicionar o produto. Tente novamente.")
            db.rollback()
            return redirect("/")
            
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
        db.commit()
    except:
        flash("Erro: ocorreu um erro ao excluir produto. Tente novamente.")
        db.rollback()
        return redirect("/")
    
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
            return error ("Valor inválido: deve ser maior que 0", 403)
        # união de todos os dados para a query
        dadosProdutoEditado = (nome, quantidade, valor, id)
        # editando o banco de dados
        query = "UPDATE produtos SET nome = %s, quantidade = %s, valor = %s WHERE id = %s"
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
            return render_template("error.html", message="Id inválido: deve ser maior que 0")
        
        # buscando valores atuais do produto
        query = "SELECT id, nome, quantidade, valor FROM produtos WHERE id = %s"
        try:
            cursor.execute(query, (id,))
        except:
            flash("Erro: produto não encontrado no banco de dados.")
            return redirect("/")
    
        produto = cursor.fetchall()
        return render_template("edit.html", produto=produto[0])
    

if __name__ == "__main__":
    app.run(debug=True)