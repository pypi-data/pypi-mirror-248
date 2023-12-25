from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup (
    name="vizmyip",
    version='0.1.2',
    description='Visualizes public IP information of your system.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Ashish S. Maharjan",
    author_email="<hello@amaharjan.de>",
    url='https://github.com/asis2016/vizmyip',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['flask', 'requests'],
    entry_points={
        'console_scripts': [
            'vizmyip = vizmyip.app:run_app',
        ],
    },
    keywords=['python', 'flask', 'ip', 'public ip'],
    license='MIT',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)
