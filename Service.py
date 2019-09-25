from datetime import datetime

from flask import Flask, render_template, request, url_for
from flask import jsonify
from werkzeug.utils import redirect
#from flask_restful import Flask

import Database
from models.DBClasses import Pessoa, Endereco, Telefone

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/atualizarPessoa/<int:_id>", methods=["GET", "POST"])
def atualizarPessoa(_id):
    session = Database.DBSession()
    pessoa = session.query(Pessoa).filter_by(id=_id).first()
    if request.method == "POST":
        data = request.form.get("data_de_nascimento")
        ano = int(data[0:4])
        mes = int(data[5:7])
        dia = int(data[8:10])

        nome = request.form.get("nome")

        data_nascimento = datetime(ano, mes, dia)
        if data and nome:
            pessoa.nome = nome
            pessoa.data_nascimento = data_nascimento

            session.commit()
            session.close()
            return redirect(url_for("lista"))
    return render_template('atualizar.html', pessoa=pessoa)


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    session = Database.DBSession()
    if request.form:
        data = request.form.get("data_de_nascimento")
        ano = int(data[0:4])
        mes = int(data[5:7])
        dia = int(data[8:10])

        p = Pessoa(nome=request.form.get("nome"), data_nascimento=datetime(ano, mes, dia))
        endereco = Endereco(rua=request.form.get("rua"), numero=request.form.get("numero"),
                            tipo_end=request.form.get("tipo_end"), cep=request.form.get("cep"))
        telefone = Telefone(tipo_tel=request.form.get("tipo_tel"), numero_tel=request.form.get("numero_tel"))
        p.enderecos.append(endereco)
        p.telefones.append(telefone)

        session.add(p)
        session.commit()
        session.close()

    return render_template('cadastrar.html')


@app.route("/lista")
def lista():
    pessoas = Database.getPessoas()
    return render_template('listaClientes.html', pessoas=pessoas)

@app.route("/listaTelefones")
def listaTelefones():

    telefones = Database.getTelefones()
    return render_template('listaTelefones.html', telefones=telefones)


@app.route("/listaEnderecos")
def listaEnderecos():
    enderecos = Database.getEndereco()
    return render_template('listaEnderecos.html', enderecos=enderecos)


@app.route("/api/getContatos", methods=["GET"])
def json_list():
    pessoas = Database.getPessoasDict()
    return jsonify(pessoas)


@app.route("/api/getContatos/<id>", methods=["GET"])
def getContatoId(id):
    pessoa = Database.getId(id)
    pessoa.toJSON()
    return jsonify(pessoa=pessoa)


@app.route("/excluir/<int:id_>")
def excluir(id_):
    session = Database.DBSession()
    pessoa = session.query(Pessoa).filter_by(id=id_).first()
    endereco = session.query(Endereco).filter_by(pessoa_id=id_).first()
    telefone = session.query(Telefone).filter_by(pessoa_id=id_).first()

    session.delete(telefone)
    session.delete(endereco)
    session.delete(pessoa)
    session.commit()

    pessoa = session.query(Pessoa).all()
    session.close()
    return render_template("listaClientes.html", pessoas=pessoa)


@app.route("/excluir/endereco/<int:id_>")
def excluirEnd(id_):
    session = Database.DBSession()
    endereco = session.query(Endereco).filter_by(id=id_).first()

    session.delete(endereco)
    session.commit()

    enderecos = session.query(Endereco).all()
    session.close()
    return render_template("listaEnderecos.html", enderecos=enderecos)


@app.route("/cadastrarEndereco/<int:_id>", methods=["GET", "POST"])
def cadastrarEndereco(_id):
    session = Database.DBSession()
    pessoa = Database.getId(_id)

    if request.method == "POST":
        p = Pessoa(pessoa)
        endereco = Endereco(rua=request.form.get("rua"), numero=request.form.get("numero"),
                            tipo_end=request.form.get("tipo_end"), cep=request.form.get("cep"))

        p.enderecos.append(endereco)
        session.add(p)
        session.commit()
        session.close()
        return redirect(url_for("listaEnderecos"))

    return render_template('cadastraEndereco.html', id=_id)


@app.route("/atualizarEndereco/<int:_id>", methods=["GET", "POST"])
def atualizarEnderecos(_id):
    session = Database.DBSession()
    endereco = session.query(Endereco).filter_by(id=_id).first()
    if request.method == "POST":
        rua = request.form.get("rua")
        numero = request.form.get("numero")
        tipo_end = request.form.get("tipo_end")
        cep = request.form.get("cep")

        if rua and numero and tipo_end and cep:
            endereco.rua = rua
            endereco.numero = numero
            endereco.tipo_end = tipo_end
            endereco.cep = cep

            session.commit()
            session.close()
            return redirect(url_for("listaEnderecos"))
    return render_template('atualizarEnderecos.html', endereco=endereco)


if __name__ == '__main__':
    app.run(debug=True, port=2000)
