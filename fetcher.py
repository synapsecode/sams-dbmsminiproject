import psutil
import platform
import subprocess
from datetime import datetime
import json
import schedule
import time
import random
import geocoder
import requests
import sys
import random

# SERVER = 'http://localhost:3000'
SERVER = 'https://dbms-miniproject.vercel.app'

def get_identifier():
    import platform
    import hashlib
    system_info = platform.uname()
    info_string = f"{system_info.system}-{system_info.node}-{system_info.release}-{system_info.version}-{system_info.machine}-{system_info.processor}"
    system_id = hashlib.sha256(info_string.encode()).hexdigest()
    return system_id

def get_external_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()  # Check if the request was successful
        ip_address = response.json()['ip']
        return ip_address
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def get_city():
    g = geocoder.ip('me')
    if g.ok:
        return g.city
    else:
        return None

def get_network_traffic():
    def get_network_usage():
        network_usage = psutil.net_io_counters(pernic=True)
        return network_usage
    network_before = get_network_usage()
    time.sleep(0.1)
    network_after = get_network_usage()
    SENT = 0
    RECX = 0
    for interface, before in network_before.items():
        after = network_after.get(interface, None)
        if after is not None:
            sent = after.bytes_sent - before.bytes_sent
            received = after.bytes_recv - before.bytes_recv
            SENT += sent
            RECX += received  
    return (SENT,RECX)

def get_metrics():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    temp = None
    if hasattr(psutil, 'sensors_temperatures'):
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                for entry in entries:
                    temp = entry.current

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sid = get_identifier()
    netusage = get_network_traffic()

    return {
        'sid': sid,
        'cpu':cpu, 
        'ram':ram, 
        'disk':disk, 
        'temp':temp,
        'network': netusage,
        'timestamp': ts,
    }

def create_log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        'desc': msg,
        'timestamp': ts,
        'id': str(uuid.uuid1()),
        'sid': get_identifier(),
        'action': '',
    }
    # send to backend

def create_alert(msg, typ):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = json.dumps({
        'desc': msg,
        'timestamp': ts,
        'sid': get_identifier(),
        'type': typ,
    })
    print(payload)
    resp = requests.post(f'{SERVER}/create_alert', json=payload)
    if(resp.status_code == 200):
        print('Alert Raised Successfully!')
    else:
        print(str(resp.content))

def register_server():
    sysname = platform.uname().node
    ip = get_external_ip()
    sid = get_identifier()
    city = get_city()
    payload = json.dumps({
        'server_name': sysname,
        'ip': ip,
        'sid': sid,
        'location': city,
    })
    resp = requests.post(f'{SERVER}/register_server', json=payload)
    if(resp.status_code == 200):
        print('Server Registered!')
    else:
        print(str(resp.content))

def job():
    metrics = get_metrics()
    # upload metrics to server

    # Alert Generation Code
    if(metrics['cpu'] > 70.0):
        create_alert(f"WARNING! HIGH USAGE DETECTED ({metrics['cpu']})", "CPU")
    elif(metrics['ram'] > 90.0):
        create_alert(f"WARNING! HIGH USAGE DETECTED ({metrics['ram']})", "RAM")
    elif(metrics['disk'] > 70.0):
        create_alert(f"WARNING! HIGH USAGE DETECTED ({metrics['disk']})", "DISK")

    resp = requests.post(f'{SERVER}/save_performance', json=json.dumps(metrics))
    if(resp.status_code == 200):
        print('Metrics Registered =>', metrics)
    else:
        print(str(resp.content))

def main():
    if(len(sys.argv) < 2):
        print('no argument')
        return
    arg = sys.argv[1]
    if(arg == 'register'):
        register_server()
    elif(arg == 'monitor'):
        INTERVAL = 5
        job()
        schedule.every(INTERVAL).seconds.do(job)
        while True:
            schedule.run_pending()
            time.sleep(1)

if(__name__ == '__main__'):
    main()