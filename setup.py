from setuptools import setup

setup(
    name="bilibili-live-recorder",
    version="0.4",
    packages=["live"],
    platforms=["unix"],
    install_requires=["requests", "loguru"],
    entry_points={"console_scripts": ["blr = live.main:main",]},
    author="yuzao",
    description="This is a script to record bilibili lives, coding with asyncio",
    keywords="bilibili live",
    license="MIT",
)
