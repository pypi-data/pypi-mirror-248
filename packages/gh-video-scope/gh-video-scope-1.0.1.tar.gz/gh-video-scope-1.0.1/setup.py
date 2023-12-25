from setuptools import setup, find_packages

setup(
    name="gh-video-scope",
    version="1.0.1",
    author="Massimo Ghiani",
    author_email="m.ghiani@gmail.com",
    url="https://github.com/m-ghiani/VideoScope",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "main.py", ".vscode"]
    ),
    license="MIT",
    description="Package for extracting metadata from video files",
    long_description_content_type="text/x-rst",
    long_description=open("README.rst").read(),
    readme="README.md",
    install_requires=["ffmpeg-python", "future", "numpy", "opencv-python"],
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
    entry_points={
        "console_scripts": [
            "videoinfo=videoscope.cli:main",  # 'nome_comando=modulo.funzione'
        ],
    },
)
