import smtplib

s = smtplib.SMTP('smtp.gmail.com', 587)

mail_id = "Your Mail Id"
r_mail_id = "Receiver Mail Id"
password = "Your Password"

s.starttls()

s.login(mail_id, password)

message = 'Hi how are you?'

s.sendmail(mail_id, r_mail_id, message)

s.quit()
