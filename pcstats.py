import psutil
import time
import platform
import subprocess
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()

old_net = psutil.net_io_counters()

def size(bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024

def get_cpu():
    return platform.processor() or "Unknown"

def get_gpu():
    try:
        result = subprocess.check_output(
            ["lspci"]
        ).decode()

        for line in result.splitlines():
            if "VGA" in line or "3D" in line:
                return line.split(": ", 1)[-1]
    except:
        pass

    return "Unknown"

def dashboard():
    global old_net

    table = Table(title="PC Stats Dashboard v1.2")

    table.add_column("Component")
    table.add_column("Value")

    cpu = psutil.cpu_percent()
    freq = psutil.cpu_freq()

    table.add_row("CPU", get_cpu())
    table.add_row("CPU Usage", f"{cpu}%")

    if freq:
        table.add_row(
            "CPU Speed",
            f"{freq.current/1000:.2f} GHz"
        )

    table.add_row(
        "GPU",
        get_gpu()
    )

    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()

    table.add_row(
        "RAM",
        f"{ram.percent}% ({size(ram.used)}/{size(ram.total)})"
    )

    table.add_row(
        "Swap",
        f"{swap.percent}%"
    )

    disk = psutil.disk_usage("/")
    table.add_row(
        "Disk",
        f"{disk.percent}% ({size(disk.used)}/{size(disk.total)})"
    )

    net = psutil.net_io_counters()

    upload = net.bytes_sent - old_net.bytes_sent
    download = net.bytes_recv - old_net.bytes_recv

    old_net = net

    table.add_row(
        "Upload",
        f"{size(upload)}/s"
    )

    table.add_row(
        "Download",
        f"{size(download)}/s"
    )

    battery = psutil.sensors_battery()
    if battery:
        table.add_row(
            "Battery",
            f"{battery.percent}%"
        )

    temps = psutil.sensors_temperatures()
    if temps:
        for name, values in temps.items():
            if values:
                table.add_row(
                    "Temp",
                    f"{values[0].current}°C"
                )
                break

    uptime = int(time.time() - psutil.boot_time())
    table.add_row(
        "Uptime",
        f"{uptime//3600}h {(uptime%3600)//60}m"
    )

    table.add_row(
        "Kernel",
        platform.release()
    )

    return table


with Live(dashboard(), refresh_per_second=1) as live:
    while True:
        live.update(dashboard())
        time.sleep(1)    temps = psutil.sensors_temperatures()
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
