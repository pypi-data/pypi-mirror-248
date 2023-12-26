from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="rd-webhooks",
    version="0.0.1",
    author="Julien Lecomte",
    author_email="julien@lecomte.at",
    url="https://gitlab.com/jlecomte/projects/rd-webhooks",
    description="(deprecated, unmaintained)",
    python_requires=">=3.6",
    packages=find_packages(exclude=["tests*"]),
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "rd-webhooks = rd_webhooks.middleware.gunicorn:main",
        ],
    },
)
