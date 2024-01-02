import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
with open("requirements.txt", "r") as fh:
    REQUIREMENTS = fh.readlines()
with open("mk_badge/VERSION", "r") as fh:
    VERSION = fh.read().strip()

setuptools.setup(
    name="mk_badge",
    version=VERSION,
    author="LoveIsGrief",
    author_email="loveisgrief@tuta.io",
    description="Makes badges like the ones made by travis-ci to show the status of a build",
    install_requires=REQUIREMENTS,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/NamingThingsIsHard/media_tools/mk_badge",
    packages=setuptools.find_packages(),
    package_data={
        "mk_badge": [
            "VERSION",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    project_urls={
        "Bug Tracker": "https://gitlab.com/NamingThingsIsHard/media_tools/mk_badge/issues",
    },
    entry_points={
        "console_scripts": [
            "mk_badge = mk_badge.main:main",
        ]
    }
)
