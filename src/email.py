import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

msg = MIMEMultipart()
msg['Subject'] = 'Relatório'
msg['From'] = "skoposbot@gmail.com"
msg['To'] = COMMASPACE.join( ["henrique.calogeras@skoposenergia.com.br", 
   "lucas.vallim@skoposenergia.com.br", "daniel.mazucanti@skoposenergia.com.br"])

txt = MIMEText('Segue ENA por submercado em anexo')
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