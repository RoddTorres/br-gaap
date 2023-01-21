import os
import subprocess
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Carregando informações do arquivo .env
load_dotenv()

# Lendo as informações de conexão do banco de dados do arquivo .env
dbname = os.getenv('DB_NAME')
dbuser = os.getenv('DB_USER')
dbpassword = os.getenv('DB_PWD')

# Gerar nome do arquivo de backup com o nome do banco de dados e a data de criação
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_file = f'{dbname}_{now}.sql'

# Criando pasta de backup
backup_folder = 'Backup'
if not os.path.exists(backup_folder):
    os.mkdir(backup_folder)

# Comando para fazer backup do banco de dados
subprocess.call(['pg_dump', '-U', dbuser, '-Fp', '-b', '-v', '-f', os.path.join(backup_folder, backup_file), dbname])

print(f'Backup do banco de dados {dbname} criado com sucesso em {os.path.join(backup_folder, backup_file)}!')

# Enviando o arquivo de backup por email
from_email = os.getenv('EMAIL_USER')
to_email = os.getenv('EMAIL_DESTINATION')
password = os.getenv('EMAIL_PWD')

msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = "Banco de dados backup"

part = MIMEBase('application', "octet-stream")
part.set_payload(open(os.path.join(backup_folder, backup_file), "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(backup_file))
msg.attach(part)

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.login(from_email, password)
smtpObj.sendmail(from_email, to_email, msg.as_string())
smtpObj.quit()

print(f'Backup do banco de dados enviado para o email {to_email}')
