# agent/main.py
import psutil
import time
import json
from datetime import datetime

def get_metrics(server_id="host-local"):
    cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
    cpu_total = psutil.cpu_percent(interval=None)
    vm = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    return {
        "server_id": server_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "cpu": {
            "total_percent": cpu_total,
            "per_core": cpu_per_core
        },
        "memory": {
            "total_mb": vm.total // (1024*1024),
            "used_mb": vm.used // (1024*1024),
            "percent": vm.percent
        },
        "disk": {
            "total_gb": disk.total // (1024*1024*1024),
            "used_gb": disk.used // (1024*1024*1024),
            "used_percent": disk.percent
        },
        "net": {
            "sent_bytes": net.bytes_sent,
            "recv_bytes": net.bytes_recv
        }
    }

if __name__ == "__main__":
    server_id = "host-local"   # cambiá si querés
    while True:
        m = get_metrics(server_id)
        print(json.dumps(m, indent=None))
        time.sleep(1)
