# Copyright (C) 2020 Samuel Baker

DESCRIPTION = "Just some methods that are used consistently in construction or formatting of papers or data sets for" \
              " analysis"
LONG_DESCRIPTION = """
# FormattingMethods
Just some methods that are used consistently in construction or formatting of papers or data sets for analysis. 
Separated out from multiple jupyter notebooks so that instead of duplicating and potentially having version issues there
is a single repository that can be updated for all analysis.

Repository at [this page][repo]

[repo]: https://github.com/sbaker-dev/FormattingMethods

"""
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

DISTNAME = 'FormattingMethods'
MAINTAINER = 'Samuel Baker'
MAINTAINER_EMAIL = 'samuelbaker.researcher@gmail.com'
LICENSE = 'MIT'
DOWNLOAD_URL = "https://github.com/sbaker-dev/FormattingMethods"
VERSION = "0.08.0"
PYTHON_REQUIRES = ">=3.6"

INSTALL_REQUIRES = [


    'csvObject', 'IPython', 'pandas']

PACKAGES = [
    "FormattingMethods",
]

CLASSIFIERS = [
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: MIT License',
]

if __name__ == "__main__":

    from setuptools import setup

    import sys

    if sys.version_info[:2] < (3, 7):
        raise RuntimeError("FormattingMethods requires python >= 3.7.")

    setup(
        name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
        license=LICENSE,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        python_requires=PYTHON_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        packages=PACKAGES,
        classifiers=CLASSIFIERS
    )
