from setuptools import find_packages, setup

setup(
    name="vicky",
    version="0.3.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    install_requires=[
        "boto3",
        "click",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "vicky = vicky.scripts.vicky:cli",
        ],
    },
)
