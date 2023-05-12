from flask.templating import render_template_string
from werkzeug.datastructures import RequestCacheControl
from werkzeug.utils import redirect
from application import app, db
from flask import render_template, flash, request, url_for, redirect
from .forms import TodoForm
from datetime import datetime
from bson import ObjectId

@app.route("/")
def get_data():

    mun_mostrar = []

    for mun_dado in db.dado_flask.find().sort("Data_Insercao", -1):

        mun_mostrar.append(mun_dado)

        print(2)

    print(mun_mostrar)

    return render_template("view_municipios.html", title="", todos=mun_mostrar)

@app.route("/add_dado", methods=["POST", "GET"]) ##testar um update dps de finalizar a base
def add_todo():
    if request.method == "POST":
        form = TodoForm(request.form) ##seria melhor colocar varios campos no form, cada um prum tipo de dado pro bson
        dado_nome = form.name.data
        dado_descricao = form.description.data
        checado = form.description.data

        db.dado_flask.insert_one({
            "Municipio": dado_nome,
            "Descricao": dado_descricao,
            "Checado": checado,
            "Data_Insercao": datetime.utcnow()
        }) ##adicionando a uma colecao "dado_flask" ##aqui é um metodo comum, colocar um update e find tbm

        flash("Dado inserido com sucesso.", "sucess")

        return redirect("/") #2 possibilidades de import

    else: #else if request.methods == "GET"

        form = TodoForm()

    return render_template("add_dado.html", form=form)

@app.route("/update_todo/<id>", methods=["POST", "GET"])
def update_dado(id):
    if request.method == "POST":

        form = TodoForm(request.form)

        dado_nome = form.name.data
        dado_descricao = form.description.data
        checado = form.completed.data

        db.dado_flask.find_one_and_update({"_id": ObjectId(id)}, {"$set": {

            "Municipio": dado_nome,
            "Descricao": dado_descricao,
            "Checado": checado

        }})

        flash("Dados atualizados.", "success")

        return redirect("/")

    else:

        form = TodoForm()

        dado = db.dado_flask.find_one({"_id": ObjectId(id)})

        form.name.data = dado.get("Municipio", None)
        form.description.data = dado.get("Descricao", None)
        form.completed.data = dado.get("Checado", None)

    return render_template("add_dado.html", form=form)

@app.route("/delete_dado/<id>")
def delete_dado(id):

    db.dado_flask.find_one_and_delete({"_id": ObjectId(id)})

    flash("Dado deletado.", "sucess")

    return redirect("/")
