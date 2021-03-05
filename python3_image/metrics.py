import prometheus_client as prom
import random
import time
import shutil


if __name__ == '__main__':
   registry = prom.CollectorRegistry()
   total, used, free = shutil.disk_usage("/")
   gaugeT = prom.Gauge('Total_space', 'Total space on disk in byte', registry=registry)
   #gaugeT = prom.Gauge('Total_space', 'Total space on disk in byte')
   gaugeU = prom.Gauge('Used_space', 'Used space from disk in byte', registry=registry)
   #gaugeU = prom.Gauge('Used_space', 'Used space from disk in byte')
   while True:
       #prom.start_http_server(8001)
       gaugeT.set(total)
       gaugeU.set(used)
       prom.push_to_gateway('run_app:9091', job='microservice1', registry=registry)
       time.sleep(1)

