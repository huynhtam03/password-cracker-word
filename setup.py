from setuptools import setup, find_packages

setup(
    name='password-cracker-word',  # Updated project name
    version='1.0.0',
    author='Your Name',  # Replace with your name
    author_email='your.email@example.com',  # Replace with your email
    description='A tool to decrypt MS DOC 97 files with various methods like XOR and password cracking.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/huynhtam03/password-cracker-word',  # Replace with your GitHub or project URL
    packages=find_packages(where='src'),  # Ensure that packages are found in the 'src' directory
    package_dir={'': 'src'},  # Maps the package namespace to the 'src' directory
    install_requires=[  # List dependencies your project needs
        'pyfiglet',
        'tqdm',
        'colorama',  # Assuming the 'xor_obfuscation' module is available for installation
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={  # CLI entry points for the user to run commands
        'console_scripts': [
            'doc97-decrypt = cli:main',  # Maps the command 'doc97-decrypt' to the 'main' function in cli.py
        ],
    },
    python_requires='>=3.6',  # Ensure compatibility with Python 3.6 and later
    test_suite='tests',  # Specify the location of your test suite
    include_package_data=True,  # Includes non-Python files, like README.md or other assets
    data_files=[  # Optionally, include data files such as the wordlist files
        ('wordlists', ['data/wordlists/10MPASS.txt', 'data/wordlists/dictionary.txt']),
        ('encrypted_files', ['data/encrypted_files/hay.doc', 'data/encrypted_files/hihi.doc']),
        ('results', ['data/results/decrypted_file.doc', 'data/results/decrypted_hay.doc']),
    ],
)
