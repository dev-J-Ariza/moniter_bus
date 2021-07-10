import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="moniter-bus-peking",
    version="3.0.0",
    author="dev-J-Ariza",
    author_email="f_Ariza_dev@outlook.com",
    description="Get real time bus in Peking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dev-J-Ariza/moniter_bus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    REQUIRED=[
        'requests', 'colorama', 'mock',
    ],
    include_package_data=True,
)
