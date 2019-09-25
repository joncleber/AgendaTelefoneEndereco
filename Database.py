# from sqlalchemy.orm import joinedload
from sqlalchemy.orm import sessionmaker, joinedload

from models.DBClasses import Endereco, Pessoa, engine, Telefone, as_dict

DBSession = sessionmaker(bind=engine)


def insertPessoa(nome_, data_nascimento_, rua_, numero_, tipo_end_, cep_, tipo_tel_, numero_tel_):
    session = DBSession()
    p = Pessoa(nome=nome_, data_nascimento=data_nascimento_)
    endereco = Endereco(rua=rua_, numero=numero_, tipo_end=tipo_end_, cep=cep_)
    telefone = Telefone(tipo_tel=tipo_tel_, numero_tel=numero_tel_)
    p.enderecos.append(endereco)
    p.telefones.append(telefone)
    session.add(p)
    session.commit()
    session.close()


def getNome(nome_):
    session = DBSession()
    pessoa = session.query(Pessoa).filter(Pessoa.nome == nome_).all()
    session.close()
    return pessoa


def getId(id_):  # passar string
    session = DBSession()
    pessoa = session.query(Pessoa).filter(Pessoa.id == id_).first()
    session.close()
    return pessoa


def getPessoas():
    session = DBSession()
    pessoas = session.query(Pessoa).all()
    session.close()
    return pessoas


def getPessoasDict():
    session = DBSession()
    pessoas = session.query(Pessoa).options(joinedload('enderecos')).all()
    array = []
    for item in pessoas:
        array.append(as_dict(item))
    # data = {'pessoa': [pessoa.to_dict(True)] for pessoa in pessoas}
    session.close()
    return array


def getPessoasDictID(id_):
    session = DBSession()
    pessoas = session.query(Pessoa.id == id_).options(joinedload('enderecos')).one()
    array = []
    for item in pessoas:
        array.append(as_dict(item))
    #data = {'pessoa': [pessoa.to_dict(True)] for pessoa in pessoas}
    session.close()
    return array


def getPessoasID(id_):
    pessoa_t = getId(id_)
    # pessoa = { 'pessoa' : [ pessoa.to_dict(True)] for pessoa in pessoa_t}
    return pessoa_t


def getEndereco():
    session = DBSession()
    enderecos = session.query(Endereco).all()
    session.close()
    return enderecos


def getTelefones():
    session = DBSession()
    telefones = session.query(Telefone).all()
    session.close()
    return telefones

