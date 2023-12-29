from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension("_pytinyxml2", ["pytinyxml2.i",
                                  "tinyxml2.cpp"], ["."],
                  swig_opts=['-c++'])
    ]
)
