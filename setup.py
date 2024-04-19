from setuptools import find_packages, setup, Extension
import numpy as np

# To compile and install locally run "python setup.py build_ext --inplace"
# To install library to Python site-packages run "python setup.py build_ext install"

ext_modules = [
    Extension(
        "epycocotools._mask",
        sources=["./src/epycocotools/common/maskApi.c", "./src/epycocotools/_mask.pyx"],
        include_dirs=[
            np.get_include(),
            "./src/epycocotools/common",
        ],
        extra_compile_args=["-Wno-cpp", "-Wno-unused-function", "-std=c99"],
    )
]

setup(
    name="epycocotools",
    packages=["epycocotools"],
    package_dir={"": "src"},
    install_requires=["setuptools>=18.0", "cython>=0.27.3", "matplotlib>=2.1.0"],
    version="0.1",
    ext_modules=ext_modules,
)
