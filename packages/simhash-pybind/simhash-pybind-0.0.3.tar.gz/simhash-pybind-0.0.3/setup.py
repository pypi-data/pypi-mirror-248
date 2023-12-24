from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

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


setup(
    name="simhash-pybind",
    version="0.0.3",
    description="Near-Duplicate Detection with Simhash",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    setup_requires=['pybind11'],
    python_requires='>=3.6',
    packages=["simhash"],
    package_dir={"simhash": "simhash"},
    ext_modules=ext_modules,
)
