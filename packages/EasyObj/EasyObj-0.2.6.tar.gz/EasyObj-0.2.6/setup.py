import setuptools
from versionManager import readPackageJson

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='EasyObj',
    version=readPackageJson().version,
    license="GPL-3.0",
    description='EasyObj lets you manipulate objects as easily as in JavaScript.',
    packages=["EasyObj"],
    zip_safe=False,
    url="https://github.com/Howardzhangdqs/EasyObj",
    python_requires=">=3.8",
    author_email="zjh@shanghaiit.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=(
        "Programming Language :: Python :: 3",
    ),
)
