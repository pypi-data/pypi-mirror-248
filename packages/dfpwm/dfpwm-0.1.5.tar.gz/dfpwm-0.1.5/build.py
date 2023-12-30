import os
import sys
from time import sleep

import numpy
from setuptools import Extension
from setuptools.command.build_ext import build_ext
from setuptools.errors import PlatformError, CCompilerError, ExecError, PlatformError

USE_CYTHON = os.environ.get('USE_CYTHON', False)
CYTHON = False
try:
    from Cython.Build import cythonize

    CYTHON = True
except ImportError:
    USE_CYTHON = False

file_ext = '.pyx' if USE_CYTHON else '.c'

build_modules = ['convertor']

extensions = [
    Extension(f'dfpwm.{module}', [f'./dfpwm/{module}{file_ext}'])
    for module in build_modules
]

include_dirs = [
    numpy.get_include()
]


class ExtBuilder(build_ext):
    def run(self):
        try:
            super().run()
        except (PlatformError, FileNotFoundError):
            raise Exception('File not found. Could not compile C extension.')

    def build_extension(self, ext):
        try:
            super().build_extension(ext)
        except (CCompilerError, ExecError, PlatformError, ValueError):
            raise Exception('Could not compile C extension.')


def build(setup_kwargs: dict):
    os.environ['CFLAGS'] = '-O3'

    setup_kwargs.update({
        'ext_modules': cythonize(
            extensions, language_level=3,
            compiler_directives={'linetrace': True}
        ) if USE_CYTHON else extensions, "include_dirs": include_dirs,
        "cmdclass": {
            "build_ext": ExtBuilder,
        }
    })


if __name__ == '__main__':
    params = sys.argv[1:]
    if len(params) != 0 and 'build' == params[0]:
        if not CYTHON:
            print("Please install cython to convert to .c file")
            sys.exit(-1)

        cythonize([f'./dfpwm/{module}.pyx' for module in build_modules])
