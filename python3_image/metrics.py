import prometheus_client as prom
import time
import paramiko


def connect_to_host(host, username):
    user = username
    port = 22
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, port=port)
        stdin, stdout, stderr = client.exec_command('df -k')
        data = stdout.read()
        lines = (str(data).split('\\n'))
        client.close()
        for line in lines:
            if len(line.split()) == 6:
                fsys = line.split()[0]
                full_size = int(line.split()[1]) * 1024
                used_space = int(line.split()[2]) * 1024
                mount = line.split()[-1]
                push_metrics(host, str(fsys), full_size, used_space, str(mount))
    except Exception as e:
        print(e)


def push_metrics(host, fsys, full_size, used_space, mount):
   registry = prom.CollectorRegistry()
   gaugeT = prom.Gauge('Total_space', 'Total space on disk in byte', registry=registry)
   gaugeU = prom.Gauge('Used_space', 'Used space from disk in byte', registry=registry)
   gaugeT.set(full_size)
   gaugeU.set(used_space)
   prom.push_to_gateway('run_app:9091', job=host+' Filesystem: ' + fsys + ' ,Mount '+ mount, registry=registry)


if __name__ == '__main__':
    host = '10.0.2.106'
    username = 'root'
    while True:
        connect_to_host(host, username)
        time.sleep(5)





