import os
from typing import Dict, List

from setuptools import find_packages, setup


def get_version() -> str:
  # https://packaging.python.org/guides/single-sourcing-package-version/
  init = open(os.path.join("moss", "__init__.py"), "r").read().split()
  return init[init.index("__version__") + 2][1:-1]


def get_install_requires() -> List[str]:
  launchpad = [
    "tensorflow==2.8.1",
    "dm-reverb==0.12.0",
    "dm-launchpad==0.5.2",
  ]

  jax_requirements = [
    "jax==0.4.9",
    "jaxlib==0.4.9",
    "dm-haiku==0.0.10",
    "chex",
    "flax",
    "optax",
    "rlax",
  ] + launchpad

  requirements = [
    "absl-py",
    "envpool",
    "dm-env",
    "dm-tree",
    "numpy",
    "pillow",
    "pygame",
    "tensorboardX",
    "tqdm",
    "typing-extensions",
  ] + jax_requirements
  return requirements


def get_extras_require() -> Dict[str, List[str]]:
  req = {
    "dev":
      [
        "sphinx<7",
        "sphinx_rtd_theme",
        "jinja2",
        "sphinxcontrib-bibtex",
        "flake8",
        "flake8-bugbear",
        "yapf",
        "isort",
        "mypy",
        "pydocstyle",
        "doc8",
        "pyenchant",
        "pytest",
        "pytest-cov",
      ],
  }
  return req


setup(
  name="moss-rl",
  version=get_version(),
  description="A Python library for Reinforcement Learning.",
  long_description=open("README.md", encoding="utf8").read(),
  long_description_content_type="text/markdown",
  author="lanzhiyi",
  author_email="lanzhiy.mail@qq.com",
  url="https://github.com/hilanzy/moss",
  packages=find_packages(),
  license="MIT",
  python_requires=">=3.8",
  install_requires=get_install_requires(),
  extras_require=get_extras_require(),
  classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    "Development Status :: 3 - Alpha",
    # Indicate who your project is intended for
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    # Pick your license as you wish (should match "license" above)
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
  ],
  keywords="reinforcement-learning python machine learning",
)
