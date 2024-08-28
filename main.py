from fastapi import FastAPI
from queries import questao

app = FastAPI()

@app.get("/")
def read_root():
    return """
    /questao/n
    Retorna a resposta da questao n 

    /salario_medio 
    QUESTAO 1 :  média dos salários (atual) dos funcionários responsáveis por projetos concluídos, agrupados por departamento

    /custo_proj 
    QUESTAO 3 : Calcula o custo total dos projetos por departamento, considerando apenas os projetos 'Concluídos

    /projetos_em_execucao 
    QUESTÃO 4 : Lista todos os projetos com seus respectivos nomes, custo, data de início, data de conclusão e o nome do funcionário responsável, que estejam 'Em Execução'
    """

@app.get("/questao/{id}")
def q(id):
    return questao(id)

@app.get("/salario_medio")
def salario_medio():
    return questao(1)

@app.get("/custo_projetos")
def custo_projetos():
    return questao(3)

@app.get("/projetos_em_execucao")
def projetos_em_execucao():
    return questao(4)

app.mount()