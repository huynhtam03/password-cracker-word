import psutil
import GPUtil
import platform

def display_cpu_and_gpu_info():
    """Hiển thị thông tin CPU và GPU theo cách đơn giản."""
    # Lấy thông tin CPU
    cpu_name = platform.processor() if platform.processor() else "CPU không xác định"
    cpu_cores = psutil.cpu_count(logical=False)  # Số lõi vật lý
    cpu_threads = psutil.cpu_count(logical=True)  # Số luồng logic
    cpu_freq = psutil.cpu_freq(percpu=False).max  # Tần số tối đa (MHz)

    # Hiển thị thông tin CPU
    print(f"CPU: {cpu_name}")
    print(f"  Số lõi: {cpu_cores} | Số luồng: {cpu_threads}")
    print(f"  Tần số tối đa: {cpu_freq} MHz")

    # Lấy thông tin GPU (nếu có)
    gpus = GPUtil.getGPUs()
    if gpus:
        for gpu in gpus:
            print(f"GPU {gpu.id}: {gpu.name}")
            print(f"  Bộ nhớ sử dụng: {gpu.memoryUsed} MB / {gpu.memoryTotal} MB")
    else:
        print("Không phát hiện GPU.")
