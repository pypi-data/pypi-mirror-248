from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        name="simhash._simhash",
        sources = ['simhash/simhash.cpp',
                    'simhash/simhash-cpp/src/permutation.cpp',
                    'simhash/simhash-cpp/src/simhash.cpp'],
        extra_compile_args=['-O3', '-std=c++14'],
        include_dirs=["simhash/simhash-cpp/include"]
    ),
]


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="simhash-pybind",
    version="0.0.2",
    description="Near-Duplicate Detection with Simhash",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: C++",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=required,
    python_requires='>=3.6',
    packages=["simhash"],
    package_dir={"simhash": "simhash"},
    ext_modules=ext_modules,
)
