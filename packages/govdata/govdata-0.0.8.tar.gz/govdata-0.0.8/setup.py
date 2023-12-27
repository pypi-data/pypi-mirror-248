from setuptools import setup, find_packages

setup(
    name="govdata",
    author="Giancarlo Rizzo",
    version="0.0.8",
    packages=["."],
    install_requires=[
        'Jinja2==3.0.3',
        'pandas==1.5.3',
        'pretty-errors==1.2.25',
        'pytest==7.4.3',
        'pytest-cov==4.1.0',
        'requests==2.31.0',
        'requests-mock==1.11.0',
        "pytest-cov",
        "fastapi",
        "kaleido",
        "python-multipart",
        "uvicorn"
    ]
)
