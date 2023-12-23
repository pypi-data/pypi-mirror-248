import os
import platform
import subprocess

import setuptools

# Package metadata.

name = "clickzetta-travel"
description = "Toolkits including Transpile, Run, And Validate queries, for Evaluating clickzetta with Love."

# Should be one of:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Production/Stable'
release_status = "Development Status :: 3 - Alpha"
dependencies = [
    'clickzetta-migration >= 0.0.8',
    'streamlit >= 1.26.0',
    'cz-sqlglot >= 0.0.1',
    'pandas >= 2.0.3',
]
extras = {

}

all_extras = []

for extra in extras:
    all_extras.extend(extras[extra])

extras["all"] = all_extras

# Setup boilerplate below this line.

package_root = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(package_root, "travel/version.py")) as fp:
    exec(fp.read(), version)
version = version["__version__"]

packages = setuptools.find_packages(exclude=["build", "test", "test.*", "scripts", "scripts.*"])

setuptools.setup(
    name=name,
    version=version,
    description=description,
    url='https://www.yunqi.tech/',
    author="mocun",
    author_email="hanmiao.li@clickzetta.com",
    platforms="Posix; MacOS X;",
    packages=packages,
    install_requires=dependencies,
    extras_require=extras,
    python_requires=">=3.7",
    entry_points={
        'console_scripts': ['travel=travel.batch.trans_batch:main',
                            'glot=travel.glot.glot:main'],
    },
    include_package_data=True,
    zip_safe=False,
)
