import os
import sys
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Date, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import MetaData



Base = declarative_base()

class Pessoa(Base):
    __tablename__ = '__pessoa'

    id = Column(Integer, primary_key=True)
    nome = Column(String(250))
    data_nascimento = Column(Date())
    enderecos = relationship("Endereco")
    telefones = relationship("Telefone")

    def __init__(self, nome, data_nascimento):
        self.nome = nome
        self.data_nascimento = data_nascimento

    def to_dict(self, includeEndereco=False):
        data = {
            'id' : self.id,
            'nome' : self.nome,
            'data_nascimento' : self.data_nascimento,
        }
        if includeEndereco :
            data['enderecos'] = [item.to_dict() for item in self.enderecos]
            data['telefones'] = [item.to_dict() for item in self.telefones]
        return data

class Endereco(Base):
    __tablename__ = '__endereco'

    id 		= Column(Integer, primary_key=True)
    rua 	= Column(String(250))
    numero	= Column(String(250))
    tipo_end = Column(String(250))
    cep 	= Column(String(250))
    pessoa_id 	= Column(Integer, ForeignKey('__pessoa.id'))

    def __init__(self, rua, numero, tipo_end, cep):
        self.rua = rua
        self.numero = numero
        self.tipo_end = tipo_end
        self.cep = cep

    def to_dict(self):
        data = {
            'id' : self.id,
            'rua' : self.rua,
            'numero' : self.numero,
            'tipo_end' : self.tipo_end,
            'cep' : self.cep,
        }
        return data


class Telefone(Base):
    __tablename__ = '__telefone'

    id 		= Column(Integer, primary_key=True)
    tipo_tel = Column(String(250))
    numero_tel	= Column(String(250))
    pessoa_id 	= Column(Integer, ForeignKey('__pessoa.id'))

    def __init__(self, tipo_tel, numero_tel):
        self.tipo_tel = tipo_tel
        self.numero_tel = numero_tel

    def to_dict(self):
        data = {
            'id' : self.id,
            'tipo_tel' : self.tipo_tel,
            'numero_tel' : self.numero_tel,
        }
        return data

def as_dict(obj):
       mapper = inspect(obj).mapper
       data = {c.key: getattr(obj, c.key)
               for c in mapper.column_attrs}
       for relation in mapper.relationships:
           if relation.direction.name == 'MANYTOONE': continue
           items = getattr(obj, relation.key)
           array = []
           for item in items:
               array.append(as_dict(item))
           data[relation.key] = array
       return data





# Cria o engine apontando para o arquivo pessoa.db
engine = create_engine('sqlite:///pessoa.db')
#engine = create_engine('mysql://versatek2:aluno123!!@xmysql2.versatek.com.br:3306/versatek2')

# Apaga todas as entradas nas tabelas criadas caso essas existam
#metadata = MetaData()
#for tbl in reversed(Base.metadata.sorted_tables):
#    engine.execute(tbl.delete())

# drop todas as tabelas do metadata
#Base.metadata.drop_all(engine)

# Cria todas as tabelas. Isso e equivalente ao "Create Table" do SQL
Base.metadata.create_all(engine)