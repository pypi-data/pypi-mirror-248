import platform
import subprocess
import psutil
import GPUtil  # For GPU information

def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def get_system_info():
    system_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Processor": platform.processor(),
        "Architecture": platform.architecture(),
        "Memory (RAM)": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "Disk Usage": f"{psutil.disk_usage('/').total / (1024 ** 3):.2f} GB",
    }

    try:
        # GPU Information (using GPUtil library)
        gpus = GPUtil.getGPUs()
        gpu_info = [
            {"GPU": gpu.name, "Memory": f"{gpu.memoryTotal / 1024:.2f} GB"}
            for gpu in gpus
        ]
        system_info["GPUs"] = gpu_info
    except Exception as e:
        print(f"Failed to retrieve GPU information: {e}")

    try:
        # Detailed Hardware Information using systeminfo command
        hardware_info = run_command(["systeminfo"])
        system_info["Hardware Information"] = hardware_info
    except Exception as e:
        print(f"Failed to retrieve hardware information: {e}")

    try:
        # List installed drivers using driverquery command
        driver_info = run_command(["driverquery"])
        system_info["Installed Drivers"] = driver_info
    except Exception as e:
        print(f"Failed to retrieve driver information: {e}")

    return system_info

if __name__ == "__main__":
    specs = get_system_info()
    print(specs)

    for key, value in specs.items():
        print(f"{key}: {value}")