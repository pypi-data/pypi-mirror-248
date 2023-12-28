from setuptools import setup, find_packages

long_description = open("README.rst").read()

setup(
    name="double-buffer-shared-memory-manager",
    version="1.0.0",
    url="https://github.com/m-ghiani/DOUBLE_BUFFER_SHARED_MEMORY_MANAGER",
    author="Massimo Ghiani",
    author_email="m.ghiani@gmail.com",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "main.py", ".vscode"]
    ),
    license="MIT",
    description="Package for communication with RabbitMQ",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=["colorlog>=6.8.0", "numpy>=1.26.2", "readerwriterlock>=1.0.9"],
    python_requires=">=3.10",  # Specifica la versione di Python richiesta
    include_package_data=True,
    classifiers=[
        # Classificatori che danno informazioni sul tuo pacchetto
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)

# python3.10 setup.py sdist bdist_wheel
