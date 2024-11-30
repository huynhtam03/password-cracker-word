import psutil
import GPUtil
import platform

def display_cpu_and_gpu_info():
    """Display CPU and GPU information in a simplified way."""
    # Get CPU information
    cpu_name = platform.processor() if platform.processor() else "Unknown CPU"
    cpu_cores = psutil.cpu_count(logical=False)  # Physical cores
    cpu_threads = psutil.cpu_count(logical=True)  # Logical threads
    cpu_freq = psutil.cpu_freq(percpu=False).max  # Max frequency in MHz
    cpu_load = psutil.cpu_percent(interval=1)  # CPU load percentage over 1 second

    # Display CPU information
    print(f"CPU: {cpu_name}")
    print(f"  Cores: {cpu_cores} | Threads: {cpu_threads}")
    print(f"  Max Frequency: {cpu_freq} MHz")

    # Get GPU information (if available)
    gpus = GPUtil.getGPUs()
    if gpus:
        for gpu in gpus:
            print(f"GPU {gpu.id}: {gpu.name}")
            print(f"  Memory Used: {gpu.memoryUsed} MB / {gpu.memoryTotal} MB")
    else:
        print("No GPU detected.")
