import smtplib
from email.mime.text import MIMEText

msg = MIMEText("Someone just poured: ##oz")
msg['Subject'] = "Keg Info"
msg['From'] = 'Keg@vassallo.ca'
msg['To'] = '7053801137@msg.telus.com'

try:
  s = smtplib.SMTP('smtp.gmail.com:587')
  s.ehlo()
  s.starttls()
  s.login('fenix.jyinaer@gmail.com', 'Vassallo4460')
  s.sendmail(msg['From'], msg['To'], msg.as_string())
  s.quit()
except:
  print('Text Message Failed')