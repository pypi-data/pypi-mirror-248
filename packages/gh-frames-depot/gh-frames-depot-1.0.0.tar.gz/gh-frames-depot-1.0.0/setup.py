from setuptools import setup, find_packages

long_description = open("README.rst").read()

setup(
    name="gh-frames-depot",
    version="1.0.0",
    url="https://github.com/m-ghiani/FRAMES_DEPOT",
    author="Massimo Ghiani",
    author_email="m.ghiani@gmail.com",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "main.py", ".vscode"]
    ),
    license="MIT",
    description="Package for buffering frames in memory and sharing them between processes.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=["numpy>=1.26.2", "asyncio>=3.4.3"],
    python_requires=">=3.10",  # Specifica la versione di Python richiesta
    include_package_data=True,
    classifiers=[
        # Classificatori che danno informazioni sul tuo pacchetto
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)

# python3.10 setup.py sdist bdist_wheel
