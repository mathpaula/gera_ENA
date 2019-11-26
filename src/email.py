import smtplib
from pathlib import Path
#import base64
from email import encoders
#from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

msg = MIMEMultipart()

local = Path('../ex_csv/ENA/ENA_Sub_Mer.xls')
with open(local, 'rb') as fp:
    ena_s = MIMEBase('application', 'vnd.ms-excel')
    ena_s.set_payload(fp.read())

encoders.encode_base64(ena_s)
ena_s.add_header('placeholder', 'attachment', filename='ENA_Sub_Mer.xls')
msg.attach(ena_s)    

local = Path('../ex_csv/ENA/ENA_Bacias.xls')
with open(local, 'rb') as fp:
    ena_b = MIMEBase('application', 'vnd.ms-excel')
    ena_b.set_payload(fp.read())

encoders.encode_base64(ena_b)
ena_s.add_header('placeholder', 'attachment', filename='ENA_Bacias.xls')
msg.attach(ena_b)   

local = Path('../ex_csv/ENA/ENA_REE.xls')
with open(local, 'rb') as fp:
    ena_r = MIMEBase('application', 'vnd.ms-excel')
    ena_r.set_payload(fp.read())

encoders.encode_base64(ena_r)
ena_s.add_header('placeholder', 'attachment', filename='ENA_REE.xls')
msg.attach(ena_r)   
    
msg['Subject'] = 'Relatório'
msg['From'] = "skoposbot@gmail.com"
msg['To'] = COMMASPACE.join( ["daniel.mazucanti@skoposenergia.com.br"])


server = smtplib.SMTP("smtp.gmail.com")
server.connect("smtp.gmail.com", 587)
server.starttls()
server.login("skoposbot", 'bipbopimabot')
server.send_message(msg)
server.quit()