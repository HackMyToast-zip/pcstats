import psutil
import time
from rich.console import Console
from rich.table import Table

console = Console()

while True:
    table = Table(title="PC Stats")

    table.add_column("Component")
    table.add_column("Value")

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    battery = psutil.sensors_battery()

    table.add_row("CPU", f"{cpu}%")
    table.add_row("RAM", f"{ram.percent}% ({ram.used // 1024**3}GB used)")
    table.add_row("Disk", f"{disk.percent}%")
    
    if battery:
        table.add_row("Battery", f"{battery.percent}%")

    table.add_row("Uptime", f"{time.time() - psutil.boot_time():.0f}s")

    console.clear()
    console.print(table)

    time.sleep(2)
