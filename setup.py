from setuptools import setup

setup(
    name="bilibili-live-recorder",
    version="0.2",
    packages=["live"],
    platforms=["unix"],
    install_requires=["requests", "loguru"],
    entry_points={"console_scripts": ["blr = live.main:main",]},
    author="yuzao",
    description="This is an script used to record bilibili live stream",
    keywords="bilibili live",
    license="MIT",
)
