import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dwcflint",
    version="1.2.14",
    author="Daniel Wellington",
    author_email="dwcflint@example.com",
    description="A collection of extra rules for linting cloudformation files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dwtechnologies/dwcflint",
    packages=setuptools.find_packages(),
    install_requires=[
        'cfn-lint'
    ],
    python_requires='>=3.6',
    scripts=[
        'scripts/dwcflint'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Topic :: Software Development :: Quality Assurance"
    ],
)
