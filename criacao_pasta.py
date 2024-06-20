import os
import datetime
import pyodbc
import shutil
import smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
 
data_atual = datetime.now()
 
ServidorSaisa_SMTP  =   'novaquest-com-br.mail.protection.outlook.com'
usuario             =   'sistemas@novaquest.com.br'
senha               =   'd01@03@2023'
remetente           =   usuario
destinatario        =   'joao.reis@novaquest.com.br'
destinatario        =   'jefferson.pereira@novaquest.com.br'
 
def connect_smtp(servidor, usuario, senha):
	m = smtplib.SMTP(servidor, 25)
	m.starttls()
	# m.login(usuario, senha)
	return m
# -------------------------------------------------------------------------------------------------

server = '192.168.0.253'  # Nome ou endereço IP do servidor SQL Server
database = 'safra_teste'  # Nome do banco de dados
username = 'gpsouza'      # Nome de usuário para autenticação
password = 'gustavo@562'  # Senha para autenticação

conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# -------------------------------------------------------------------------------------------------

ano_atual = str(datetime.datetime.now().year)
meses = {
    "January": "01 - JANEIRO",
    "February": "02 - FEVEREIRO",
    "March": "03 - MARÇO",
    "April": "04 - ABRIL",
    "May": "05 - MAIO",
    "June": "06 - JUNHO",
    "July": "07 - JULHO",
    "August": "08 - AGOSTO",
    "September": "09 - SETEMBRO",
    "October": "10 - OUTUBRO",
    "November": "11 - NOVEMBRO",
    "December": "12 - DEZEMBRO",
}
dia_atual = datetime.datetime.now().strftime('%d')
mes_atual = meses[datetime.datetime.now().strftime('%B')]



destination_dir = r'\\192.168.0.48\Arquivos\PSA\RECEBIMENTOS\{}\{}\{}'.format(ano_atual, mes_atual, dia_atual)
destination_dir_processados = r'\\192.168.0.48\Arquivos\PSA\RECEBIMENTOS\{}\{}\{}\PROCESSADOS'.format(ano_atual, mes_atual, dia_atual)
NomeArquivo = os. listdir(destination_dir)


os.makedirs(destination_dir, exist_ok=True)

try:   
    cursor.execute("EXEC PROC_ANALITICO_STELANTES_RECEB")

    os.makedirs(destination_dir_processados, exist_ok=True)
    
    # mover o arquivo
    shutil.move(destination_dir + NomeArquivo,destination_dir_processados + NomeArquivo)
    
    def email():
        assunto = f'RPA - PROMESSAS/PAGAMENTO - ATUALIZADO - {data_atual.strftime("%d/%m/%Y")}'
        mensagem = f'''
    <html>
    <body>
    <p>Bom dia!</p>
    <p>HONORARIO ATUALIZADO.</p>
    <p>Atenciosamente,</p>
    
    <P>Nome do robo: STELANTES_HONORARIO<P>
    <p>Sistemas</p>
    </body>
    </html>
            '''
    
        e = connect_smtp(ServidorSaisa_SMTP, usuario, senha)
    
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto
    
        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)
    
        msgText = MIMEText(mensagem, 'html')
        msgAlternative.attach(msgText)
    
        e.sendmail(remetente, destinatario, msg.as_string())
        e.quit()
    
    
except:
    print (erro)
