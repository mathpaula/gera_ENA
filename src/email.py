import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

msg = MIMEMultipart()
msg['Subject'] = 'Testecito'
msg['From'] = "skoposbot@gmail.com"
msg['To'] = COMMASPACE.join( ["henrique.calogeras@skoposenergia.com.br", "daniel.mazucanti@skoposenergia.com.br"])

txt = MIMEText('Segue anexo o gráfico da ENA dos últimos 15 dias por submercado')
msg.attach(txt)

with open('../ena.png', 'rb') as fp:
    img = MIMEImage(fp.read())
msg.attach(img)

server = smtplib.SMTP("smtp.gmail.com")
server.connect("smtp.gmail.com", 587)
server.starttls()
server.login("skoposbot", 'bipbopimabot')
server.send_message(msg)
server.quit()