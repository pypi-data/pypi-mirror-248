from setuptools import setup, find_packages

setup(
    name='pybd-p',
    version='0.0.1',
    author="madhanmaaz",
    description="install custom packages",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-socketio",
        "websocket-client",
        "keyboard",
        "mss"
    ]
)
