import os
import json
import dotenv
import pandas as pd
import psycopg2
from azure.cosmos import CosmosClient, PartitionKey

#Busca dos parâmetros de conexão ao banco de dados PostgreSQL
db_name = input("Digite o banco de dados desejado: ")
db_user = input("Digite o nome de usuário do banco de dados: ")
db_pwd = input("Digite a senha do banco de dados: ")
db_port = input("Digite a porta do banco de dados: ")
db_host = input("Digite o host: ")

try:
    #Criar conexão com o banco de dados
    conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pwd, port=db_port, host=db_host)

    #Consulta SQL que traz uma tabela do banco de dados 
    table_name = input("Digite o nome da tabela a ser consultada: ") #Vide arquivo northwind.sql. No exemplo a tabela foi categories
    results_from_query = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    print(results_from_query)
    results_json_file = results_from_query.to_json()
    print(results_json_file)

    with open('./Atividade2/backup_data.json', 'w') as fh:
        fh.write(results_json_file)

    result = json.loads(results_json_file)
        
except (Exception, psycopg2.DatabaseError) as error:
    print("Impossível conectar com o banco de dados")
finally:
    conn.close()


#Busca das variáveis do sistema
dotenv.load_dotenv(dotenv.find_dotenv())
endpoint = os.getenv("COSMOS_ENDPOINT")
cosmos_key = os.getenv("COSMOS_KEY")

#Criação de um cliente
client = CosmosClient(url=endpoint, credential=cosmos_key)

#Criação de banco de dados
database = client.create_database_if_not_exists(id="br_gaap")


partitionKeyPath = PartitionKey(path="/categoryId")

#Criação de um container
container = database.create_container_if_not_exists(
    id="products", partition_key=partitionKeyPath
)

container.create_item(results_json_file)

# existingItem = container.read_item(
#     item="70b63682-b93a-4c77-aad2-65501347265f",
#     partition_key="61dba35b-4f02-45c5-b648-c6badc0cbd79",
# )

