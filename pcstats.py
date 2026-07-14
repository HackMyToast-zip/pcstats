import psutil
import time
import platform
import subprocess
import readchar
import os
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()
tab = 1


def size(bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024


def get_gpu():
    try:
        output = subprocess.check_output(["lspci"]).decode()
        for line in output.splitlines():
            if "VGA" in line or "3D" in line:
                return line.split(": ", 1)[-1]
    except:
        return "Unknown"

    return "Unknown"


def live_stats():
    table = Table(title="PC Stats - Live")

    table.add_column("Component")
    table.add_column("Value")

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    table.add_row("CPU Usage", f"{cpu}%")
    table.add_row("RAM Usage", f"{ram.percent}%")
    table.add_row("RAM Used", f"{size(ram.used)} / {size(ram.total)}")
    table.add_row("Disk Usage", f"{disk.percent}%")

    battery = psutil.sensors_battery()
    if battery:
        table.add_row("Battery", f"{battery.percent}%")

    temps = psutil.sensors_temperatures()
    if temps:
        for name, values in temps.items():
            if values:
                table.add_row("Temperature", f"{values[0].current}°C")
                break

    table.add_row(
        "Uptime",
        f"{int(time.time()-psutil.boot_time())//3600}h"
    )

    return table


def system_info():
    table = Table(title="PC Stats - System Info")

    table.add_column("Component")
    table.add_column("Value")

    table.add_row(
        "CPU",
        platform.processor() or "Unknown"
    )

    table.add_row(
        "CPU Cores",
        str(psutil.cpu_count())
    )

    table.add_row(
        "GPU",
        get_gpu()
    )

    ram = psutil.virtual_memory()
    table.add_row(
        "Total RAM",
        size(ram.total)
    )

    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            table.add_row(
                f"Drive {part.device}",
                size(usage.total)
            )
        except:
            pass

    table.add_row(
        "OS",
        platform.platform()
    )

    return table


def main():
    global tab

    with Live(refresh_per_second=2) as live:
        while True:
            os.system("clear")

            console.print(
                "[1] Live Stats   [2] Info   [q] Quit\n"
            )

            if tab == 1:
                live.update(live_stats())
            else:
                live.update(system_info())

            key = readchar.readkey()

            if key == "1":
                tab = 1
            elif key == "2":
                tab = 2
            elif key == "q":
                break


main()
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
