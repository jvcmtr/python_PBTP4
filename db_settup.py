import sqlite3
from utils import load_csv, tables

conection = sqlite3.connect("db/empresa.db")
cursor = conection.cursor()
data = {}

def create_tables():
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS funcionarios(
    id INTEGER not null primary key ,
    nome TEXT not null,
    dt_nasc TEXT,
    cargo_id INTEGER, 
    departamento_id INTEGER not null,
    salario REAL,
  
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
    FOREIGN KEY (cargo_id) REFERENCES cargos(id)
  )""")
  
  cursor.execute("""
  create table IF NOT EXISTS cargos(
    id INTEGER not null primary key,
    nome TEXT,
    descricao TEXT not null,
    salario_base REAL,
    promocao_id INTEGER,
  
    FOREIGN KEY (promocao_id) REFERENCES cargo(id)
  );""")
  
  cursor.execute("""
  create table IF NOT EXISTS  departamentos(
    id INTEGER not null primary key,
    nome TEXT,
    gerente_id INTEGER not null,
    andar TEXT,
    orcamento REAL
  );""")
  
  cursor.execute("""
  create table IF NOT EXISTS historico(
    id INTEGER not null primary key,
    funcionario_id INTEGER not null,
    dt_pagamento TEXT not null,
    pagamento REAL not null  ,
  
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
  );""")
  
  cursor.execute("""
  create table IF NOT EXISTS dependentes(
    id INTEGER not null primary key,
    nome TEXT not null,
    dt_nasc TEXT,
    parentesco TEXT,
    funcionario_id INTEGER not null,
    genero TEXT,
  
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
  )""")

cursor.execute("""
create table IF NOT EXISTS projetos(
  id TEXT NOT NULL PRIMARY KEY,
  nome TEXT NOT NULL ,
  descricao TEXT NOT NULL ,
  dt_inicio TEXT NOT NULL , 
  dt_termino TEXT, 
  responavel INTEGER not null, 
  custo INTEGER NOT NULL, 
  status TEXT NOT NULL , 
  departamento_id INTEGER NOT NULL,

  FOREIGN KEY (responavel) REFERENCES funcionarios(id),
  FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
)""")

cursor.execute("""
  create table IF NOT EXISTS recursos(
    id INTEGER NOT NULL PRIMARY KEY, 
    descricao TEXT not null, 
    tipo TEXT not null, 
    qtd INTEGER not null, 
    dt_pedido TEXT not null, 
    projeto_id TEXT not null, 
    
    FOREIGN KEY (projeto_id) REFERENCES projetos(id)
    )""")

def insert():
  for table in tables:
    cursor.execute(f"DELETE from {table}")
    cursor.executemany(f"insert into {table} values({('?,'*(len(data[table][0])-1))+'?'})", data[table])
  
def main():
  global data
  data = load_csv()
  create_tables()
  insert()
  conection.commit()

if __name__ == "__main__":
  main()
  
cursor.close()
conection.close()