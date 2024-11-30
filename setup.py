from setuptools import setup, find_packages

setup(
    name='password-cracker-word',  # Project name
    version='1.0.0',
    author='Huynh Thanh Tam',  # Replace with your name
    author_email='your.hthanhtam@hichaocau.online',  # Replace with your email
    description='A tool to decrypt MS DOC 97 files with various methods like XOR and password cracking.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/huynhtam03/password-cracker-word',  # Replace with your GitHub or project URL
    packages=find_packages(where='src'),  # Ensure that packages are found in the 'src' directory
    package_dir={'': 'src'},  # Maps the package namespace to the 'src' directory
    install_requires=[  # List dependencies your project needs
        'cffi==1.17.1',
        'colorama==0.4.6',
        'cryptography==43.0.3',
        'cupy-cuda12x==13.3.0',
        'fastrlock==0.8.2',
        'numpy==2.1.3',
        'olefile==0.47',
        'password-cracker-word==1.0',  # Assuming you want to install your own package as a dependency (self-reference)
        'pycparser==2.22',
        'pyfiglet==1.0.2',
        'setuptools==75.4.0',
        'tqdm==4.67.0',
    ],
    classifiers=[  # Classifiers for your package
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
    include_package_data=True,  # Includes non-Python files like README.md or other assets
    package_data={  # Includes non-Python files inside the package
        'password_cracker_word': [  # This should match the package name
            'data/wordlists/*.txt',  # Include all .txt files from the wordlists directory
            'data/encrypted_files/*.doc',  # Include all .doc files from the encrypted_files directory
            'data/results/*.doc',  # Include all .doc files from the results directory
        ],
    },
)
