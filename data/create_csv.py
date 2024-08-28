import random
import csv
from sre_constants import FAILURE

last_used_id = 10
nm = ("João", "Maria", "José", "Ana", "Pedro", "Luiza", "Marcio", "Mauricio", "Júlia", "Cristina", "Fernanda", "Camila", "Jorge", "Carlos", "Rafael", "Júlio", "Larissa", "Ricardo", "Gabriel", "Clara", "Gustavo", "Beatriz", "Lucas", "Isabela", "Felipe", "Amanda", "Rafaela", "Vinicius", "Laura", "André", "Sophia")
last_nm = ("Silva", "Santos", "Oliveira", "Souza", "Ferreira", "Almeida", "Pereira", "Lima", "Rodrigues", "Costa", "Carvalho", "Martins", "Nascimento", "Ribeiro", "Gomes", "Machado", "Fernandes", "Mendes", "Barros", "Vieira", "Dias", "Alves", "Rocha", "Morais", "Araújo", "Ferreira", "Gonçalves")
d = range(1, 28)
m = range(1, 12)
y = range(1940, 2024)

dts = ['2023-12-01', '2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01', '2024-06-01']

cargos = [
  (1, 'estagiário', 1.50, 'Fazer besteira', 2),
  (2, 'técnico', 3000.00, 'Concertar besteira', 3),
  (3, 'analista', 5000.00, 'Analisar', 4),
  (4, 'gerente', 25000.00,'Gerir', 5),
  (5, 'diretor', 50000.00, 'Dirigir',  None)
]

departamentos = [
  (1, 'RH', 1, '3', 100000.00),
  (2, 'Prod', 2, '4', 150000.00),
  (3, 'Teste', 3, '4', 150000.00),
  (4, 'Atendimento ao cliente', 3, '4', 150000.00),
  (5, 'Limpesa', 5, '5', 150000.00)
]

funcionarios = []
dependentes = []
historico = []
projetos = []
recursos = []

def _gerar_random_dt(min = '1940-01-01', max = '2024-12-30'):
  global d, m, y
  dt = ''
  FAILURES = 0
  while True:
    # print(f"trying + {dt}", end="\t")
    dt = f"{random.choice(y)}-{random.choice(m)}-{random.choice(d)}"
    if dt<max and dt>min:
       # print(f"SUCCESS min: {min} \tmax: {max} \tdt: {dt}" )
      break
    # print(f"FAIL \t min: {min} \tmax: {max} \tdt: {dt}")
    FAILURES += 1
    if FAILURES > 20:
      dt = min
      break
  return dt
  
def _gerar_random_funcionario():  
  global last_used_id, departamentos, cargos, funcionarios, nm, last_nm, d, m, y
  id = last_used_id
  last_used_id += 1
  
  nome = f"{random.choice(nm)} {random.choice(last_nm)} {random.choice(last_nm)}"
  cargo = random.choice(cargos)
  dep = random.choice(departamentos)
  salario = cargo[2] + (random.randint(0, 10)*100)
  dt_nasc = _gerar_random_dt(max = "1990-03-05")

  return (id, nome, dt_nasc, cargo[0], dep[0], salario)

def _gerar_dependente(func):
  global last_used_id, nm, m, d
  id = last_used_id
  last_used_id += 1
  dt_nasc = _gerar_random_dt(min='2005-01-01', max='2010-12-31')
  nome = f"{random.choice(nm)} {random.choice(last_nm)} {func[1].split(' ')[1]}"
  parentesco = random.choice(['filho', 'conjuje','outro'])
  genero = random.choice(["m", "f", "outro"])

  return(id, nome, dt_nasc, parentesco, func[0], genero)

def _gerar_funcionario(dep, cargo, bonificacao = 0):
  func = _gerar_random_funcionario()
  sal = cargo[2] + bonificacao
  return (func[0], func[1], func[2], cargo[0], dep[0], sal)

def _edit_funcionarios(funcionarios_editados):
  global funcionarios
  for new_f in funcionarios_editados:
    for i, f in enumerate(funcionarios):
      if f[0] == new_f[0]:
          funcionarios[i] = new_f
          break

def _gerar_projeto():
  
  global last_used_id, departamentos, cargos, funcionarios, nm, last_nm, d, m, y, dts
  id = last_used_id
  last_used_id += 1

  status = random.choice(['Em Planejamento', 'Em Execucao', 'Concluido', 'Cancelado'])
  custo = random.randint(1, 10)*500

  func = random.choice(funcionarios)
  responsavel = func[0]
  dep = departamentos[func[4]-1]
  departamento_id = dep[0]

  dt_termino = ''
  dt_inicio = random.choice(dts)
  if status != 'Em Planejamento' and status != "Em Execucao":
    dt_inicio = _gerar_random_dt("2010-01-01", "2020-01-01")
    dt_termino = _gerar_random_dt(min = dt_inicio, max="2024-01-01")

  nome = (f"Projeto {dep[1]} {id}")
  descricao = f"Descrição do projeto {nm} conduzido por {func[1]}"

  return (id, nome, descricao, dt_inicio, dt_termino, responsavel, custo, status, departamento_id)

def _gerar_recurso(p):
  
  global last_used_id
  id = last_used_id
  last_used_id += 1

  tipo = random.choice(["financeiro", "material", "humano"])
  qtd = random.randint(1, 10)*50
  if tipo == "humano":
    qtd = random.randint(1, 5)

  dt_pedido = min=p[3]
  if p[7] != 'Em Planejamento' and p[7] != "Em Execucao":
    dt_pedido = _gerar_random_dt(min=p[3], max=p[4])

  descricao = f"Recurso {tipo} {random.choice(['A', 'B', 'C'])}"
  projeto_id = p[0]
  return (id, descricao, tipo, qtd, dt_pedido, projeto_id)
  
def gerar_gerentes():
  global cargos
  cargo = cargos[3]
  for key, dep in enumerate(departamentos):
      f = _gerar_funcionario(dep, cargo)
      departamentos[key] = list(departamentos[key])
      departamentos[key][2] = f[0]
      departamentos[key] = tuple(departamentos[key])
      funcionarios.append(f)

def gerar_funcionarios():
  global cargos, departamentos
  
  for d in departamentos:
    orcamento = d[4] - 25000
    while orcamento > 0:
      c = random.choice(cargos)
      bon = random.randint(0, 10)*100

      if orcamento > bon+c[2]:
        orcamento -= c[2] + bon
        f = _gerar_funcionario(d, c, bon)
        funcionarios.append(f)
      else:
        break

def gerar_dependentes():
  
  for f in funcionarios:
    dependentes.append(_gerar_dependente(f))
    dependentes.append(_gerar_dependente(f))
    if random.randint(0, 1) == 1:
      dependentes.append(_gerar_dependente(f))

def gerar_hist():
  id = 1000
  for dt in dts:
    f_alterados = []
    for f in funcionarios:
      if random.random() > 0.90:
        f = list(f)
        f[5] += random.randint(1, 10)*100
        f = tuple(f)
        f_alterados.append(f)
      historico.append((id, f[0], dt, f[5]))
      id += 1
    _edit_funcionarios(f_alterados)

def gerar_recursos():
  for p in projetos:
    for i in range(random.randint(0, 3)):
      recursos.append(_gerar_recurso(p))

def gerar_projetos():
  for i in range(30):
    projetos.append(_gerar_projeto())
  pass
  
def gravar_csv(nm_arquivo, dados):
  with open(nm_arquivo, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(dados)

def create_csv():
  print("\n GERANDO DADOS _____________________")
  print("\tgerando gerentes...")
  gerar_gerentes()
  print("\tgerando funcionarios...")
  gerar_funcionarios()
  print("\tgerando dependentes...")
  gerar_dependentes()
  print("\tgerando historico...")
  gerar_hist()
  print("\tgerando projetos...")
  gerar_projetos()
  print("\tgerando recursos...")
  gerar_recursos()

  print("\n GRAVANDO CSV _____________________")
  for data in ["funcionarios", "cargos", "departamentos", "historico", "dependentes", "projetos", "recursos"]:
    print(f"\tgravando data/{data}.csv...")
    gravar_csv(f"data/{data}.csv", globals()[data])

  print("\nFINALIZANDO ...")

if __name__ == "__main__":
  create_csv()