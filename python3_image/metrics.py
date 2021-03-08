import prometheus_client as prom
import time
import os
import paramiko
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s : %(levelname)s : %(message)s', filename='metrics.log')


def connect_to_host(host, username, push_to):
    user = username
    port = 22
    try:
        logging.info('Connect start')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, port=port)
        stdin, stdout, stderr = client.exec_command('df -k')
        data = stdout.read()
        lines = (str(data).split('\\n'))
        client.close()
        logging.info('Connect end')
        for line in lines:
            if len(line.split()) == 6:
                fsys = line.split()[0]
                full_size = int(line.split()[1]) * 1024
                used_space = int(line.split()[2]) * 1024
                mount = line.split()[-1]
                push_metrics(push_to, host, str(fsys), full_size, used_space, str(mount))
            time.sleep(1)
    except Exception as e:
        logging.info(str(e))


def push_metrics(push_to, host, fsys, full_size, used_space, mount):
   registry = prom.CollectorRegistry()
   gaugeT = prom.Gauge('Total_space', 'Total space on disk in byte', registry=registry)
   gaugeU = prom.Gauge('Used_space', 'Used space from disk in byte', registry=registry)
   gaugeT.set(full_size)
   gaugeU.set(used_space)
   logging.info(type(push_to))
   logging.info('push_to ' + str(push_to))
   prom.push_to_gateway(push_to, job=host+' Filesystem: ' + fsys + ' ,Mount '+ mount, registry=registry)
   logging.info('ok')


if __name__ == '__main__':
    while True:
        try:
            PATH = os.getcwd()
            f = open(PATH + '/settings/hosts.conf', encoding='utf-8')
            lines = f.readlines()
            for line in lines:
                push_to = line.split('|')[0]
                host = line.split('|')[1]
                username = line.split('|')[-1]
                connect_to_host(host, username, push_to)
                time.sleep(10)
        except FileNotFoundError:
            logging.info('No such file or directory')





