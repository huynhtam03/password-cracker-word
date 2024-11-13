import io
import argparse
import os
import sys
import itertools
import string
import pyfiglet  # Import pyfiglet for ASCII art generation
from doc97 import Doc97File  # Giả sử lớp của bạn nằm trong doc97file.py
import exceptions
import colorama
from functools import partial
from colorama import Fore, Back, Style
from xor_obfuscation import DocumentXOR  
from tqdm import tqdm  # Thêm tqdm cho thanh tiến trình

# Khởi tạo colorama để hỗ trợ màu sắc trên tất cả các nền tảng
colorama.init(autoreset=True)

# Định nghĩa màu sắc sử dụng mã ANSI cho một phong cách "hacker"
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
WHITE = Fore.WHITE
RESET = Style.RESET_ALL  # Đặt lại màu sắc về mặc định

def display_logo():
    """Hiển thị logo với tên 'THANH TAM' và mặt cười."""
    logo = pyfiglet.figlet_format("THANH TAM")  # Tạo ASCII art cho tên
    print(f"{MAGENTA}{logo}{RESET}")
    print(f"{YELLOW}😊{RESET}")  # Thêm mặt cười vào cuối logo

def display_help():
    """Hiển thị hướng dẫn sử dụng CLI với màu sắc."""
    help_text = f"""
    {CYAN}Hướng dẫn sử dụng công cụ giải mã MS DOC 97:{RESET}

    =========================================================
    1. Kiểm tra mã hóa của file
    ---------------------------------------------------------
    Sử dụng `--check` để kiểm tra mã hóa của file.
    Ví dụ: 
    ```bash
    python cli.py /path/to/file.doc --check
    ```

    =========================================================
    2. Giải mã file bằng mật khẩu
    ---------------------------------------------------------
    Cung cấp mật khẩu và đường dẫn đầu ra.
    Ví dụ: 
    ```bash
    python cli.py /path/to/file.doc --password "your_password" --output /path/to/decrypted_file.doc
    ```
    Tham số: `--password`, `--output`

    =========================================================
    3. Giải mã với wordlist (danh sách mật khẩu)
    ---------------------------------------------------------
    Cung cấp đường dẫn tới file wordlist.
    Ví dụ: 
    ```bash
    python cli.py /path/to/file.doc --wordlist /path/to/wordlist.txt --output /path/to/decrypted_file.doc
    ```

    =========================================================
    4. Giải mã với XOR
    ---------------------------------------------------------
    Giải mã bằng phương pháp XOR.
    Ví dụ: 
    ```bash
    python cli.py /path/to/file.doc --xor --password "your_password" --output /path/to/decrypted_file.doc
    ```

    =========================================================
    5. Sinh mật khẩu phức tạp để giải mã
    ---------------------------------------------------------
    Tạo và thử mật khẩu phức tạp.
    Ví dụ: 
    ```bash
    python cli.py /path/to/file.doc --generate-passwords --output /path/to/decrypted_file.doc
    ```

    =========================================================
    Các tham số:
    ---------------------------------------------------------
    - `file`: Đường dẫn tới file DOC 97 cần giải mã.
    - `--password`: Mật khẩu để giải mã file.
    - `--check`: Kiểm tra mã hóa của file.
    - `--output`: Đường dẫn lưu file giải mã.
    - `--wordlist`: Đường dẫn tới file chứa danh sách mật khẩu.
    - `--xor`: Dùng phương pháp XOR để giải mã.
    - `--generate-passwords`: Sinh và thử mật khẩu phức tạp.
    """
    print(help_text)


def check_encryption(file_path):
    """Kiểm tra xem file có được mã hóa không và chỉ hiển thị trạng thái mã hóa với màu sắc."""
    try:
        with open(file_path, "rb") as f:
            doc = Doc97File(f)
            is_encrypted = doc.is_encrypted()
            print(f"{GREEN}File có mã hóa: {is_encrypted}{RESET}")

    except Exception as e:
        print(f"{RED}Lỗi khi kiểm tra mã hóa: {e}{RESET}")

def decrypt_with_xor(file_path, password, output_path=None):
    """Giải mã file sử dụng XOR với mật khẩu và chỉ in mật khẩu nếu đúng."""
    try:
        # Mở file gốc để đọc
        with open(file_path, "rb") as f:
            doc = Doc97File(f)
            doc.load_key(password=password)  # Giải mã với mật khẩu

            # Tạo mảng XOR từ mật khẩu
            xor_array = DocumentXOR.create_xor_array_method1(password)

            # Đọc toàn bộ nội dung file vào bộ nhớ
            ibuf = io.BytesIO(f.read())  # Đảm bảo rằng mô-đun io được sử dụng
            
            # Giải mã nội dung của file
            obuf = DocumentXOR.decrypt(password, ibuf, ibuf.read(), None, None)

            # Nếu giải mã thành công, in mật khẩu ra CLI
            print(f"{GREEN}Mật khẩu đúng là: {password}{RESET}")
            return True

    except exceptions.InvalidKeyError:
        # Không cần làm gì nếu mật khẩu không đúng
        pass
    except exceptions.DecryptionError as e:
        print(f"{RED}Lỗi khi giải mã: {e}{RESET}")
    except Exception as e:
        print(f"{RED}Lỗi khi giải mã file: {e}{RESET}")

    return False

def decrypt_file(file_path, password, output_path):
    """Giải mã file bằng mật khẩu với thông báo màu sắc."""
    try:
        with open(file_path, "rb") as f:
            doc = Doc97File(f)
            doc.load_key(password=password)
            with open(output_path, "wb") as outfile:
                doc.decrypt(outfile)
            print(f"{GREEN}File đã được giải mã và lưu tại {output_path}{RESET}")
    except exceptions.InvalidKeyError:
        print(f"{RED}Mật khẩu không hợp lệ.{RESET}")
    except exceptions.DecryptionError as e:
        print(f"{RED}Lỗi khi giải mã: {e}{RESET}")
    except Exception as e:
        print(f"{RED}Lỗi khi giải mã file: {e}{RESET}")

def decrypt_using_wordlist(file_path, wordlist_path, output_path):
    """Giải mã file sử dụng danh sách mật khẩu từ wordlist mà không có XOR."""
    try:
        # Đọc mật khẩu từ wordlist
        with open(wordlist_path, "r") as wordlist_file:
            passwords = wordlist_file.readlines()

        # Sử dụng tqdm để theo dõi tiến trình khi lặp qua từng mật khẩu
        with tqdm(total=len(passwords), desc="Đang thử mật khẩu", unit=" mật khẩu") as pbar:
            # Lặp qua từng mật khẩu trong wordlist
            for password in passwords:
                password = password.strip()  # Loại bỏ khoảng trắng và ký tự xuống dòng
                try:
                    # Mở file và giải mã bằng mật khẩu
                    with open(file_path, "rb") as f:
                        doc = Doc97File(f)
                        doc.load_key(password=password)  # Giải mã với mật khẩu
                        with open(output_path, "wb") as outfile:
                            doc.decrypt(outfile)  # Ghi kết quả giải mã vào file đầu ra
                    print(f"{GREEN}\nFile đã được giải mã thành công với mật khẩu: {password}{RESET}")
                    return # Nếu giải mã thành công, thoát khỏi vòng lặp
                except exceptions.InvalidKeyError:
                    # Nếu mật khẩu không hợp lệ
                    pass
                except exceptions.DecryptionError as e:
                    # Nếu gặp lỗi khi giải mã
                    print(f"{RED}Lỗi khi giải mã với mật khẩu {password}: {e}{RESET}")
                except Exception as e:
                    # Xử lý các lỗi khác
                    print(f"{RED}Lỗi khi giải mã với mật khẩu {password}: {e}{RESET}")

                # Cập nhật thanh tiến trình sau mỗi mật khẩu
                pbar.update(1)

        # Nếu không tìm thấy mật khẩu đúng
        print(f"{YELLOW}Không tìm thấy mật khẩu đúng trong danh sách.{RESET}")
    
    except FileNotFoundError:
        print(f"{RED}File wordlist không tồn tại: {wordlist_path}{RESET}")
    except Exception as e:
        print(f"{RED}Lỗi khi đọc wordlist: {e}{RESET}")

def decrypt_generate_full_complex_passwords(file_path, output_path, max_length):
    """Sinh và thử mật khẩu phức tạp để giải mã file nếu mật khẩu đúng."""
    chars = string.digits + string.ascii_letters + string.punctuation  # Chữ số, chữ cái và ký tự đặc biệt

    def try_password(password, file_path, output_path):
        """Thử mật khẩu và giải mã file nếu mật khẩu đúng."""
        try:
            # Đảm bảo thư mục đầu ra tồn tại
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)  # Tạo thư mục nếu chưa có

            with open(file_path, "rb") as f:
                doc = Doc97File(f)
                doc.load_key(password=password)  # Giải mã với mật khẩu
                with open(output_path, "wb") as outfile:
                    doc.decrypt(outfile)  # Ghi kết quả giải mã vào file đầu ra
            return password  # Trả về mật khẩu nếu giải mã thành công
        except (exceptions.InvalidKeyError, exceptions.DecryptionError) as e:
            return None  # Trả về None nếu có lỗi
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")
            return None  # Bắt mọi lỗi khác

    # Sinh mật khẩu phức tạp
    for length in range(1, max_length + 1):
        password_tuples = itertools.product(chars, repeat=length)
        passwords = [''.join(password_tuple) for password_tuple in password_tuples]

        # Thanh tiến trình
        with tqdm(total=len(passwords), desc=f"Đang thử mật khẩu độ dài {length}", unit=" mật khẩu") as pbar:
            for password in passwords:
                try:
                    result = try_password(password, file_path, output_path)  # Kiểm tra mật khẩu
                    if result:
                        print(f"\nFile đã được giải mã thành công với mật khẩu: {result}")
                        pbar.n = pbar.total  # Đặt thanh tiến trình thành 100%
                        pbar.last_print_n = pbar.total  # Cập nhật vị trí in cuối cùng
                        pbar.update(0)  # Cập nhật để dừng thanh tiến trình
                        pbar.close()  # Đóng thanh tiến trình
                        return  # Thoát khỏi hàm ngay khi giải mã thành công
                    pbar.update(1)  # Cập nhật thanh tiến trình
                except KeyboardInterrupt:
                    print("\nQuá trình đã bị dừng bởi người dùng (Ctrl + C).")
                    pbar.close()  # Đảm bảo thanh tiến trình được đóng
                    return  # Thoát khỏi vòng lặp và kết thúc chương trình

    print(f"{YELLOW}Không tìm thấy mật khẩu đúng trong danh sách.{RESET}")

def main():
    """Điểm vào chính cho CLI.""" 
    display_logo()  # Gọi hàm display_logo để hiển thị logo

    # Tạo đối tượng parser cho CLI
    parser = argparse.ArgumentParser(description="Giải mã file MS DOC 97.")
    parser.add_argument("file", help="Đường dẫn tới file .doc", nargs="?")  # Tùy chọn tham số file
    parser.add_argument("--password", help="Mật khẩu để giải mã file", required=False)
    parser.add_argument("--check", action="store_true", help="Kiểm tra xem file có được mã hóa không")
    parser.add_argument("--output", help="Đường dẫn để lưu file đã giải mã", required=False)
    parser.add_argument("--wordlist", help="Đường dẫn tới file danh sách mật khẩu (wordlist)", required=False)
    parser.add_argument("--xor", action="store_true", help="Giải mã với XOR")
    parser.add_argument("--generate-passwords", action="store_true", help="Sinh và thử mật khẩu phức tạp để giải mã")

    # Phân tích các đối số được nhập từ CLI
    args = parser.parse_args()

    # Nếu không có tham số nào hoặc tham số không hợp lệ, hiển thị hướng dẫn
    if not args.file:
        display_help()
        sys.exit(0)

    if not os.path.exists(args.file):
        print(f"{RED}File {args.file} không tồn tại.{RESET}")
        sys.exit(1)

    if args.check:
        check_encryption(args.file)
    elif args.generate_passwords and args.output:
        # Yêu cầu nhập độ dài tối đa của mật khẩu
        max_length = int(input("Nhập độ dài tối đa của mật khẩu: "))
        decrypt_generate_full_complex_passwords(args.file, args.output, max_length)
    elif args.xor and args.wordlist and args.output:
        decrypt_with_xor(args.file, args.wordlist, args.output)  # Giải mã bằng XOR với wordlist
    elif args.password and args.output:
        decrypt_file(args.file, args.password, args.output)
    elif args.wordlist and args.output:
        decrypt_using_wordlist(args.file, args.wordlist, args.output)
    else:
        print(f"{RED}Để giải mã file, bạn cần cung cấp cả --password hoặc --wordlist và --output.{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
