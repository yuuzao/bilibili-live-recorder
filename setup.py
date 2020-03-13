from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="bilibili-live-recorder",
    version="0.7.1",
    packages=["live"],
    platforms=["unix"],
    install_requires=["requests", "loguru", "yarl"],
    entry_points={"console_scripts": ["blr = live.main:main",]},
    author="yuzao",
    description="This is a script to record bilibili lives, coding with asyncio",
    url="https://github.com/yuuzao/bilibili-live-recorder",
    keywords="bilibili live",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
)
