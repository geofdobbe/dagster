from pathlib import Path
from typing import Dict

from setuptools import find_packages, setup


def get_version() -> str:
    version: Dict[str, str] = {}
    with open(Path(__file__).parent / "dagster_airflow/version.py", encoding="utf8") as fp:
        exec(fp.read(), version)  # pylint: disable=W0122

    return version["__version__"]


ver = get_version()
# dont pin dev installs to avoid pip dep resolver issues
pin = "" if ver == "0+dev" else f"=={ver}"
setup(
    name="dagster-airflow",
    version=ver,
    author="Elementl",
    author_email="hello@elementl.com",
    license="Apache-2.0",
    description="Airflow plugin for Dagster",
    url="https://github.com/dagster-io/dagster",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["dagster_airflow_tests*"]),
    install_requires=[
        f"dagster{pin}",
        "docker",
        "python-dateutil>=2.8.0",
        "lazy_object_proxy",
        # https://issues.apache.org/jira/browse/AIRFLOW-6854
        'typing_extensions; python_version>="3.8"',
    ],
    project_urls={
        # airflow will embed a link this in the providers page UI
        "project-url/documentation": "https://docs.dagster.io",
    },
    extras_require={
        "kubernetes": ["kubernetes>=3.0.0", "cryptography>=2.0.0"],
        "test": [
            # Airflow should be provided by the end user, not us. For example, GCP Cloud
            # Composer ships a fork of Airflow; we don't want to override it with our install.
            # See https://github.com/dagster-io/dagster/issues/2701
            "apache-airflow==1.10.10",
            # https://github.com/dagster-io/dagster/issues/3858
            "sqlalchemy>=1.0,<1.4.0",
            "marshmallow-sqlalchemy<0.26.0",
            "boto3==1.9.*",
            "kubernetes==10.0.1",
            # New WTForms release breaks the version of airflow used by tests
            "WTForms<3.0.0",
            # pinned based on certain incompatible versions of Jinja2, which is itself pinned
            # by apache-airflow==1.10.10
            "markupsafe<=2.0.1",
        ],
    },
    entry_points={
        "console_scripts": ["dagster-airflow = dagster_airflow.cli:main"],
        # airflow 1.0/2.0 plugin format
        "airflow.plugins": ["dagster_airflow = dagster_airflow.__init__:DagsterAirflowPlugin"],
        # airflow 2.0 provider format
        "apache_airflow_provider": ["provider_info=dagster_airflow.__init__:get_provider_info"],
    },
)
