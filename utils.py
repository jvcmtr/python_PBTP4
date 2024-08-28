import csv

tables = ['funcionarios', 'departamentos', 'cargos', 'historico', 'dependentes', 'projetos', 'recursos']

def load_csv():
  dt = {}
  for t in tables:
    with open(f"data/{t}.csv", "r") as file:
      reader = csv.reader(file)
      dt[t] = [x for x in reader]
  return dt

def list_to_dict(data, headers):
  r = []
  for d in data:
    obj = {}
    for i, h in enumerate(headers):
      dt = d[i]
      if isinstance(dt, int):
        dt = float(dt)
      obj[h] = dt
    r.append(obj)
  return r

