import pathlib, setuptools

setuptools.setup(
    name="pyqliksense",
    version="0.0.7",
    description="A simple library to communicate with Qlik Sense Enterprise on Windows",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/Andrey-Kosarev/py_qlik_sense",
    author="Andrei Kosarev",
    author_email="kosarev_andrey@mail.ru",
    license="The Unlicense",
    project_urls={
        "Source": "https://github.com/Andrey-Kosarev/py_qlik_sense"
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.11,<3.12",
    install_requires=[
        "requests==2.31.0",
        "requests-ntlm==1.2.0",
        "websocket-client==1.7.0",
        "websockets==11.0.3"
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
)