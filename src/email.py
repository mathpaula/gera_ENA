import smtplib
from email.mime.text import MIMEText

COMMASPACE = ', '

with open('../relat_ena.html') as fp:
    msg = MIMEText(fp.read(), 'html')
    
msg['Subject'] = 'Relatório'
msg['From'] = "skoposbot@gmail.com"
msg['To'] = COMMASPACE.join( ["daniel.mazucanti@skoposenergia.com.br"])


server = smtplib.SMTP("smtp.gmail.com")
server.connect("smtp.gmail.com", 587)
server.starttls()
server.login("skoposbot", 'bipbopimabot')
server.send_message(msg)
server.quit()