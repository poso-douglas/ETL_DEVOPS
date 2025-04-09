from devops_api import DevopsAPI
from database_manipulation import Dados
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()

#CARRAGA AS VARIÁVEIS DE AMBIENTE
ORG = os.getenv("ORGANIZATION")
PAT = os.getenv("PAT")
HEADER = {"Accept" : "application/json"}
auth = HTTPBasicAuth('', PAT)
TABLE_NAMES = os.getenv("TABLE_NAMES")
list_table_names = [i.strip() for i in TABLE_NAMES.split(",")]

#CRIA AS TABELAS NO BANCO CASO NÃO EXISTAM
dados = Dados(org_name = ORG)
for i in list_table_names:
    dados.criar_tabela(i)

#CONSOME OS ENDPOINTS DA API E FAZ AS TRANSFORMAÇÕES
api = DevopsAPI(ORG,auth, HEADER)
projetos = api.listar_projetos()

lista_projetos = api.extrair_projetos(projetos)
print(lista_projetos)

for i in lista_projetos:
    work_items = api.listar_work_items(project=i)
    lista_work_items = api.extrair_workitems_id(json=work_items)
    detalhes_work_items = api.listar_detalhes_work_items(id_list=lista_work_items, project=i)
    json_resultado = api.adicionar_dados_workitem_pai(work_items,detalhes_work_items)
    #EFETUA A INSERÇÃO DOS DADOS
    dados.inserir_dados(json=json_resultado,project=i)
    print(f"Projeto {i} \n")