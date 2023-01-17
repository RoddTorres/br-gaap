import pandas as pd
import psycopg2
import json
import win32com.client as win32

#Busca dos parâmetros de conexão ao banco de dados PostgreSQL
db_name = input("Digite o banco de dados desejado: ")
db_user = input("Digite o nome de usuário do banco de dados: ")
db_pwd = input("Digite a senha do banco de dados: ")
db_port = input("Digite a porta do banco de dados: ")
db_host = input("Digite o host: ")

#Criar conexão com o banco de dados
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pwd, port=db_port, host=db_host) 
#Opção 2: ler dados acima através de um arquivo externo para proteção dos dados.

#Consulta SQL que traz uma tabela do banco de dados 
results_from_query = pd.read_sql("SELECT * FROM categories", conn)
print(results_from_query)

# table_names_query = pd.read_sql("SELECT tablename FROM pg_tables WHERE schemaname = 'public'", conn)
# print(table_names_query)

#Conversão do Dataframe para Json
results_json_file = results_from_query.to_json()

#Criar arquivo .json
with open('./Atividade1/backup_data.json', 'w') as fh:
    fh.write(results_json_file)

conn.close()

#Envio de um email com anexo
outlook = win32.Dispatch('outlook.application')

email = outlook.CreateItem(0)

email.To = "rtsouza87@gmail.com"
email.Subject = "Backup BD"
email.HTMLBody = """
<p>Bom dia<p>

<p>Segue backup em anexo<p>

<p>Atenciosamente<p>
"""
anexo = "./Atividade1/backup_data.json'"
email.Attachments.Add(anexo)

email.Send()
print("Email enviado")


