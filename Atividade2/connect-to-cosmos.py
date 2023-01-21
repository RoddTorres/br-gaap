import os
import json
import dotenv
import pandas as pd
import psycopg2
from azure.cosmos import CosmosClient, PartitionKey

#Busca dos parâmetros de conexão ao banco de dados PostgreSQL
dotenv.load_dotenv(dotenv.find_dotenv())
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DB_PORT = os.getenv("DB_PORT")
DB_HOST = os.getenv("DB_HOST")

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PWD, port=DB_PORT, host=DB_HOST)

results_from_query = pd.read_sql("SELECT * FROM categories", conn)
print(results_from_query)
results_json_file = results_from_query.to_json()
print(results_json_file)

with open('./Atividade2/backup_data.json', 'w') as fh:
    fh.write(results_json_file)

result = json.loads(results_json_file)
    
conn.close()

dotenv.load_dotenv(dotenv.find_dotenv())
endpoint = os.getenv("COSMOS_ENDPOINT")
cosmos_key = os.getenv("COSMOS_KEY")

client = CosmosClient(url=endpoint, credential=cosmos_key)

database = client.create_database_if_not_exists(id="sipef")


partitionKeyPath = PartitionKey(path="/categoryId")

container = database.create_container_if_not_exists(
    id="products", partition_key=partitionKeyPath
)

container.create_item(results_json_file)

# existingItem = container.read_item(
#     item="70b63682-b93a-4c77-aad2-65501347265f",
#     partition_key="61dba35b-4f02-45c5-b648-c6badc0cbd79",
# )

