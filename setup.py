from setuptools import setup, find_packages

setup(
    name='password-cracker-word',  # Tên dự án
    version='1.0.0',  # Phiên bản của dự án
    author='Huynh Thanh Tam',  # Tên tác giả
    author_email='hthanhtam@hichaocau.online',  # Email của tác giả
    description='Công cụ giải mã các file MS DOC 97.',  # Mô tả ngắn gọn về dự án
    long_description=open('README.md').read(),  # Mô tả chi tiết, thường được lấy từ file README.md
    long_description_content_type='text/markdown',  # Định dạng của mô tả chi tiết (ở đây là Markdown)
    url='https://github.com/huynhtam03/password-cracker-word',  # URL của dự án trên GitHub hoặc trang web
    packages=find_packages(where='src'),  # Tìm các gói (package) trong thư mục 'src'
    package_dir={'': 'src'},  # Chỉ định thư mục chứa mã nguồn là 'src'
    install_requires=[  # Liệt kê các phụ thuộc mà dự án cần
        'cffi==1.17.1',
        'colorama==0.4.6',
        'cryptography==43.0.3',
        'cupy-cuda12x==13.3.0',
        'fastrlock==0.8.2',
        'numpy==2.1.3',
        'olefile==0.47',
        'password-cracker-word==1.0',  # Giả sử bạn muốn cài đặt chính gói của mình như một phụ thuộc (tham chiếu chính)
        'pycparser==2.22',
        'pyfiglet==1.0.2',
        'setuptools==75.4.0',
        'tqdm==4.67.0',
    ],
    classifiers=[  # Các phân loại (classifiers) cho dự án
        'Programming Language :: Python :: 3',  # Chỉ ra rằng dự án hỗ trợ Python 3
        'License :: OSI Approved :: MIT License',  # Giấy phép của dự án (ở đây là MIT License)
        'Operating System :: OS Independent',  # Dự án không phụ thuộc vào hệ điều hành cụ thể nào
    ],
    entry_points={  # Các điểm vào (entry points) cho giao diện dòng lệnh (CLI)
        'console_scripts': [
            'doc97-decrypt = cli:main',  # Liên kết lệnh 'doc97-decrypt' tới hàm 'main' trong file cli.py
        ],
    },
    python_requires='>=3.6',  # Đảm bảo tương thích với Python 3.6 trở lên
    include_package_data=True,  # Bao gồm các file không phải mã nguồn như README.md và các tài nguyên khác
    package_data={  # Bao gồm các file không phải mã nguồn trong package
        'password_cracker_word': [  # Tên gói (package) của bạn
            'data/wordlists/*.txt',  # Bao gồm tất cả các file .txt trong thư mục wordlists
            'data/encrypted_files/*.doc',  # Bao gồm tất cả các file .doc trong thư mục encrypted_files
            'data/results/*.doc',  # Bao gồm tất cả các file .doc trong thư mục results
        ],
    },
)
