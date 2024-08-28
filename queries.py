from tabulate import tabulate
import utils 
import sqlite3

def querie(s):
  global cursor, console_print
  cursor.execute(s)
  response = cursor.fetchall()
  if console_print:
    print(tabulate(response, tablefmt="grid"))
  return response
  
def q1():
  """Trazer a média dos salários (atual) dos funcionários responsáveis por projetos concluídos, agrupados
por departamento"""
  
  return querie("""
    SELECT 
      d.nome AS departamento, 
      AVG(f.salario) AS media_salario 
    FROM funcionarios f
      JOIN projetos p ON f.id = p.responavel
      JOIN departamentos d ON d.id = p.departamento_id
    WHERE p.status = 'Concluido'
    GROUP BY d.nome
  """)


def q2():
  """Identificar os três recursos materiais mais usados nos projetos, listando a descrição do recurso e a quantidade total usada"""
  
  return querie("""
    SELECT r.descricao, COUNT(p.id), SUM(r.qtd)
    FROM recursos r 
      JOIN projetos p ON r.projeto_id = p.id
    GROUP BY r.descricao
    ORDER BY COUNT(p.id) DESC
    LIMIT 3
  """)


def q3():
  """Calcular o custo total dos projetos por departamento, considerando apenas os projetos
'Concluídos'"""
  
  return querie("""
  SELECT 
    d.nome AS departamento, 
    SUM(p.custo) AS custo_projetos 
  FROM departamentos d
    JOIN projetos p ON d.id = p.departamento_id
  WHERE p.status = 'Concluido'
  GROUP BY d.id
  """)


def q4():
  """Listar todos os projetos com seus respectivos nomes, custo, data de início, data de conclusão
e o nome do funcionário responsável, que estejam 'Em Execução'"""

  # NOTA: a data de término dos projetos em execução é Nula 
  
  return querie("""
  SELECT 
    p.nome AS projeto, 
    p.custo AS custo,
    p.dt_inicio AS dt_inicio,
    p.dt_termino AS dt_termino,
    p.status AS status, 
    f.nome AS funcionario_responsavel 
  FROM projetos p
    JOIN funcionarios f ON p.responavel = f.id
  WHERE p.status = 'Em Execucao'
  """)


def q5():
  """Identificar o projeto com o maior número de dependentes envolvidos, considerando que os dependentes são associados aos funcionários que estão gerenciando os projetos"""

  # NOTA: todos os funcionarios possuem 2 ou 3 dependentes, sendo assim, um conjunto de projetos empata em primeiro lugar
  
  return querie("""
    SELECT p.nome, COUNT(d.id) 
    FROM projetos p
        JOIN funcionarios f ON p.responavel = f.id
        JOIN dependentes d ON f.id = d.funcionario_id
      GROUP BY p.id
      ORDER BY COUNT(d.id) DESC
      LIMIT 1
  """)


def questao(i):
  func = globals()[f"q{i}"]
  if func == None:
    return "Questão não encontrada"

  global cursor, connection, console_print
  console_print = False
  conection = sqlite3.connect("db/empresa.db")
  cursor = conection.cursor()

  data = func()
  headers = [description[0] for description in cursor.description]
  r = utils.list_to_dict(data, headers)
  
  cursor.close()
  conection.close()
  print(r)
  return r

if __name__ == "__main__":
  global cursor, connection, console_print
  console_print = True
  conection = sqlite3.connect("db/empresa.db")
  cursor = conection.cursor()
  q1()
  q2()
  q3()
  q4()
  q5() 
  cursor.close()
  conection.close()