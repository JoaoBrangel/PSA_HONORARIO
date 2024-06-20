import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

data_atual = datetime.now()

ServidorSaisa_SMTP = 'novaquest-com-br.mail.protection.outlook.com'
remetente = 'vinicius@novaquest.com.br'
destinatario = 'joao.reis@novaquest.com.br'

def email_sem_auth():
    assunto = f'RPA - PROC_ANALITICO_STELANTES_RECEB - {data_atual.strftime("%d/%m/%Y")}'
    mensagem = '''
    <html>
    <body>
    <p>Bom dia!</p>
    <p>Todos os CPFs processados com sucesso.</p>
    <p>Atenciosamente,</p>
    <p>Sistemas</p>
    </body>
    </html>
    '''

    try:
        # Conectar ao servidor SMTP na porta padrão (25)
        e = smtplib.SMTP(ServidorSaisa_SMTP, 25)

        # Construir e enviar e-mail
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto

        msg.attach(MIMEText(mensagem, 'html'))

        e.sendmail(remetente, destinatario, msg.as_string())

        print("E-mail enviado com sucesso!")

    except Exception as ex:
        print(f"Erro ao enviar e-mail: {str(ex)}")

    finally:
        e.quit()  # Encerrar conexão com o servidor SMTP

# Chamar a função para enviar o e-mail sem autenticação
email_sem_auth()
