import time
import paramiko
import sys

nbytes = 4096
hostname = 'dgamonmdhds01.sl.bluecloud.ibm.com'
port = 22
username = 'airflow'
password = 'Dec19Dec@12345!'
command ='sh /home/dsadm/DataStage/MDHDEV/Script/run_datastage_script.sh MDHDEV Status_chk  /home/dsadm/DataStage/MDHDEV/data'
try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    print('Trying to Connect To Data Stage server')
    client.connect(hostname, port=port, username=username, password=password)
    print('Connected')
    print('running the job')
    stdin1, stdout1, stderr1 =client.exec_command('sh testrun.sh')
    print(stdout1.read())
    print('job ran')
finally:
    print('Clossing connection To Data Stage server')
    client.close()
