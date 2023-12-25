from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os
from setuptools.command.build_ext import build_ext as _build_ext


class build_ext(_build_ext):
    def build_extensions(self):
        super().build_extensions()
        for extension in self.extensions:
            for source_file in extension.sources:
                if source_file.endswith('.py'):
                    build_file = self.get_ext_fullpath(extension.name)
                    base, ext = os.path.splitext(build_file)
                    if os.path.exists(base + '.py'):
                        os.remove(base + '.py')


extensions = [
    Extension("AutoIntegrityCheck.validator", ["AutoIntegrityCheck/validator.py"]),
]

setup(
    name='AutoIntegrityCheck',
    version='0.1',
    packages=find_packages(),
    ext_modules=cythonize(extensions),
    cmdclass={'build_ext': build_ext},
    install_requires=[
        'gitpython',
        'requests',
    ],
    author='digitalhigh',
    author_email='d8ahazard@gmail.com',
    description='A tool to validate the integrity of Automatic1111/SdNext environments',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/d8ahazard/AutoIntegrityCheck',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,  # Important to include files specified in MANIFEST.in
    zip_safe=False,
)
