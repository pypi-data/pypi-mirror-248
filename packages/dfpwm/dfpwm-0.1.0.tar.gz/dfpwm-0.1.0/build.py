import os

import numpy
from Cython.Build import cythonize
from distutils.command.build_ext import build_ext


def build(setup_kwargs: dict):
    extensions = [
        './dfpwm/dfpwm.pyx'
    ]
    include_dirs = [
        numpy.get_include()
    ]

    os.environ['CFLAGS'] = '-O3'

    setup_kwargs.update({
        'ext_modules': cythonize(
            extensions, language_level=3,
            compiler_directives={'linetrace': True}
        )
    })

    if 'include_dirs' in setup_kwargs:
        setup_kwargs['include_dirs'].extend(include_dirs)
    else:
        setup_kwargs['include_dirs'] = include_dirs
