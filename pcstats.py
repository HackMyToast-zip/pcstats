import psutil
import time
import platform
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()

def get_size(bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024

def create_table():
    table = Table(title="PC Stats Dashboard")

    table.add_column("Component")
    table.add_column("Value")

    # CPU
    table.add_row(
        "CPU Usage",
        f"{psutil.cpu_percent()}%"
    )

    # CPU info
    table.add_row(
        "CPU Cores",
        f"{psutil.cpu_count(logical=True)} threads"
    )

    # RAM
    ram = psutil.virtual_memory()
    table.add_row(
        "RAM",
        f"{ram.percent}% ({get_size(ram.used)} / {get_size(ram.total)})"
    )

    # Disk
    disk = psutil.disk_usage("/")
    table.add_row(
        "Disk",
        f"{disk.percent}% ({get_size(disk.used)} / {get_size(disk.total)})"
    )

    # Network
    net = psutil.net_io_counters()
    table.add_row(
        "Network Sent",
        get_size(net.bytes_sent)
    )
    table.add_row(
        "Network Received",
        get_size(net.bytes_recv)
    )

    # Battery
    battery = psutil.sensors_battery()
    if battery:
        table.add_row(
            "Battery",
            f"{battery.percent}%"
        )

    # Temperature
    temps = psutil.sensors_temperatures()
    if temps:
        for name, entries in temps.items():
            if entries:
                table.add_row(
                    "Temperature",
                    f"{entries[0].current}°C ({name})"
                )
                break

    # System
    table.add_row(
        "System",
        f"{platform.system()} {platform.release()}"
    )

    # Uptime
    uptime = int(time.time() - psutil.boot_time())
    hours = uptime // 3600
    minutes = (uptime % 3600) // 60

    table.add_row(
        "Uptime",
        f"{hours}h {minutes}m"
    )

    return table


with Live(create_table(), refresh_per_second=1) as live:
    while True:
        live.update(create_table())
        time.sleep(1)
