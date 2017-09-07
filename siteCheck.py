#for reference this is a python3 script and will not work with old version 2.7
#you need to install paramiko using pip3 for this to work (it is the ssh library used) / No idea how to do it on windows but I know it can be done. 
#********the bottom of the iceberg**********
from urllib.request import urlopen
from time import sleep
from paramiko import client


#email variables change the items below between the <> to what you need/want
e_username='<email username>'
e_password='<email password>'
email_address='<email address>'
site='<http://site to check>'
subject='<subject line you want>'
message='<tell them what you think, no wait just put your message here.>'

#power device to reboot if in accessable variables / change these also to what is needed for ssh
p_ip='<ip address to use for ssh >'
p_username='<ssh username to use>'
p_password='<ssh password for user>'



#don't mess with anything below unless you know what you are doing, one exception might be to change email if you don't want to use gmail but then you get to test it!
#email alert function 
def send_alert():
    from smtplib import SMTP
    from email.mime.text import MIMEText

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = email_address
    #I used Gmail here so here you go! you will have to allow "less secure apps" in gmail settings for this to work like you do for Microsoft outlook
    #if you choose to use something else good luck! ;) 
    server = SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(e_username, e_password)
    server.sendmail(email_address, [email_address], msg.as_string())
    server.quit()

#ssh class for connecting with power controller (mfi) and then issuing command to reboot
class ssh:
    client = None
 
    def __init__(self, address, username, password):
        print("Connecting to server.")
        self.client = client.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
 
    def sendCommand(self, command):
        if(self.client):
            stdin, stdout, stderr = self.client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                # Print data when available
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata
 
                    print(str(alldata, "utf8"))
        else:
            print("Connection not opened.")
            
#*************actual work being done (the top of the iceberg)**********
while True:
  try:
      urlopen(site)
      print ("OK")
  except:
      send_alert()
      #ssh into power controller and issue poweroff and wait 10 seconds then power on
      connection = ssh(p_ip, p_username, p_password)
      connection.sendCommand("echo 0 > /proc/power/relay1 && sleep 10 && echo 1 > /proc/power/relay1")
  sleep(600)
