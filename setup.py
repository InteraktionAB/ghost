import os

import pkg_resources
from setuptools import setup, find_packages

setup(
    name="ghostswap",
    version="1.0",
    description="Ghost swap as API",
    author="Sreerag",
    url='https://github.com/InteraktionAB/ghost',
    packages=find_packages(include=['AdaptiveWingLoss', 'apex', 'coordinate_reg', 'examples', 'insightface_func', 'models', 'network', 'utils']),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ]
)
