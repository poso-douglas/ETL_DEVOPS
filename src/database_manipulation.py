import sqlite3
from datetime import date, datetime
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE = os.getenv("DATABASE")

class Dados:
    def __init__(self, org_name:str):
        self.org_name = org_name

    def criar_tabela(self, table:str):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute((f"""
        CREATE TABLE IF NOT EXISTS {table}(
            id INTEGER
            ,date TEXT
            ,organization TEXT
            ,project TEXT
            ,id_father INTEGER
            ,rev INTEGER
            ,url TEXT
            ,AreaPath TEXT
            ,TeamProject TEXT
            ,IterationPath TEXT
            ,WorkItemType TEXT
            ,State TEXT
            ,Reason TEXT
            ,CreatedDate TEXT 
            ,CreatedBy_displayName TEXT
            ,CreatedBy_url TEXT
            ,CreatedBy_avatar TEXT
            ,CreatedBy_id TEXT
            ,CreatedBy_uniqueName TEXT
            ,CreatedBy_imageUrl TEXT
            ,CreatedBy_descriptor TEXT
            ,ChangedDate TEXT
            ,ChangedBy_displayName TEXT
            ,ChangedBy_url TEXT
            ,ChangedBy_avatar TEXT
            ,ChangedBy_id TEXT
            ,ChangedBy_uniqueName TEXT
            ,ChangedBy_imageUrl TEXT
            ,ChangedBy_descriptor TEXT
            ,CommentCount TEXT
            ,Title TEXT
            ,StateChangeDate TEXT
            ,Priority TEXT
            ,ValueArea TEXT
            ,Risk TEXT
            ,Effort TEXT
            ,Description TEXT  
            ,Datetime_injestion TEXT
            ,PRIMARY KEY (id, date, organization, project) 
        )
        """))

        conn.commit()
        conn.close()

    def inserir_dados(self,json:dict, project:str):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        for i in json:
            fields = i["fields"]
            table = fields.get("System.WorkItemType")
            cursor.execute(f"""
                INSERT INTO {table.replace(" ","_")} (
                                id
                                ,date
                                ,organization
                                ,project
                                ,id_father 
                                ,rev 
                                ,url 
                                ,AreaPath 
                                ,TeamProject 
                                ,IterationPath 
                                ,WorkItemType 
                                ,State 
                                ,Reason 
                                ,CreatedDate  
                                ,CreatedBy_displayName 
                                ,CreatedBy_url 
                                ,CreatedBy_avatar 
                                ,CreatedBy_id 
                                ,CreatedBy_uniqueName 
                                ,CreatedBy_imageUrl 
                                ,CreatedBy_descriptor 
                                ,ChangedDate 
                                ,ChangedBy_displayName 
                                ,ChangedBy_url 
                                ,ChangedBy_avatar 
                                ,ChangedBy_id 
                                ,ChangedBy_uniqueName 
                                ,ChangedBy_imageUrl 
                                ,ChangedBy_descriptor 
                                ,CommentCount 
                                ,Title 
                                ,StateChangeDate 
                                ,Priority 
                                ,ValueArea 
                                ,Risk 
                                ,Effort 
                                ,Description
                                ,Datetime_injestion 
                        )
                VALUES (? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? 
                        ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?,?)
                """,
                (
                    i["id"]
                    ,date.today().isoformat()
                    ,self.org_name
                    ,project
                    ,i["id_father"]
                    ,i["rev"] 
                    ,i["url"] 
                    ,fields.get("System.AreaPath")
                    ,fields.get("System.TeamProject")
                    ,fields.get("System.IterationPath") 
                    ,fields.get("System.WorkItemType") 
                    ,fields.get("System.State") 
                    ,fields.get("System.Reason") 
                    ,fields.get("System.CreatedDate")  
                    ,fields.get("System.CreatedBy", {}).get("displayName") 
                    ,fields.get("System.CreatedBy", {}).get("url") 
                    ,fields.get("System.CreatedBy", {}).get("_links", {}).get("avatar", {}).get("href") 
                    ,fields.get("System.CreatedBy", {}).get("id") 
                    ,fields.get("System.CreatedBy", {}).get("uniqueName") 
                    ,fields.get("System.CreatedBy", {}).get("imageUrl") 
                    ,fields.get("System.CreatedBy", {}).get("descriptor") 
                    ,fields.get("System.ChangedDate") 
                    ,fields.get("System.ChangedBy", {}).get("displayName")
                    ,fields.get("System.ChangedBy", {}).get("url") 
                    ,fields.get("System.ChangedBy", {}).get("_links", {}).get("avatar", {}).get("href")
                    ,fields.get("System.ChangedBy", {}).get("id") 
                    ,fields.get("System.ChangedBy", {}).get("uniqueName") 
                    ,fields.get("System.ChangedBy", {}).get("imageUrl") 
                    ,fields.get("System.ChangedBy", {}).get("descriptor") 
                    ,fields.get("System.CommentCount")
                    ,fields.get("System.Title") 
                    ,fields.get("Microsoft.VSTS.Common.StateChangeDate") 
                    ,fields.get("Microsoft.VSTS.Common.Priority")
                    ,fields.get("Microsoft.VSTS.Common.ValueArea") 
                    ,fields.get("Microsoft.VSTS.Common.Risk") 
                    ,fields.get("Microsoft.VSTS.Common.Effort") 
                    ,fields.get("System.Description")
                    ,datetime.now().isoformat(sep= ' ')
                )
            )
        conn.commit()
        conn.close()