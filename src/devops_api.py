import requests
from requests.auth import HTTPBasicAuth
import sqlite3
from datetime import date,datetime

class DevopsAPI():
    def __init__(self,org_name:str, auth:str, header:str):
        """_summary_
        Classe que faz o consumo de dados dos endpoints da api do devops e o tratamento dos dados
        para que se obtenha todos os workitems de um projeto dentro de uma organização
        Args:
            org_name (str): Nome da organização a ser pesquisada.
            auth (str): String com a autorização para a chamada da API
            header (dict): dicionario contendo o header da chamada http
        """
        self.org_name = org_name
        self.auth = auth
        self.header = header

    #BUCAR PROJETOS DENTRO DE UMA ORG
    def listar_projetos(self)-> dict:
        """_summary_ 
        Retorna a listagem de todos os projetos dentro da organização passada como parâmetro.

        Returns:
            dict: Retorna um dicionário com os dados de todos os projetos encontrados
        """
        url_projects = f"https://dev.azure.com/{self.org_name}/_apis/projects?api-version=6.0"
        projects_return = requests.get(url_projects, auth=self.auth)
        if projects_return.status_code == 200:
            return projects_return.json()["value"]
        else:
                return f"Erro ao buscar lista de ORGs {self.org_name} \
                - Erro: {projects_return.status_code} - {projects_return.text}"

    #EXTRAIR AS ORGS
    def extrair_projetos(self, json:dict)->list:
        """_summary_
        Retorna uma lista com os nomes dos projetos encontrados no dicionário passado como parâmetro.
        Args:
            json (dict): Dicionário retornado pela função listar_projetos

        Returns:
            list: Lista com os nomes do projetos.
        """
        project_list = []
        for i in json:
            project_list.append(i["name"])
        if len(project_list) > 0:
            return project_list
        else:
            return "Não foi encontrado nenhum projeto"

    # BUSCAR  WORK ITENS DE UM PROJETO
    def listar_work_items(self, project:str)-> dict:
        """_summary_
        Traz a lista de work items de um projeto dentro de uma organização.
        
        Args:
            project (str): nome do projeto ao qual deseja retornar os work items

        Returns:
            dict: Dicionário com todos os workitems.
        """ 

        url = f"https://dev.azure.com/{self.org_name}/_apis/wit/wiql?api-version=6.0"
        body = {
        "query": f"""
        SELECT [System.Id], [System.WorkItemType], [System.Title]
        FROM workitemLinks
        WHERE 
            ([Source].[System.WorkItemType] = 'Epic')
            AND ([System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Forward')
            AND ([Source].[System.TeamProject] = '{project}')
        MODE (Recursive)
        """
    }
        response = requests.post(url, headers=self.header, json=body, auth=self.auth)
        if response.status_code == 200:
            return response.json()["workItemRelations"]
        else:
            return f"Erro ao buscar relacionamentos da ORG {self.org_name}\
            e do Projeto {project} - Erro: {response.status_code} - {response.text}"


    # EXTRAIR   WORK ITENS IDs DE UM PROJETO
    def extrair_workitems_id(self, json:dict)->list:
        """_summary_
        Retorna os ids de todos os workitems existentes em um projeto. Isso é feito através da leitura do json (retornado na função listar_work_items) passado com parâmetro.
        Args:
            json (dict): Retorno na função listar_work_items

        Returns:
            list: Lista com todos os ids dos workitems existentes no projeto
        """
        ids =set()
        for idx in json:
            source = idx.get("source")
            target = idx.get("target")

            if source  and "id" in source:
                ids.add(source["id"])
            if target and "id" in target:
                ids.add(target["id"])
            
        id_list= list(ids) 
        if len(id_list) > 0:
            return id_list
        else:
            return f"Não foram encontrados workitems IDs"
        
    #BUSCA OS DETALHES DOS WORKITEM
    def listar_detalhes_work_items(self, id_list:list, project:str)->dict:
        """_summary_
        Retorna os informações detalhadas de todos os workitems de um projeto.
        Args:
            id_list (list): Lista de ids retornada da funação extrair_workitems_id.
            project (str): Nome do projeto.

        Returns:
            dict: Dicionarios com todos os detalhes de cada workitem.
        """
        url = f"https://dev.azure.com/{self.org_name}/{project}/_apis/wit/workitemsbatch?api-version=6.0"
        body = {
            "ids": id_list,
        }

        response = requests.post(url, json=body, auth=self.auth, headers=self.header)
        if response.status_code == 200:
            return response.json()["value"]
        else:
            return f"Erro ao buscar os work items da org {self.org_name}\
            e do Projeto {project} - Erro: {response.status_code} - {response.text}"

    #ADICIONAR INFORMAÇÃO DO WORKITEM PAI NO JSON DE DETALHES
    def adicionar_dados_workitem_pai(self, work_items:dict, detail_work_items:dict)->dict:
        """_summary_
        Adiciona o id do workitem pai no json retornado na função listar_detalhes_work_items
        Args:
            work_items (dict): Json retornado na função listar_work_items
            detail_work_items (dict): Json retornado na função listar_detalhes_work_items

        Returns:
            dict: Json com a informação do Workitem id pai.
        """
        new_json = []
        for wi in detail_work_items:
            id = wi.get("id")
            for i in work_items:
            #print(id)
                if i["target"]["id"] == id:
                    id_father = i["source"]["id"] if i["source"] != None else None
                    wi["id_father"] = id_father
                    new_json.append(wi)
        return new_json