from setuptools import setup, find_packages

setup(
    name="Windows11-Debloater",
    version="1.0.0",  # Define a static version
    description="A tool to debloat and optimize Windows 11",
    author="TheSharkKingOG & Swishhyy",
    packages=find_packages(),
    install_requires=[
        "altgraph>=0.17.4",
        "packaging>=24.2",
        "pefile>=2023.2.7",
        "psutil>=7.0.0",
        "pyinstaller>=6.13.0",
        "pyinstaller-hooks-contrib>=2025.2",
        "PyQt5>=5.15.11",
        "PyQt5-Qt5>=5.15.2",
        "PyQt5_sip>=12.17.0",
        "pywin32>=310",
        "pywin32-ctypes>=0.2.3",
        "setuptools>=78.1.0",
        "Pillow>=9.5.0",
    ],
    python_requires=">=3.7",
)