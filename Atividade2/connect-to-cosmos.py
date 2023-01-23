import os
import json
from sqlalchemy import create_engine
from azure.cosmos import CosmosClient, PartitionKey

#Busca dos parâmetros de conexão ao banco de dados PostgreSQL e CosmosDB em arquivo .env
dbname = os.getenv("DB_NAME")
dbuser = os.getenv("DB_USER")
dbpassword = os.getenv("DB_PWD")
dbhost = os.getenv("DB_HOST")
dbport = os.getenv("DB_PORT")
endpoint = os.getenv("COSMOS_ENDPOINT")
cosmos_key = os.getenv("COSMOS_KEY")

#Criar a engine PostgreSQL
pg_engine = create_engine(f'postgresql://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}')

#Busca dos dados na tabela Categories
pg_table = pg_engine.execute("SELECT * FROM categories").fetchall()

#Criar o objeto CosmosClient
client = CosmosClient(url=endpoint, credential=cosmos_key)

#Criar o banco de dados "sipef" e container "financeiro" no CosmosDB
database = client.create_database_if_not_exists(id="sipef")
key_path = PartitionKey(path="/logs")
container = database.create_container_if_not_exists(
    id="financeiro", partition_key=key_path, offer_throughput=400
)

#Mapear os campos obtidos pelo PostgreSQL, transformando-os em dicionário
def map_fields(row):
    mapped_fields = {}
    mapped_fields["category_name"] = row[1]
    mapped_fields["description"] = row[2]
    mapped_fields["picture"] = row[3]
    return mapped_fields

#Iterar pelas linhas da tabela PostgreSQL e adiocioná-las no CosmosDB
for row in pg_table:
    mapped_fields = map_fields(row)
    mapped_fields["id"] = json.dumps(row[0])
    container.create_item(mapped_fields)
    
print("Tabela adicionada no CosmosDB")
