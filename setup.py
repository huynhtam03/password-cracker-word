from setuptools import setup, find_packages
import os

# Đọc nội dung của README.md để sử dụng trong long_description
long_description = ''
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='password-cracker-word',  # Tên dự án
    version='1.0.0',  # Phiên bản dự án
    author='Huynh Thanh Tam',  # Tên tác giả
    author_email='hthanhtam@hichaocau.online',  # Email của tác giả
    description='Công cụ giải mã các file MS DOC 97.',  # Mô tả ngắn gọn
    long_description=long_description,  # Đọc mô tả dài từ README.md
    long_description_content_type='text/markdown',  # Định dạng mô tả dài (Markdown)
    url='https://github.com/huynhtam03/password-cracker-word',  # URL dự án trên GitHub
    packages=find_packages(where='src'),  # Tìm các package trong thư mục src
    package_dir={'': 'src'},  # Chỉ định thư mục chứa mã nguồn là 'src'
    install_requires=[  # Liệt kê các phụ thuộc cần thiết
        'colorama==0.4.6',
        'pyfiglet==1.0.2',
        'setuptools==75.4.0',
    ],
    classifiers=[  # Các phân loại dự án
        'Programming Language :: Python :: 3',  # Dự án hỗ trợ Python 3
        'Operating System :: OS Independent',  # Dự án không phụ thuộc hệ điều hành cụ thể
    ],
    entry_points={  # Định nghĩa các điểm vào (entry points) cho CLI
        'console_scripts': [
            'doc97-decrypt = cli:main',  # Liên kết lệnh 'doc97-decrypt' tới hàm 'main' trong src/cli.py
        ],
    },
    python_requires='>=3.6',  # Đảm bảo tương thích với Python 3.6 trở lên
    include_package_data=True,  # Bao gồm các file bổ sung như README.md
    package_data={  # Bao gồm các file không phải mã nguồn (chẳng hạn như dữ liệu và tệp DOC)
        'password_cracker_word': [
            'data/wordlists/*.txt',  # Bao gồm các file *.txt trong thư mục 'data/wordlists'
            'data/encrypted_files/*.doc',  # Bao gồm các file *.doc trong thư mục 'data/encrypted_files'
            'data/results/*.doc',  # Bao gồm các file *.doc trong thư mục 'data/results'
        ],
    },
)
