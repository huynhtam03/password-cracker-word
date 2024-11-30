import io
import sys
import string
import itertools
import argparse
import os
import psutil
import pyfiglet
from doc97 import Doc97File
from xor_obfuscation import DocumentXOR
import exceptions
import colorama
from functools import partial
from colorama import Fore, Style
from multiprocessing import Pool, Manager, Lock, cpu_count
from io import BytesIO
from multiprocessing import shared_memory
from monitor_resources import display_cpu_and_gpu_info
import threading
import time

# Khởi tạo colorama
colorama.init(autoreset=True)

# Định nghĩa các màu sắc
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
WHITE = Fore.WHITE
RESET = Style.RESET_ALL

# Các hàm tiện ích
def init_worker_shared_memory(shm_name, size, current_password_dict):
    """Khởi tạo bộ nhớ chia sẻ cho worker."""
    global shm
    shm = shared_memory.SharedMemory(name=shm_name)
    global global_doc_data
    global_doc_data = shm.buf[:size]
    global current_password
    current_password = current_password_dict

def display_logo():
    """Hiển thị logo và thông tin đóng góp."""
    logo = pyfiglet.figlet_format("HIHI")
    print(f"{MAGENTA}{logo}{RESET}", end="")
    contributors = [
        ("Huỳnh Thanh Tâm", "2033210951", "12DHBM08"),
        ("Nguyễn Đặng Ngân Hà", "2033216400", "12DHBM03"),
        ("Nguyễn Ngọc Thiên Phước", "2033216522", "12DHBM03")
    ]
    for name, student_id, class_id in contributors:
        print(f"{CYAN}{name:<25} - {student_id:<10} - {class_id}{RESET}")

def display_help():
    """Hiển thị hướng dẫn cho CLI."""
    help_text = f"""
    {CYAN}Hướng dẫn sử dụng:{RESET}

    1. Kiểm tra mã hóa:
    python cli.py /path/to/file.doc --check

    2. Giải mã với mật khẩu:
    python cli.py /path/to/file.doc --password "your_password" --output /path/to/decrypted_file.doc

    3. Giải mã với wordlist:
    python cli.py /path/to/file.doc --wordlist /path/to/wordlist.txt --output /path/to/decrypted_file.doc

    4. Sinh mật khẩu phức tạp:
    python cli.py /path/to/file.doc --generate-passwords --output /path/to/decrypted_file.doc
    """
    print(help_text)

# Kiểm tra mã hóa
def check_encryption(file_path):
    """Kiểm tra xem tệp có mã hóa không."""
    try:
        with open(file_path, "rb") as f:
            doc = Doc97File(f)
            return doc.is_encrypted()
    except Exception:
        return False

# Giải mã với mật khẩu
def decrypt_file(password, output_path, found, lock, current_password_dict):
    """Cố gắng giải mã tệp với mật khẩu đã cung cấp."""
    if found.value:
        return None  # Dừng nếu mật khẩu đã được tìm thấy
    try:
        with lock:
            current_password_dict['password'] = password

        # Sử dụng bộ nhớ chia sẻ cho dữ liệu tệp
        data = global_doc_data
        with BytesIO(data) as f:
            doc = Doc97File(f)
            if password:
                doc.load_key(password=password)

            with open(output_path, "wb") as outfile:
                doc.decrypt(outfile)

        with lock:
            print(f"\n{GREEN}File đã được giải mã và lưu tại {output_path}{RESET}")
            found.value = True
        return password
    except (exceptions.InvalidKeyError, exceptions.DecryptionError):
        return None
    except (IOError, OSError) as e:
        with lock:
            print(f"{RED}\nLỗi I/O khi giải mã: {e}{RESET}")
        return None
    except Exception as e:
        with lock:
            print(f"{RED}\nLỗi không mong đợi: {e}{RESET}")
        return None

# Sinh mật khẩu phức tạp và xử lý wordlist
def generate_complex_passwords(max_length=None, wordlist=None):
    """Sinh mật khẩu phức tạp hoặc sử dụng wordlist."""
    if wordlist:
        try:
            with open(wordlist, 'r', encoding='utf-8') as f:
                for line in f:
                    password = line.strip()
                    if password:
                        yield password
        except FileNotFoundError:
            print(f"{RED}File wordlist không tồn tại: {wordlist}{RESET}")
            return
    elif max_length:
        chars = string.digits + string.ascii_letters + string.punctuation
        for length in range(1, max_length + 1):
            for password_tuple in itertools.product(chars, repeat=length):
                yield ''.join(password_tuple)
    else:
        print(f"{RED}Cần cung cấp wordlist hoặc max_length để sinh mật khẩu.{RESET}")
        return

def count_total_passwords(max_length=None, wordlist=None):
    """Đếm tổng số mật khẩu từ wordlist hoặc max_length."""
    if wordlist:
        try:
            with open(wordlist, 'r', encoding='utf-8') as f:
                return sum(1 for line in f if line.strip())
        except FileNotFoundError:
            print(f"{RED}File wordlist không tồn tại: {wordlist}{RESET}")
            return 0
    elif max_length:
        chars = string.digits + string.ascii_letters + string.punctuation
        return sum(len(chars) ** length for length in range(1, max_length + 1))
    return 0

# Hiển thị mật khẩu hiện tại
def display_current_password(current_password_dict, lock, stop_event, start_time):
    """Luồng hiển thị mật khẩu và thời gian đã trôi qua."""
    last_displayed = ""
    while not stop_event.is_set():
        cpu_load = psutil.cpu_percent(interval=0.1)  # Lấy tải CPU nhanh chóng

        with lock:
            current_password = current_password_dict.get('password', '')

        if current_password != last_displayed:
            elapsed_time = time.time() - start_time
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            print(f"\r{YELLOW}Đang thử mật khẩu: {current_password:<30} | CPU Load: {cpu_load:.1f}% | Thời gian: {formatted_time}{RESET} ", end="")
            last_displayed = current_password

        time.sleep(0.1)

# Đa xử lý giải mã
def try_passwords_multiprocessing(password_generator, total_passwords, output_path, file_path, num_processes=None):
    """Cố gắng giải mã mật khẩu song song sử dụng đa xử lý."""
    if num_processes is None:
        num_processes = cpu_count()

    manager = Manager()
    found = manager.Value('b', False)
    lock = manager.Lock()
    current_password_dict = manager.dict()

    with open(file_path, "rb") as f:
        file_data = f.read()

    shm = shared_memory.SharedMemory(create=True, size=len(file_data))
    shm.buf[:] = file_data

    # Khởi động luồng hiển thị
    start_time = time.time()
    stop_event = threading.Event()
    display_thread = threading.Thread(target=display_current_password, args=(current_password_dict, lock, stop_event, start_time))
    display_thread.start()

    try:
        decrypt_partial = partial(decrypt_file, output_path=output_path, found=found, lock=lock, current_password_dict=current_password_dict)

        with Pool(processes=num_processes, initializer=init_worker_shared_memory, initargs=(shm.name, len(file_data), current_password_dict)) as pool:
            results = pool.imap_unordered(decrypt_partial, password_generator)

            for result in results:
                if result:
                    print(f"\n{GREEN}File đã được giải mã thành công với mật khẩu: {result}{RESET}")
                    found.value = True
                    pool.terminate()
                    pool.join()
                    break
    finally:
        shm.close()
        shm.unlink()
        stop_event.set()
        display_thread.join()

    if not found.value:
        print(f"\n{YELLOW}Không tìm thấy mật khẩu đúng trong danh sách.{RESET}")

# Hàm giải mã cho CLI
def decrypt_using_wordlist(file_path, wordlist_path, output_path):
    """Giải mã tệp sử dụng wordlist mật khẩu."""
    try:
        password_generator = generate_complex_passwords(wordlist=wordlist_path)
        total_passwords = count_total_passwords(wordlist=wordlist_path)
        if total_passwords == 0:
            return
        try_passwords_multiprocessing(password_generator, total_passwords, output_path, file_path)
    except FileNotFoundError:
        print(f"{RED}File wordlist không tồn tại: {wordlist_path}{RESET}")
    except Exception as e:
        print(f"{RED}Lỗi khi đọc wordlist: {e}{RESET}")

def decrypt_generate_full_complex_passwords(file_path, output_path, max_length):
    """Sinh mật khẩu phức tạp và cố gắng giải mã."""
    password_generator = generate_complex_passwords(max_length=max_length)
    total_passwords = count_total_passwords(max_length=max_length)
    if total_passwords == 0:
        print(f"{RED}Không thể tạo mật khẩu phức tạp.{RESET}")
        return
    try_passwords_multiprocessing(password_generator, total_passwords, output_path, file_path)

# Hàm chính
def main():
    """Điểm vào chính cho CLI."""
    display_logo()

    display_cpu_and_gpu_info()

    # Cấu hình parser CLI
    parser = argparse.ArgumentParser(description="Giải mã file MS DOC97.")
    parser.add_argument("file", help="Đường dẫn tới file .doc", nargs="?")
    parser.add_argument("--password", help="Mật khẩu để giải mã file")
    parser.add_argument("--check", action="store_true", help="Kiểm tra mã hóa")
    parser.add_argument("--output", help="Đường dẫn để lưu file đã giải mã")
    parser.add_argument("--wordlist", help="Danh sách mật khẩu từ file")
    parser.add_argument("--generate-passwords", action="store_true", help="Sinh mật khẩu phức tạp")

    parser_args = parser.parse_args()

    if not parser_args.file or not os.path.exists(parser_args.file):
        display_help()
        sys.exit(1)

    try:
        is_encrypted = check_encryption(parser_args.file)

        if not is_encrypted:
            print(f"{RED}Tệp không được mã hóa. Không cần giải mã.{RESET}")
            return

        if parser_args.check:
            print(f"{GREEN}Tệp có mã hóa: {is_encrypted}{RESET}")
            return

        if parser_args.generate_passwords and parser_args.output:
            max_length = int(input("Nhập độ dài tối đa của mật khẩu: "))
            decrypt_generate_full_complex_passwords(parser_args.file, parser_args.output, max_length)

        elif parser_args.password and parser_args.output:
            try:
                with open(parser_args.file, "rb") as f:
                    file_data = f.read()

                with BytesIO(file_data) as f:
                    doc = Doc97File(f)
                    doc.load_key(password=parser_args.password)

                    with open(parser_args.output, "wb") as outfile:
                        doc.decrypt(outfile)

                print(f"\n{GREEN}File đã được giải mã thành công với mật khẩu: {parser_args.password}{RESET}")
            except exceptions.InvalidKeyError:
                print(f"\n{RED}Mật khẩu không hợp lệ hoặc lỗi khi giải mã.{RESET}")
            except exceptions.DecryptionError as e:
                print(f"\n{RED}Lỗi khi giải mã: {e}{RESET}")
            except (IOError, OSError) as e:
                print(f"{RED}\nLỗi I/O khi giải mã: {e}{RESET}")
            except Exception as e:
                print(f"{RED}\nLỗi không mong đợi: {e}{RESET}")

        elif parser_args.wordlist and parser_args.output:
            decrypt_using_wordlist(parser_args.file, parser_args.wordlist, parser_args.output)
        else:
            print(f"{RED}Để giải mã file, bạn cần cung cấp cả --password hoặc --wordlist và --output.{RESET}")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"{RED}\nQuá trình đã bị dừng bởi người dùng (Ctrl + C).{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()